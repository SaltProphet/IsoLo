"""Metadata tagger module for adding BPM/key tags to audio files."""

import os
from workflow_types import WorkflowContext, ModuleResult

try:
    from mutagen.wave import WAVE
    from mutagen.id3 import ID3, TIT2, TPE1, COMM, TBPM
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False


class MetadataTagger:
    """Tags audio files with metadata."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Metadata Tagger"
    
    def is_required(self) -> bool:
        """This module is optional but recommended."""
        return False
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Add metadata tags to all generated audio files.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult indicating success
        """
        if not MUTAGEN_AVAILABLE:
            # Not critical, continue without tagging
            return ModuleResult(
                success=True,
                message="Metadata tagging skipped (mutagen not installed)"
            )
        
        try:
            tagged_count = 0
            
            # Tag all sliced files
            for file_path in context.sliced_files:
                if file_path.endswith('.wav'):
                    self._tag_wav_file(file_path, context)
                    tagged_count += 1
            
            # Tag instrumental if present
            if context.instrumental and context.config.include_instrumental:
                instrumental_path = os.path.join(
                    context.temp_dir,
                    f"{context.config.pack_name}_Instrumental.wav"
                )
                if os.path.exists(instrumental_path):
                    self._tag_wav_file(instrumental_path, context)
                    tagged_count += 1
            
            return ModuleResult(
                success=True,
                message=f"Tagged {tagged_count} audio files"
            )
            
        except Exception as e:
            # Non-critical failure
            return ModuleResult(
                success=True,
                message=f"Metadata tagging partially failed: {str(e)}"
            )
    
    def _tag_wav_file(self, file_path: str, context: WorkflowContext) -> None:
        """Tag a single WAV file with metadata."""
        try:
            audio = WAVE(file_path)
            
            # Add ID3 tags to WAV
            if audio.tags is None:
                audio.add_tags()
            
            # Add BPM
            audio.tags.add(TBPM(encoding=3, text=str(int(context.bpm))))
            
            # Add title
            filename = os.path.basename(file_path)
            audio.tags.add(TIT2(encoding=3, text=filename))
            
            # Add artist if provided
            if context.config.artist_name:
                audio.tags.add(TPE1(encoding=3, text=context.config.artist_name))
            
            # Add comment with key
            comment = f"Key: {context.key} | BPM: {int(context.bpm)} | {context.time_signature}"
            audio.tags.add(COMM(encoding=3, lang='eng', desc='', text=comment))
            
            audio.save()
            
        except Exception:
            # Silently fail for individual files
            pass
