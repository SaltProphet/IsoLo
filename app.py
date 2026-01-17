import gradio as gr
import numpy as np
import librosa
import librosa.display
import soundfile as sf
import os
import tempfile
import zipfile
import time
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal
from typing import Tuple, List, Any, Optional, Dict
import shutil

# SAM Audio integration
from sam_audio_integration import SAMAudioSeparator, create_named_stem_separations

# Use a non-interactive backend for Matplotlib
matplotlib.use('Agg')

# --- CONSTANTS & DICTIONARIES ---

KEY_TO_CAMELOT = {
    "C Maj": "8B", "G Maj": "9B", "D Maj": "10B", "A Maj": "11B", "E Maj": "12B",
    "B Maj": "1B", "F# Maj": "2B", "Db Maj": "3B", "Ab Maj": "4B", "Eb Maj": "5B",
    "Bb Maj": "6B", "F Maj": "7B",
    "A Min": "8A", "E Min": "9A", "B Min": "10A", "F# Min": "11A", "C# Min": "12A",
    "G# Min": "1A", "D# Min": "2A", "Bb Min": "3A", "F Min": "4A", "C Min": "5A",
    "G Min": "6A", "D Min": "7A",
    # Enharmonic equivalents
    "Gb Maj": "2B", "Cb Maj": "7B", "A# Min": "3A", "D# Maj": "5B", "G# Maj": "4B"
}

# Fixed reverse mapping to avoid "lossy" inversion
CAMELOT_TO_KEY = {
    "8B": "C Maj", "9B": "G Maj", "10B": "D Maj", "11B": "A Maj", "12B": "E Maj",
    "1B": "B Maj", "2B": "F# Maj / Gb Maj", "3B": "Db Maj", "4B": "Ab Maj / G# Maj", "5B": "Eb Maj / D# Maj",
    "6B": "Bb Maj", "7B": "F Maj / Cb Maj",
    "8A": "A Min", "9A": "E Min", "10A": "B Min", "11A": "F# Min", "12A": "C# Min",
    "1A": "G# Min", "2A": "D# Min", "3A": "Bb Min / A# Min", "4A": "F Min", "5A": "C Min",
    "6A": "G Min", "7A": "D Min"
}

STEM_NAMES = ["vocals", "drums", "bass", "other", "guitar", "piano"]

# --- UTILITY FUNCTIONS ---

def freq_to_midi(freq: float) -> int:
    """Converts a frequency in Hz to a MIDI note number."""
    if freq <= 0:
        return 0
    # C1 is ~32.7 Hz. Let's set a reasonable floor.
    if freq < 32.0:
        return 0
    return int(round(69 + 12 * np.log2(freq / 440.0)))

def write_midi_file(notes_list: List[Tuple[int, float, float]], bpm: float, output_path: str):
    """
    Writes a basic MIDI file from a list of notes.
    Note: This is a simplified MIDI writer and may have issues.
    Using a dedicated library like 'mido' is recommended for robust use.
    """
    if not notes_list:
        return

    tempo_us_per_beat = int(60000000 / bpm)
    division = 96  # Ticks per quarter note
    seconds_per_tick = 60.0 / (bpm * division)

    # Sort notes by start time
    notes_list.sort(key=lambda x: x[1])

    current_tick = 0
    midi_events = []

    # --- MIDI Track Header ---
    # Set Tempo: FF 51 03 TTTTTT (TTTTTT = tempo_us_per_beat)
    tempo_bytes = tempo_us_per_beat.to_bytes(3, 'big')
    track_data = b'\x00\xFF\x51\x03' + tempo_bytes
    
    # Set Time Signature: FF 58 04 NN DD CC BB (Using 4/4)
    track_data += b'\x00\xFF\x58\x04\x04\x02\x18\x08' 
    
    # Set Track Name
    track_data += b'\x00\xFF\x03\x0BLoopArchitect' # 11 chars

    for note, start_sec, duration_sec in notes_list:
        if note == 0:
            continue

        # Calculate delta time from last event
        target_tick = int(round(start_sec / seconds_per_tick))
        delta_tick = target_tick - current_tick
        current_tick = target_tick

        # Note On event (Channel 1, Velocity 100)
        note_on = [0x90, note, 100]
        track_data += encode_delta_time(delta_tick) + bytes(note_on)

        # Note Off event (Channel 1, Velocity 0)
        duration_ticks = int(round(duration_sec / seconds_per_tick))
        if duration_ticks == 0:
            duration_ticks = 1 # Minimum duration
            
        note_off = [0x80, note, 0]
        track_data += encode_delta_time(duration_ticks) + bytes(note_off)
        current_tick += duration_ticks

    # End of track
    track_data += b'\x00\xFF\x2F\x00'

    # --- MIDI File Header ---
    # MThd, header_length (6), format (1), num_tracks (1), division
    header = b'MThd' + (6).to_bytes(4, 'big') + (1).to_bytes(2, 'big') + (1).to_bytes(2, 'big') + division.to_bytes(2, 'big')
    
    # MTrk, track_length, track_data
    track_chunk = b'MTrk' + len(track_data).to_bytes(4, 'big') + track_data
    midi_data = header + track_chunk

    with open(output_path, 'wb') as f:
        f.write(midi_data)

def encode_delta_time(ticks: int) -> bytes:
    """Encodes an integer tick value into MIDI variable-length quantity."""
    buffer = ticks & 0x7F
    ticks >>= 7
    if ticks > 0:
        buffer |= 0x80
        while ticks > 0:
            buffer = (buffer << 8) | ((ticks & 0x7F) | 0x80)
            ticks >>= 7
        buffer = (buffer & 0xFFFFFF7F) # Clear MSB of last byte
        
        # Convert buffer to bytes
        byte_list = []
        while buffer > 0:
            byte_list.insert(0, buffer & 0xFF)
            buffer >>= 8
        if not byte_list:
            return b'\x00'
        return bytes(byte_list)
    else:
        return bytes([buffer])

def get_harmonic_recommendations(key_str: str) -> str:
    """Calculates harmonically compatible keys based on the Camelot wheel."""
    code = KEY_TO_CAMELOT.get(key_str, "N/A")
    if code == "N/A":
        return "N/A (Key not recognized or 'Unknown Key' detected.)"

    try:
        num = int(code[:-1])
        mode = code[-1]
        opposite_mode = 'B' if mode == 'A' else 'A'
        num_plus_one = (num % 12) + 1
        num_minus_one = 12 if num == 1 else num - 1
        
        recs_codes = [
            f"{num}{opposite_mode}",   # e.g., 8A (A Min) -> 8B (C Maj)
            f"{num_plus_one}{mode}",   # e.g., 8A (A Min) -> 9A (E Min)
            f"{num_minus_one}{mode}"   # e.g., 8A (A Min) -> 7A (D Min)
        ]
        
        rec_keys = [f"{CAMELOT_TO_KEY.get(r_code, f'Code {r_code}')} ({r_code})" for r_code in recs_codes]
        return " | ".join(rec_keys)
    except Exception as e:
        print(f"Error calculating recommendations: {e}")
        return "N/A (Error calculating recommendations.)"

def detect_key(y: np.ndarray, sr: int) -> str:
    """Analyzes the audio to determine the most likely musical key."""
    try:
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_sums = np.sum(chroma, axis=1)
        
        # Avoid division by zero if audio is silent
        if np.sum(chroma_sums) == 0:
            return "Unknown Key"
            
        chroma_norm = chroma_sums / np.sum(chroma_sums)

        # Krumhansl-Schmuckler key-finding algorithm templates
        major_template = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_template = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        
        # Normalize templates
        major_template /= np.sum(major_template)
        minor_template /= np.sum(minor_template)

        pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        major_correlations = [np.dot(chroma_norm, np.roll(major_template, i)) for i in range(12)]
        best_major_index = np.argmax(major_correlations)

        minor_correlations = [np.dot(chroma_norm, np.roll(minor_template, i)) for i in range(12)]
        best_minor_index = np.argmax(minor_correlations)

        if major_correlations[best_major_index] > minor_correlations[best_minor_index]:
            return pitch_classes[best_major_index] + " Maj"
        else:
            return pitch_classes[best_minor_index] + " Min"
    except Exception as e:
        print(f"Key detection failed: {e}")
        return "Unknown Key"

def apply_modulation(y: np.ndarray, sr: int, bpm: float, rate: str, pan_depth: float, level_depth: float) -> np.ndarray:
    """Applies tempo-synced LFOs for panning and volume modulation."""
    if y.ndim == 0:
        return y
    if y.ndim == 1:
        y = np.stack((y, y), axis=-1) # Convert to stereo

    N = len(y)
    duration_sec = N / sr

    rate_map = {'1/2': 0.5, '1/4': 1, '1/8': 2, '1/16': 4}
    beats_per_measure = rate_map.get(rate, 1)
    # LFO frequency = (BPM / 60) * (beats_per_measure / 4.0) -- seems off.
    # Let's redefine: LFO freq in Hz = (BPM / 60) * (1 / (4 / beats_per_measure))
    # e.g., 1/4 rate at 120BPM = 2Hz. (120/60) * (1 / (4/1)) = 2 * (1/4) = 0.5Hz? No.
    # 120 BPM = 2 beats/sec. 1/4 note = 1 beat. So LFO should be 2 Hz.
    # 1/8 note = 4 Hz.
    # 1/16 note = 8 Hz.
    # 1/2 note = 1 Hz.
    # Formula: (BPM / 60) * (rate_map_value / 4)
    # 1/4 note: (120/60) * (1/4) = 0.5 Hz. Still wrong.
    # Let's try: (BPM / 60) * (rate_map_value)
    # 1/4 note @ 120BPM: (120/60) * 1 = 2 Hz. Correct.
    # 1/8 note @ 120BPM: (120/60) * 2 = 4 Hz. Correct.
    # 1/2 note @ 120BPM: (120/60) * 0.5 = 1 Hz. Correct.
    lfo_freq_hz = (bpm / 60.0) * rate_map.get(rate, 1)

    t = np.linspace(0, duration_sec, N, endpoint=False)

    # Panning LFO (Sine wave, -1 to 1)
    if pan_depth > 0:
        pan_lfo = np.sin(2 * np.pi * lfo_freq_hz * t) * pan_depth
        # L_mod/R_mod should be 0-1. (1-pan_lfo)/2 and (1+pan_lfo)/2 gives 0-1 range.
        L_mod = (1 - pan_lfo) / 2.0
        R_mod = (1 + pan_lfo) / 2.0
        # This is amplitude panning, not constant power. Good enough.
        y[:, 0] *= L_mod
        y[:, 1] *= R_mod

    # Level LFO (Tremolo) (Sine wave, 0 to 1)
    if level_depth > 0:
        level_lfo = (np.sin(2 * np.pi * lfo_freq_hz * t) + 1) / 2.0
        # gain_multiplier ranges from (1-level_depth) to 1
        gain_multiplier = (1 - level_depth) + (level_depth * level_lfo)
        y[:, 0] *= gain_multiplier
        y[:, 1] *= gain_multiplier

    return y

def apply_normalization_dbfs(y: np.ndarray, target_dbfs: float) -> np.ndarray:
    """Applies peak normalization to match a target dBFS value."""
    if target_dbfs >= 0:
        return y # Don't normalize to 0dBFS or higher

    current_peak_amp = np.max(np.abs(y))
    if current_peak_amp < 1e-9: # Avoid division by zero on silence
        return y
        
    target_peak_amp = 10**(target_dbfs / 20.0)

    gain = target_peak_amp / current_peak_amp
    y_normalized = y * gain
    
    # Clip just in case of floating point inaccuracies
    y_normalized = np.clip(y_normalized, -1.0, 1.0)
    return y_normalized

def apply_filter_modulation(y: np.ndarray, sr: int, bpm: float, rate: str, filter_type: str, freq: float, depth: float) -> np.ndarray:
    """Applies a tempo-synced LFO to a 2nd order Butterworth filter cutoff frequency."""
    if depth == 0 or filter_type == "None":
        return y

    # Ensure stereo for LFO application
    if y.ndim == 1:
        y = np.stack((y, y), axis=-1)
    if y.ndim == 0:
        return y

    N = len(y)
    duration_sec = N / sr

    # LFO Rate Calculation
    rate_map = {'1/2': 0.5, '1/4': 1, '1/8': 2, '1/16': 4}
    lfo_freq_hz = (bpm / 60.0) * rate_map.get(rate, 1)

    t = np.linspace(0, duration_sec, N, endpoint=False)

    # LFO: ranges from 0 to 1
    lfo_value = (np.sin(2 * np.pi * lfo_freq_hz * t) + 1) / 2.0

    # Modulate Cutoff Frequency: Cutoff = BaseFreq + (LFO * Depth)
    cutoff_modulation = freq + (lfo_value * depth)
    # Safety clip to prevent instability
    nyquist = sr / 2.0
    cutoff_modulation = np.clip(cutoff_modulation, 20.0, nyquist - 100.0) # Keep away from Nyquist

    y_out = np.zeros_like(y)
    
    # --- BUG FIX ---
    # Was: filter_type.lower().replace('-pass', '') -> 'low' (ValueError)
    # Now: filter_type.lower().replace('-pass', 'pass') -> 'lowpass' (Correct)
    filter_type_b = filter_type.lower().replace('-pass', 'pass')

    frame_size = 512  # Frame-based update for filter coefficients
    if N < frame_size:
        frame_size = N # Handle very short audio

    # Apply filter channel by channel
    for channel in range(y.shape[1]):
        zi = signal.lfilter_zi(*signal.butter(2, 20.0, btype=filter_type_b, fs=sr))

        for frame_start in range(0, N, frame_size):
            frame_end = min(frame_start + frame_size, N)
            if frame_start == frame_end: continue # Skip empty frames
            
            frame = y[frame_start:frame_end, channel]

            # Use the average LFO cutoff for the frame
            avg_cutoff = np.mean(cutoff_modulation[frame_start:frame_end])

            # Calculate 2nd order Butterworth filter coefficients
            try:
                b, a = signal.butter(2, avg_cutoff, btype=filter_type_b, fs=sr)
            except ValueError as e:
                print(f"Butterworth filter error: {e}. Using last good coefficients.")
                # This can happen if avg_cutoff is bad, though we clip it.
                # If it still fails, we just re-use the last good b, a.
                # In the first frame, this is not robust.
                if 'b' not in locals():
                    b, a = signal.butter(2, 20.0, btype=filter_type_b, fs=sr) # Failsafe

            # Apply filter to the frame, updating the state `zi`
            filtered_frame, zi = signal.lfilter(b, a, frame, zi=zi)
            y_out[frame_start:frame_end, channel] = filtered_frame

    return y_out

def apply_crossfade(y: np.ndarray, fade_samples: int) -> np.ndarray:
    """Applies a linear fade-in and fade-out to a clip."""
    if fade_samples == 0:
        return y
    
    N = len(y)
    fade_samples = min(fade_samples, N // 2) # Fade can't be longer than half the clip
    
    if fade_samples == 0:
        return y # Clip is too short to fade

    # Create fade ramps
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    y_out = y.copy()
    
    # Apply fades (handling mono/stereo)
    if y.ndim == 1:
        y_out[:fade_samples] *= fade_in
        y_out[-fade_samples:] *= fade_out
    else:
        y_out[:fade_samples, :] *= fade_in[:, np.newaxis]
        y_out[-fade_samples:, :] *= fade_out[:, np.newaxis]
        
    return y_out

def apply_envelope(y: np.ndarray, sr: int, attack_gain_db: float, sustain_gain_db: float) -> np.ndarray:
    """Applies a simple attack/sustain gain envelope to one-shots."""
    N = len(y)
    if N == 0:
        return y
        
    # Simple fixed attack time of 10ms
    attack_time_sec = 0.01
    attack_samples = min(int(attack_time_sec * sr), N // 2)
    
    start_gain = 10**(attack_gain_db / 20.0)
    end_gain = 10**(sustain_gain_db / 20.0)

    # Envelope: Linear ramp from start_gain to end_gain over attack_samples, then hold end_gain
    envelope = np.ones(N) * end_gain
    if attack_samples > 0:
        attack_ramp = np.linspace(start_gain, end_gain, attack_samples)
        envelope[:attack_samples] = attack_ramp

    # Apply envelope (handling mono/stereo)
    if y.ndim == 1:
        y_out = y * envelope
    else:
        y_out = y * envelope[:, np.newaxis]
        
    return y_out

# --- CORE PROCESSING FUNCTIONS ---

def separate_stems_with_sam_audio(
    audio_file_path: str,
    use_sam_audio: bool = False,
    sam_prompts: Optional[List[str]] = None
) -> Tuple[
    Dict[str, Optional[Tuple[int, np.ndarray]]],
    float, str, str
]:
    """
    Enhanced stem separation supporting both traditional stems and SAM Audio named isolation.
    
    Args:
        audio_file_path: Path to the audio file
        use_sam_audio: Whether to use SAM Audio for named isolation
        sam_prompts: List of text descriptions for sounds to isolate (if using SAM Audio)
        
    Returns:
        Tuple of (stems_dict, detected_bpm, detected_key, harmonic_recs)
        stems_dict maps stem/prompt name to (sample_rate, audio_data) tuples
    """
    if audio_file_path is None:
        raise gr.Error("No audio file uploaded!")
    
    try:
        # Load audio for analysis
        y_orig, sr_orig = librosa.load(audio_file_path, sr=None, mono=False)
        
        # Ensure stereo for processing
        if y_orig.ndim == 1:
            y_orig = np.stack([y_orig, y_orig], axis=-1)
        if y_orig.ndim == 2 and y_orig.shape[0] < y_orig.shape[1]:
            y_orig = y_orig.T  # Transpose to (N, 2)
            
        y_mono = librosa.to_mono(y_orig)

        # Detect tempo and key
        tempo, _ = librosa.beat.beat_track(y=y_mono, sr=sr_orig)
        detected_bpm = 120.0 if tempo is None or tempo.size == 0 or tempo[0] == 0 else float(np.round(tempo[0]))
        detected_key = detect_key(y_mono, sr_orig)
        harmonic_recs = get_harmonic_recommendations(detected_key)

        stems_data: Dict[str, Optional[Tuple[int, np.ndarray]]] = {}
        
        # Convert to int16 for Gradio Audio component
        y_int16 = (y_orig * 32767).astype(np.int16)

        # Use SAM Audio if enabled and prompts provided
        if use_sam_audio and sam_prompts:
            print("Using SAM Audio for named sound isolation...")
            try:
                separator = SAMAudioSeparator()
                if not separator.is_available():
                    print("SAM Audio not available, falling back to traditional stems")
                    use_sam_audio = False
                else:
                    # Separate each named sound
                    results = separator.separate_multiple(audio_file_path, sam_prompts)
                    
                    for prompt, (sr, audio_data) in results.items():
                        # Convert to int16 for Gradio
                        if audio_data.dtype != np.int16:
                            audio_int16 = (audio_data * 32767).astype(np.int16)
                        else:
                            audio_int16 = audio_data
                        
                        # Ensure stereo
                        if audio_int16.ndim == 1:
                            audio_int16 = np.stack([audio_int16, audio_int16], axis=-1)
                        
                        stems_data[prompt] = (sr, audio_int16)
                    
                    print(f"Successfully isolated {len(results)} named sounds using SAM Audio")
            except Exception as e:
                print(f"Error with SAM Audio: {e}")
                print("Falling back to traditional stem separation")
                use_sam_audio = False
        
        # Fall back to traditional stems if SAM Audio not used or failed
        if not use_sam_audio or not sam_prompts:
            print("Using traditional stem separation (mock)...")
            # In a real implementation, this would use Demucs or similar
            # For now, return the original audio for each traditional stem
            for name in STEM_NAMES:
                stems_data[name] = (sr_orig, y_int16.copy())

        return stems_data, detected_bpm, detected_key, harmonic_recs
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        import traceback
        traceback.print_exc()
        raise gr.Error(f"Error processing audio: {str(e)}")


def separate_stems(audio_file_path: str) -> Tuple[
    Optional[Tuple[int, np.ndarray]], 
    Optional[Tuple[int, np.ndarray]], 
    Optional[Tuple[int, np.ndarray]], 
    Optional[Tuple[int, np.ndarray]], 
    Optional[Tuple[int, np.ndarray]], 
    Optional[Tuple[int, np.ndarray]], 
    float, str, str
]:
    """
    Simulates stem separation and detects BPM and Key.
    Returns Gradio Audio tuples (sr, data) for each stem.
    
    This is the original function maintained for backward compatibility.
    """
    stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
        audio_file_path, 
        use_sam_audio=False,
        sam_prompts=None
    )
    
    # Extract traditional stems in expected order
    return (
        stems_dict.get("vocals"), 
        stems_dict.get("drums"), 
        stems_dict.get("bass"), 
        stems_dict.get("other"),
        stems_dict.get("guitar"), 
        stems_dict.get("piano"), 
        bpm, key, recs
    )

def generate_waveform_preview(y: np.ndarray, sr: int, stem_name: str, temp_dir: str) -> str:
    """Generates a Matplotlib image showing the waveform."""
    img_path = os.path.join(temp_dir, f"{stem_name}_preview.png")

    plt.figure(figsize=(10, 3))
    y_display = librosa.to_mono(y.T) if y.ndim > 1 and y.shape[0] < y.shape[1] else y
    y_display = librosa.to_mono(y) if y.ndim > 1 else y
    
    librosa.display.waveshow(y_display, sr=sr, x_axis='time', color="#4a7098")
    plt.title(f"{stem_name} Waveform (Processed)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()

    return img_path

def slice_stem_real(
    stem_audio_tuple: Optional[Tuple[int, np.ndarray]],
    loop_choice: str,
    sensitivity: float,
    stem_name: str,
    manual_bpm: float,
    time_signature: str,
    crossfade_ms: int,
    transpose_semitones: int,
    detected_key: str,
    pan_depth: float,
    level_depth: float,
    modulation_rate: str,
    target_dbfs: float,
    attack_gain: float,
    sustain_gain: float,
    filter_type: str,
    filter_freq: float,
    filter_depth: float
) -> Tuple[List[str], Optional[str]]:
    """
    Slices a single stem and applies transformations.
    Returns a list of filepaths and a path to a preview image.
    """
    if stem_audio_tuple is None:
        return [], None

    try:
        sample_rate, y_int = stem_audio_tuple
        # Convert from int16 array back to float
        y = y_int.astype(np.float32) / 32767.0
        
        if y.ndim == 0 or len(y) == 0:
            return [], None

        # --- 1. PITCH SHIFTING (if enabled) ---
        if transpose_semitones != 0:
            y = librosa.effects.pitch_shift(y, sr=sample_rate, n_steps=transpose_semitones)

        # --- 2. FILTER MODULATION ---
        if filter_depth > 0 and filter_type != "None":
            y = apply_filter_modulation(y, sample_rate, manual_bpm, modulation_rate, filter_type, filter_freq, filter_depth)

        # --- 3. PAN/LEVEL MODULATION ---
        normalized_pan_depth = pan_depth / 100.0
        normalized_level_depth = level_depth / 100.0
        if normalized_pan_depth > 0 or normalized_level_depth > 0:
            y = apply_modulation(y, sample_rate, manual_bpm, modulation_rate, normalized_pan_depth, normalized_level_depth)

        # --- 4. NORMALIZATION ---
        if target_dbfs < 0:
            y = apply_normalization_dbfs(y, target_dbfs)

        # --- 5. DETERMINE BPM & KEY ---
        bpm_int = int(round(manual_bpm))
        key_tag = "UnknownKey"
        if detected_key != "Unknown Key":
            key_tag = detected_key.replace(" ", "")
            if transpose_semitones != 0:
                root, mode = detected_key.split(" ")
                pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                try:
                    current_index = pitch_classes.index(root)
                    new_index = (current_index + transpose_semitones) % 12
                    new_key_root = pitch_classes[new_index]
                    key_tag = f"{new_key_root}{mode}Shift"
                except ValueError:
                    key_tag = f"Shifted{transpose_semitones}" # Fallback
        
        # --- 6. MIDI GENERATION (Melodic Stems) ---
        output_files = []
        loops_dir = tempfile.mkdtemp()
        is_melodic = stem_name in ["vocals", "bass", "guitar", "piano", "other"]

        if is_melodic and ("Bar Loops" in loop_choice):
            try:
                y_mono_for_midi = librosa.to_mono(y)
                # Use piptrack for pitch detection
                pitches, magnitudes = librosa.piptrack(y=y_mono_for_midi, sr=sample_rate)
                
                # Get the dominant pitch at each frame
                main_pitch_line = np.zeros(pitches.shape[1])
                for t in range(pitches.shape[1]):
                    index = magnitudes[:, t].argmax()
                    main_pitch_line[t] = pitches[index, t]

                notes_list = []
                i = 0
                hop_length = 512 # Default hop for piptrack
                
                while i < len(main_pitch_line):
                    current_freq = main_pitch_line[i]
                    current_midi = freq_to_midi(current_freq)
                    if current_midi == 0: # Skip silence/unpitched
                        i += 1
                        continue

                    # Find end of this note
                    j = i
                    while j < len(main_pitch_line) and freq_to_midi(main_pitch_line[j]) == current_midi:
                        j += 1

                    duration_frames = j - i
                    # Only add notes that are long enough (e.g., > 2 frames)
                    if duration_frames >= 2:
                        start_sec = librosa.frames_to_time(i, sr=sample_rate, hop_length=hop_length)
                        duration_sec = librosa.frames_to_time(duration_frames, sr=sample_rate, hop_length=hop_length)
                        notes_list.append((current_midi, start_sec, duration_sec))
                    
                    i = j

                if notes_list:
                    full_stem_midi_path = os.path.join(loops_dir, f"{stem_name}_MELODY_{key_tag}_{bpm_int}BPM.mid")
                    write_midi_file(notes_list, manual_bpm, full_stem_midi_path)
                    output_files.append(full_stem_midi_path)

            except Exception as e:
                print(f"MIDI generation failed for {stem_name}: {e}")

        # --- 7. CALCULATE TIMING & SLICING ---
        beats_per_bar = 4
        if time_signature == "3/4":
            beats_per_bar = 3

        if "Bar Loops" in loop_choice:
            bars = int(loop_choice.split(" ")[0])
            loop_type_tag = f"{bars}Bar"
            loop_duration_samples = int((60.0 / manual_bpm * beats_per_bar * bars) * sample_rate)
            fade_samples = int((crossfade_ms / 1000.0) * sample_rate)

            if loop_duration_samples > 0 and len(y) > loop_duration_samples:
                num_loops = len(y) // loop_duration_samples
                for i in range(min(num_loops, 16)):  # Limit to 16 loops
                    start_sample = i * loop_duration_samples
                    end_sample = min(start_sample + loop_duration_samples, len(y))
                    slice_data = y[start_sample:end_sample]

                    # Apply crossfade
                    slice_data = apply_crossfade(slice_data, fade_samples)

                    filename = os.path.join(loops_dir, f"{stem_name}_{loop_type_tag}_{i+1:03d}_{key_tag}_{bpm_int}BPM.wav")
                    sf.write(filename, slice_data, sample_rate, subtype='PCM_16')
                    output_files.append(filename)

        elif "One-Shots" in loop_choice:
            loop_type_tag = "OneShot"
            y_mono_for_onsets = librosa.to_mono(y)
            
            # IMPLEMENTED: Use sensitivity to find onsets
            # Adjust 'wait' and 'delta' based on sensitivity (0-1)
            # Higher sensitivity = lower delta, shorter wait
            delta = 0.5 * (1.0 - sensitivity) # 0.0 -> 0.5
            wait_sec = 0.1 * (1.0 - sensitivity) # 0.0 -> 0.1
            wait_samples = int(wait_sec * sample_rate / 512) # in frames
            
            onset_frames = librosa.onset.onset_detect(
                y=y_mono_for_onsets, 
                sr=sample_rate, 
                units='frames', 
                backtrack=True,
                delta=delta,
                wait=wait_samples
            )
            onset_samples = librosa.frames_to_samples(onset_frames)
            
            # Add end of file as the last "onset"
            onset_samples = np.append(onset_samples, len(y))

            for i in range(min(len(onset_samples) - 1, 40)):  # Limit to 40 slices
                start_sample = onset_samples[i]
                end_sample = onset_samples[i+1]
                slice_data = y[start_sample:end_sample]
                
                if len(slice_data) < 100: # Skip tiny fragments
                    continue

                # IMPLEMENTED: Apply attack/sustain envelope
                slice_data = apply_envelope(slice_data, sample_rate, attack_gain, sustain_gain)
                
                # Apply short fade-out to prevent clicks
                slice_data = apply_crossfade(slice_data, int(0.005 * sample_rate)) # 5ms fade

                filename = os.path.join(loops_dir, f"{stem_name}_{loop_type_tag}_{i+1:03d}_{key_tag}_{bpm_int}BPM.wav")
                sf.write(filename, slice_data, sample_rate, subtype='PCM_16')
                output_files.append(filename)

        # --- 8. VISUALIZATION GENERATION ---
        img_path = generate_waveform_preview(y, sample_rate, stem_name, loops_dir)

        # Clean up the temp dir for the *next* run
        # Gradio File components need the files to exist, so we don't delete loops_dir yet
        # A more robust solution would use gr.TempFile() or manage cleanup
        
        return output_files, img_path

    except Exception as e:
        print(f"Error processing stem {stem_name}: {e}")
        import traceback
        traceback.print_exc()
        return [], None # Return empty on error


def slice_all_and_zip(
    vocals_audio: Optional[Tuple[int, np.ndarray]],
    drums_audio: Optional[Tuple[int, np.ndarray]],
    bass_audio: Optional[Tuple[int, np.ndarray]],
    other_audio: Optional[Tuple[int, np.ndarray]],
    guitar_audio: Optional[Tuple[int, np.ndarray]],
    piano_audio: Optional[Tuple[int, np.ndarray]],
    loop_choice: str,
    sensitivity: float,
    manual_bpm: float,
    time_signature: str,
    crossfade_ms: int,
    transpose_semitones: int,
    detected_key: str,
    pan_depth: float,
    level_depth: float,
    modulation_rate: str,
    target_dbfs: float,
    attack_gain: float,
    sustain_gain: float,
    filter_type: str,
    filter_freq: float,
    filter_depth: float,
    progress: gr.Progress
) -> Optional[str]:
    """Slices all available stems and packages them into a ZIP file."""
    try:
        stems_to_process = {
            "vocals": vocals_audio, "drums": drums_audio, "bass": bass_audio,
            "other": other_audio, "guitar": guitar_audio, "piano": piano_audio
        }

        # Filter out None stems
        valid_stems = {name: data for name, data in stems_to_process.items() if data is not None}

        if not valid_stems:
            raise gr.Error("No stems to process! Please separate stems first.")

        # Create temporary directory for all outputs
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "Loop_Architect_Pack.zip")
        
        all_sliced_files = []

        # Use progress tracker
        progress(0, desc="Starting...")
        
        num_stems = len(valid_stems)
        for i, (name, data) in enumerate(valid_stems.items()):
            progress((i+1)/num_stems, desc=f"Slicing {name}...")
            
            # Process stem
            sliced_files, _ = slice_stem_real(
                data, loop_choice, sensitivity, name,
                manual_bpm, time_signature, crossfade_ms, transpose_semitones, detected_key,
                pan_depth, level_depth, modulation_rate, target_dbfs,
                attack_gain, sustain_gain, filter_type, filter_freq, filter_depth
            )
            all_sliced_files.extend(sliced_files)

        progress(0.9, desc="Zipping files...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in all_sliced_files:
                if not file_path: continue
                # Create a sane folder structure in the ZIP
                file_type = os.path.splitext(file_path)[1][1:].upper() # WAV or MID
                arcname = os.path.join(file_type, os.path.basename(file_path))
                zf.write(file_path, arcname)
        
        progress(1.0, desc="Done!")
        
        # Clean up individual slice files (but not the zip dir)
        for file_path in all_sliced_files:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        return zip_path

    except Exception as e:
        print(f"Error creating ZIP: {e}")
        import traceback
        traceback.print_exc()
        raise gr.Error(f"Error creating ZIP: {str(e)}")


def separate_named_sounds(
    audio_file_path: str,
    prompts_text: str
) -> Tuple[Dict[str, Tuple[int, np.ndarray]], float, str, str]:
    """
    Separate multiple named sounds from audio using SAM Audio.
    
    This is a convenience function that can be called to isolate any named sounds
    instead of using traditional stems.
    
    Args:
        audio_file_path: Path to the audio file
        prompts_text: Comma-separated list of sound descriptions
                     Example: "lead vocals, guitar solo, bass line, drum beat"
        
    Returns:
        Tuple of (isolated_sounds_dict, bpm, key, harmonic_recs)
    """
    if audio_file_path is None:
        raise gr.Error("No audio file uploaded!")
    
    # Parse prompts from comma-separated text
    prompts = [p.strip() for p in prompts_text.split(",") if p.strip()]
    
    if not prompts:
        raise gr.Error("Please provide at least one sound description")
    
    print(f"Isolating {len(prompts)} named sounds: {prompts}")
    
    # Use the enhanced separation function
    stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
        audio_file_path,
        use_sam_audio=True,
        sam_prompts=prompts
    )
    
    return stems_dict, bpm, key, recs


# --- GRADIO INTERFACE ---

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="red")) as demo:
    gr.Markdown("# 🎵 Loop Architect (Pro Edition)")
    gr.Markdown("Upload any song to separate it into stems, detect musical attributes, and then slice and tag the stems for instant use in a DAW.")

    # State variables
    detected_bpm_state = gr.State(value=120.0)
    detected_key_state = gr.State(value="Unknown Key")
    harmonic_recs_state = gr.State(value="---")

    # Outputs for each stem (as gr.Audio tuples)
    vocals_audio = gr.Audio(visible=False, type="numpy")
    drums_audio = gr.Audio(visible=False, type="numpy")
    bass_audio = gr.Audio(visible=False, type="numpy")
    other_audio = gr.Audio(visible=False, type="numpy")
    guitar_audio = gr.Audio(visible=False, type="numpy")
    piano_audio = gr.Audio(visible=False, type="numpy")
    
    stem_audio_outputs = [vocals_audio, drums_audio, bass_audio, other_audio, guitar_audio, piano_audio]

    with gr.Row():
        with gr.Column(scale=1):
            # --- INPUT COLUMN ---
            gr.Markdown("### 1. Upload & Analyze")
            audio_input = gr.Audio(label="Upload Song", type="filepath")
            separate_button = gr.Button("Separate Stems & Analyze", variant="primary")
            
            with gr.Accordion("Global Musical Settings", open=True):
                manual_bpm_input = gr.Number(label="BPM", value=120.0, step=0.1, interactive=True)
                key_display = gr.Textbox(label="Detected Key", value="Unknown Key", interactive=False)
                harmonic_recs_display = gr.Textbox(label="Harmonic Recommendations", value="---", interactive=False)
                transpose_semitones = gr.Slider(label="Transpose (Semitones)", minimum=-12, maximum=12, value=0, step=1)
                time_signature = gr.Radio(label="Time Signature", choices=["4/4", "3/4"], value="4/4")

            with gr.Accordion("Global Slicing Settings", open=True):
                loop_choice = gr.Radio(label="Loop Type", choices=["1 Bar Loops", "2 Bar Loops", "4 Bar Loops", "One-Shots"], value="4 Bar Loops")
                sensitivity = gr.Slider(label="One-Shot Sensitivity", minimum=0.0, maximum=1.0, value=0.5, info="Higher = more slices")
                crossfade_ms = gr.Slider(label="Loop Crossfade (ms)", minimum=0, maximum=50, value=10, step=1)
            
            with gr.Accordion("Global FX Settings", open=False):
                target_dbfs = gr.Slider(label="Normalize Peak to (dBFS)", minimum=-24.0, maximum=-0.0, value=-1.0, step=0.1, info="-0.0 = Off")
                
                gr.Markdown("---")
                gr.Markdown("**LFO Modulation (Pan/Level)**")
                modulation_rate = gr.Radio(label="Modulation Rate", choices=["1/2", "1/4", "1/8", "1/16"], value="1/4")
                pan_depth = gr.Slider(label="Pan Depth (%)", minimum=0, maximum=100, value=0, step=1)
                level_depth = gr.Slider(label="Level Depth (%)", minimum=0, maximum=100, value=0, step=1, info="Tremolo effect")
                
                gr.Markdown("---")
                gr.Markdown("**LFO Modulation (Filter)**")
                filter_type = gr.Radio(label="Filter Type", choices=["None", "Low-pass", "High-pass"], value="None")
                filter_freq = gr.Slider(label="Filter Base Freq (Hz)", minimum=20, maximum=10000, value=5000, step=100)
                filter_depth = gr.Slider(label="Filter Mod Depth (Hz)", minimum=0, maximum=10000, value=0, step=100, info="LFO amount")
                
                gr.Markdown("---")
                gr.Markdown("**One-Shot Shaping**")
                attack_gain = gr.Slider(label="Attack Gain (dB)", minimum=-24.0, maximum=6.0, value=0.0, step=0.5, info="Gain at start of transient")
                sustain_gain = gr.Slider(label="Sustain Gain (dB)", minimum=-24.0, maximum=6.0, value=0.0, step=0.5, info="Gain for note body")

            gr.Markdown("### 3. Generate Pack")
            slice_all_button = gr.Button("SLICE ALL & GENERATE PACK", variant="primary")
            zip_file_output = gr.File(label="Download Your Loop Pack")

        with gr.Column(scale=2):
            # --- OUTPUT COLUMN ---
            gr.Markdown("### 2. Review Stems & Slices")
            with gr.Tabs():
                # Create a tab for each stem
                for i, name in enumerate(STEM_NAMES):
                    with gr.Tab(name.capitalize()):
                        with gr.Row():
                            # The (hidden) audio output for this stem
                            stem_audio_component = stem_audio_outputs[i]
                            
                            # Visible components
                            preview_image = gr.Image(label="Processed Waveform", interactive=False)
                            slice_files = gr.Files(label="Generated Slices & MIDI", interactive=False)
                        
                        # Add a button to slice just this one stem
                        slice_one_button = gr.Button(f"Slice This {name.capitalize()} Stem")
                        
                        # Gather all global settings as inputs
                        all_settings = [
                            loop_choice, sensitivity, manual_bpm_input, time_signature, crossfade_ms,
                            transpose_semitones, detected_key_state, pan_depth, level_depth, modulation_rate,
                            target_dbfs, attack_gain, sustain_gain, filter_type, filter_freq, filter_depth
                        ]
                        
                        # Wire up the "Slice One" button
                        slice_one_button.click(
                            fn=slice_stem_real,
                            inputs=[stem_audio_component, gr.State(value=name)] + all_settings,
                            outputs=[slice_files, preview_image]
                        )

    # --- EVENT LISTENERS ---

    # 1. "Separate Stems" button click
    separate_button.click(
        fn=separate_stems,
        inputs=[audio_input],
        outputs=stem_audio_outputs + [detected_bpm_state, detected_key_state, harmonic_recs_state]
    )

    # 2. When BPM state changes, update the visible input box
    detected_bpm_state.change(
        fn=lambda x: x,
        inputs=[detected_bpm_state],
        outputs=[manual_bpm_input]
    )
    
    # 3. When Key state changes, update the visible text boxes
    detected_key_state.change(
        fn=lambda x: x,
        inputs=[detected_key_state],
        outputs=[key_display]
    )
    harmonic_recs_state.change(
        fn=lambda x: x,
        inputs=[harmonic_recs_state],
        outputs=[harmonic_recs_display]
    )

    # 4. "SLICE ALL" button click
    slice_all_button.click(
        fn=slice_all_and_zip,
        inputs=stem_audio_outputs + all_settings,
        outputs=[zip_file_output]
    )


if __name__ == "__main__":
    demo.launch(debug=True)
