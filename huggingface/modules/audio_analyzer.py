"""Audio analyzer module for BPM, key, and time signature detection."""

import numpy as np
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

from workflow_types import WorkflowContext, ModuleResult


# Key to Camelot mapping
KEY_TO_CAMELOT = {
    "C Maj": "8B", "G Maj": "9B", "D Maj": "10B", "A Maj": "11B", "E Maj": "12B",
    "B Maj": "1B", "F# Maj": "2B", "Db Maj": "3B", "Ab Maj": "4B", "Eb Maj": "5B",
    "Bb Maj": "6B", "F Maj": "7B",
    "A Min": "8A", "E Min": "9A", "B Min": "10A", "F# Min": "11A", "C# Min": "12A",
    "G# Min": "1A", "D# Min": "2A", "Bb Min": "3A", "F Min": "4A", "C Min": "5A",
    "G Min": "6A", "D Min": "7A",
}

CAMELOT_TO_KEY = {v: k for k, v in KEY_TO_CAMELOT.items()}


class AudioAnalyzer:
    """Analyzes audio for BPM, key, and time signature."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Audio Analyzer"
    
    def is_required(self) -> bool:
        """This module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Detect BPM, key, and time signature.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with analysis results
        """
        if not LIBROSA_AVAILABLE:
            return ModuleResult(
                success=False,
                message="",
                error="librosa not installed. Run: pip install librosa"
            )
        
        try:
            # Load audio
            y, sr = librosa.load(context.input_file, sr=None, mono=True)
            
            # Detect BPM
            if context.config.manual_bpm:
                bpm = context.config.manual_bpm
            else:
                tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
                bpm = 120.0 if tempo is None or tempo.size == 0 or tempo[0] == 0 else float(np.round(tempo[0]))
            
            context.bpm = bpm
            
            # Detect key
            key = self._detect_key(y, sr)
            context.key = key
            
            # Get harmonic recommendations
            context.harmonic_recs = self._get_harmonic_recommendations(key)
            
            # Set time signature from config
            context.time_signature = context.config.time_signature
            
            return ModuleResult(
                success=True,
                message=f"Analysis complete: {bpm:.1f} BPM, {key}, {context.time_signature}",
                data={
                    'bpm': bpm,
                    'key': key,
                    'harmonic_recs': context.harmonic_recs,
                    'time_signature': context.time_signature
                }
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Audio analysis failed: {str(e)}"
            )
    
    def _detect_key(self, y: np.ndarray, sr: int) -> str:
        """Detect musical key using chromagram analysis."""
        try:
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            chroma_sums = np.sum(chroma, axis=1)
            
            if np.sum(chroma_sums) == 0:
                return "Unknown Key"
            
            chroma_norm = chroma_sums / np.sum(chroma_sums)
            
            # Krumhansl-Schmuckler key-finding templates
            major_template = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
            minor_template = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
            
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
                
        except Exception:
            return "Unknown Key"
    
    def _get_harmonic_recommendations(self, key_str: str) -> str:
        """Get harmonically compatible keys based on Camelot wheel."""
        code = KEY_TO_CAMELOT.get(key_str, "N/A")
        if code == "N/A":
            return "N/A (Key not recognized)"
        
        try:
            num = int(code[:-1])
            mode = code[-1]
            opposite_mode = 'B' if mode == 'A' else 'A'
            num_plus_one = (num % 12) + 1
            num_minus_one = 12 if num == 1 else num - 1
            
            recs_codes = [
                f"{num}{opposite_mode}",
                f"{num_plus_one}{mode}",
                f"{num_minus_one}{mode}"
            ]
            
            rec_keys = [f"{CAMELOT_TO_KEY.get(r_code, f'Code {r_code}')} ({r_code})" for r_code in recs_codes]
            return " | ".join(rec_keys)
        except Exception:
            return "N/A (Error calculating recommendations)"
