"""Audio slicer module for creating loops and one-shots."""

import os
import numpy as np
try:
    import librosa
    import soundfile as sf
    from scipy import signal
    AUDIO_LIBS_AVAILABLE = True
except ImportError:
    AUDIO_LIBS_AVAILABLE = False

from workflow_types import WorkflowContext, ModuleResult
from typing import List, Tuple


class Slicer:
    """Slices stems into loops and one-shots, generates MIDI."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Audio Slicer"
    
    def is_required(self) -> bool:
        """This module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Slice all stems based on configuration.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with sliced files
        """
        if not AUDIO_LIBS_AVAILABLE:
            return ModuleResult(
                success=False,
                message="",
                error="Required libraries not installed. Run: pip install librosa soundfile scipy"
            )
        
        try:
            if not context.stems:
                return ModuleResult(
                    success=False,
                    message="",
                    error="No stems available to slice"
                )
            
            total_slices = 0
            total_midi = 0
            
            # Slice each stem
            for stem_name, (sr, audio) in context.stems.items():
                slices, midi = self._slice_stem(
                    stem_name=stem_name,
                    sample_rate=sr,
                    audio=audio,
                    context=context
                )
                
                context.sliced_files.extend(slices)
                context.midi_files.extend(midi)
                context.generated_files.extend(slices)
                context.generated_files.extend(midi)
                
                total_slices += len(slices)
                total_midi += len(midi)
            
            return ModuleResult(
                success=True,
                message=f"Slicing complete: {total_slices} slices, {total_midi} MIDI files"
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Slicing failed: {str(e)}"
            )
    
    def _slice_stem(
        self,
        stem_name: str,
        sample_rate: int,
        audio: np.ndarray,
        context: WorkflowContext
    ) -> Tuple[List[str], List[str]]:
        """Slice a single stem into loops or one-shots."""
        sliced_files = []
        midi_files = []
        
        # Convert from int16 to float
        y = audio.astype(np.float32) / 32767.0 if audio.dtype == np.int16 else audio
        
        # Apply transformations from config
        y = self._apply_transformations(y, sample_rate, context)
        
        # Determine slicing type
        config = context.config
        
        if config.loop_type in ['1-bar', '2-bar', '4-bar']:
            sliced_files = self._slice_bar_loops(y, sample_rate, stem_name, context)
            
            # Generate MIDI for melodic stems
            if stem_name.lower() in ['vocals', 'bass', 'guitar', 'piano', 'other'] and config.include_midi:
                midi_file = self._generate_midi(y, sample_rate, stem_name, context)
                if midi_file:
                    midi_files.append(midi_file)
        else:
            # One-shots
            sliced_files = self._slice_one_shots(y, sample_rate, stem_name, context)
        
        return sliced_files, midi_files
    
    def _apply_transformations(
        self,
        y: np.ndarray,
        sample_rate: int,
        context: WorkflowContext
    ) -> np.ndarray:
        """Apply FX transformations to audio."""
        config = context.config
        
        # Transpose
        if config.transpose_semitones != 0:
            y = librosa.effects.pitch_shift(y, sr=sample_rate, n_steps=config.transpose_semitones)
        
        # Normalize
        if config.normalize_peak < 0:
            target_peak = 10**(config.normalize_peak / 20.0)
            current_peak = np.max(np.abs(y))
            if current_peak > 1e-9:
                gain = target_peak / current_peak
                y = np.clip(y * gain, -1.0, 1.0)
        
        return y
    
    def _slice_bar_loops(
        self,
        y: np.ndarray,
        sample_rate: int,
        stem_name: str,
        context: WorkflowContext
    ) -> List[str]:
        """Slice audio into bar-aligned loops."""
        sliced_files = []
        config = context.config
        
        # Calculate loop duration
        bars = int(config.loop_type.split('-')[0])
        beats_per_bar = 4 if config.time_signature == '4/4' else 3
        loop_duration_sec = (60.0 / context.bpm) * beats_per_bar * bars
        loop_duration_samples = int(loop_duration_sec * sample_rate)
        
        if loop_duration_samples == 0 or len(y) <= loop_duration_samples:
            return sliced_files
        
        # Calculate crossfade
        fade_samples = int((config.crossfade_ms / 1000.0) * sample_rate)
        
        # Slice into loops
        num_loops = len(y) // loop_duration_samples
        for i in range(min(num_loops, 16)):  # Limit to 16 loops
            start = i * loop_duration_samples
            end = min(start + loop_duration_samples, len(y))
            slice_data = y[start:end]
            
            # Apply crossfade
            slice_data = self._apply_crossfade(slice_data, fade_samples)
            
            # Generate filename
            key_tag = context.key.replace(" ", "")
            bpm_int = int(round(context.bpm))
            filename = os.path.join(
                context.temp_dir,
                f"{stem_name}_{bars}Bar_{i+1:03d}_{key_tag}_{bpm_int}BPM.wav"
            )
            
            sf.write(filename, slice_data, sample_rate, subtype='PCM_16')
            sliced_files.append(filename)
        
        return sliced_files
    
    def _slice_one_shots(
        self,
        y: np.ndarray,
        sample_rate: int,
        stem_name: str,
        context: WorkflowContext
    ) -> List[str]:
        """Slice audio into one-shots using onset detection."""
        sliced_files = []
        config = context.config
        
        # Convert to mono for onset detection
        y_mono = librosa.to_mono(y) if y.ndim > 1 else y
        
        # Detect onsets with sensitivity
        sensitivity = config.one_shot_sensitivity
        delta = 0.5 * (1.0 - sensitivity)
        wait_sec = 0.1 * (1.0 - sensitivity)
        wait_samples = int(wait_sec * sample_rate / 512)
        
        onset_frames = librosa.onset.onset_detect(
            y=y_mono,
            sr=sample_rate,
            units='frames',
            backtrack=True,
            delta=delta,
            wait=wait_samples
        )
        onset_samples = librosa.frames_to_samples(onset_frames)
        onset_samples = np.append(onset_samples, len(y))
        
        # Slice at onsets
        key_tag = context.key.replace(" ", "")
        bpm_int = int(round(context.bpm))
        
        for i in range(min(len(onset_samples) - 1, 40)):  # Limit to 40
            start = onset_samples[i]
            end = onset_samples[i + 1]
            slice_data = y[start:end]
            
            if len(slice_data) < 100:  # Skip tiny fragments
                continue
            
            # Apply short fade
            slice_data = self._apply_crossfade(slice_data, int(0.005 * sample_rate))
            
            filename = os.path.join(
                context.temp_dir,
                f"{stem_name}_OneShot_{i+1:03d}_{key_tag}_{bpm_int}BPM.wav"
            )
            
            sf.write(filename, slice_data, sample_rate, subtype='PCM_16')
            sliced_files.append(filename)
        
        return sliced_files
    
    def _apply_crossfade(self, y: np.ndarray, fade_samples: int) -> np.ndarray:
        """Apply linear crossfade to audio."""
        if fade_samples == 0:
            return y
        
        N = len(y)
        fade_samples = min(fade_samples, N // 2)
        
        if fade_samples == 0:
            return y
        
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        y_out = y.copy()
        
        if y.ndim == 1:
            y_out[:fade_samples] *= fade_in
            y_out[-fade_samples:] *= fade_out
        else:
            y_out[:fade_samples, :] *= fade_in[:, np.newaxis]
            y_out[-fade_samples:, :] *= fade_out[:, np.newaxis]
        
        return y_out
    
    def _generate_midi(
        self,
        y: np.ndarray,
        sample_rate: int,
        stem_name: str,
        context: WorkflowContext
    ) -> str:
        """Generate MIDI file from melodic audio (simplified stub)."""
        # This is a simplified version - full implementation would use
        # the MIDI generation logic from app.py
        key_tag = context.key.replace(" ", "")
        bpm_int = int(round(context.bpm))
        
        midi_path = os.path.join(
            context.temp_dir,
            f"{stem_name}_MELODY_{key_tag}_{bpm_int}BPM.mid"
        )
        
        # Create empty MIDI file as stub
        # In full implementation, this would call write_midi_file from app.py
        try:
            with open(midi_path, 'wb') as f:
                # Minimal MIDI file header
                f.write(b'MThd')
                f.write((6).to_bytes(4, 'big'))
                f.write((0).to_bytes(2, 'big'))
                f.write((1).to_bytes(2, 'big'))
                f.write((96).to_bytes(2, 'big'))
                f.write(b'MTrk')
                f.write((4).to_bytes(4, 'big'))
                f.write(b'\x00\xFF\x2F\x00')
            
            return midi_path
        except Exception:
            return None
