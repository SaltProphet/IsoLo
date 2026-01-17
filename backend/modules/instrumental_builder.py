"""Instrumental builder module for mixing non-vocal stems."""

import os
import numpy as np
try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

from workflow_types import WorkflowContext, ModuleResult


class InstrumentalBuilder:
    """Builds instrumental track from non-vocal stems."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Instrumental Builder"
    
    def is_required(self) -> bool:
        """This module is optional."""
        return False
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Mix non-vocal stems into instrumental track.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with instrumental audio
        """
        if not SOUNDFILE_AVAILABLE:
            return ModuleResult(
                success=False,
                message="",
                error="soundfile not installed. Run: pip install soundfile"
            )
        
        try:
            if not context.stems:
                return ModuleResult(
                    success=False,
                    message="",
                    error="No stems available to build instrumental"
                )
            
            # Get non-vocal stems
            non_vocal_stems = {
                name: audio for name, audio in context.stems.items()
                if 'vocal' not in name.lower()
            }
            
            if not non_vocal_stems:
                return ModuleResult(
                    success=False,
                    message="",
                    error="No non-vocal stems found"
                )
            
            # Mix stems
            mixed_audio = None
            sample_rate = None
            
            for name, (sr, audio) in non_vocal_stems.items():
                # Convert to float
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32767.0
                
                # Ensure stereo
                if audio.ndim == 1:
                    audio = np.stack([audio, audio], axis=-1)
                
                if mixed_audio is None:
                    mixed_audio = audio.copy()
                    sample_rate = sr
                else:
                    # Add to mix (simple sum, could be more sophisticated)
                    min_len = min(len(mixed_audio), len(audio))
                    mixed_audio[:min_len] += audio[:min_len]
            
            # Normalize to prevent clipping
            peak = np.max(np.abs(mixed_audio))
            if peak > 0:
                mixed_audio = mixed_audio / peak * 0.95  # Leave some headroom
            
            # Apply normalization if configured
            if context.config.normalize_peak < 0:
                target_peak = 10**(context.config.normalize_peak / 20.0)
                current_peak = np.max(np.abs(mixed_audio))
                if current_peak > 0:
                    gain = target_peak / current_peak
                    mixed_audio = np.clip(mixed_audio * gain, -1.0, 1.0)
            
            # Save instrumental
            instrumental_path = os.path.join(
                context.temp_dir,
                f"{context.config.pack_name}_Instrumental.wav"
            )
            sf.write(instrumental_path, mixed_audio, sample_rate, subtype='PCM_16')
            context.generated_files.append(instrumental_path)
            
            # Store in context (convert back to int16 for consistency)
            mixed_int16 = (mixed_audio * 32767).astype(np.int16)
            context.instrumental = (sample_rate, mixed_int16)
            
            return ModuleResult(
                success=True,
                message=f"Instrumental created from {len(non_vocal_stems)} stems"
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Instrumental building failed: {str(e)}"
            )
