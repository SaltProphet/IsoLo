"""Lyric extractor module (STUB - for future Whisper integration)."""

from workflow_types import WorkflowContext, ModuleResult, LyricData


class LyricExtractor:
    """Extracts and syncs lyrics from vocals (STUB)."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Lyric Extractor"
    
    def is_required(self) -> bool:
        """This module is optional."""
        return False
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        STUB: Extract timestamped lyrics using Whisper/STT.
        
        In future implementation, this will:
        1. Run Whisper on vocal stem
        2. Extract word-level timestamps
        3. Format as SRT or JSON
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with stub lyric data
        """
        # Return stub data
        context.lyrics = LyricData(
            text="[Lyrics will be extracted here when Whisper is integrated]",
            timestamps=[]
        )
        
        return ModuleResult(
            success=True,
            message="Lyric extraction (STUB - feature not yet implemented)"
        )
