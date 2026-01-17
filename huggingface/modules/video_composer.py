"""Video composer module (STUB - for future ffmpeg/moviepy integration)."""

from workflow_types import WorkflowContext, ModuleResult


class VideoComposer:
    """Composes video with visuals and lyrics (STUB)."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Video Composer"
    
    def is_required(self) -> bool:
        """This module is optional."""
        return False
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        STUB: Overlay visuals/lyrics and render video.
        
        In future implementation, this will:
        1. Take visualizer output
        2. Overlay timestamped lyrics
        3. Render final video with ffmpeg/moviepy
        4. Export in various formats (MP4, WebM, etc.)
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with stub video path
        """
        # Return stub
        context.video = None
        
        return ModuleResult(
            success=True,
            message="Video composition (STUB - feature not yet implemented)"
        )
