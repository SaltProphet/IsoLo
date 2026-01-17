"""Input handler module for validating and preparing audio files."""

import os
from workflow_types import WorkflowContext, ModuleResult


class InputHandler:
    """Validates and prepares input audio files."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Input Handler"
    
    def is_required(self) -> bool:
        """This module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Validate input audio file.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult indicating success or failure
        """
        try:
            # Check if file exists
            if not os.path.exists(context.input_file):
                return ModuleResult(
                    success=False,
                    message="",
                    error=f"Input file not found: {context.input_file}"
                )
            
            # Check file size (limit to 100MB)
            file_size = os.path.getsize(context.input_file)
            max_size = 100 * 1024 * 1024  # 100MB
            
            if file_size > max_size:
                return ModuleResult(
                    success=False,
                    message="",
                    error=f"File too large: {file_size / (1024*1024):.1f}MB (max 100MB)"
                )
            
            # Check file extension
            valid_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac']
            _, ext = os.path.splitext(context.input_file)
            
            if ext.lower() not in valid_extensions:
                return ModuleResult(
                    success=False,
                    message="",
                    error=f"Unsupported file format: {ext} (supported: {', '.join(valid_extensions)})"
                )
            
            # Create temp directory if needed
            os.makedirs(context.temp_dir, exist_ok=True)
            
            return ModuleResult(
                success=True,
                message=f"Input validated: {os.path.basename(context.input_file)}"
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Input validation failed: {str(e)}"
            )
