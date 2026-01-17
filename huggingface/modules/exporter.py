"""Exporter module for creating final ZIP package."""

import os
import zipfile
from workflow_types import WorkflowContext, ModuleResult


class Exporter:
    """Creates final ZIP package for download."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Pack Exporter"
    
    def is_required(self) -> bool:
        """This module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Create ZIP file from pack structure.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with ZIP file path
        """
        try:
            if not context.pack_structure:
                return ModuleResult(
                    success=False,
                    message="",
                    error="Pack structure not created"
                )
            
            # Create ZIP file
            zip_path = context.pack_structure.root_dir + '.zip'
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add all files from pack structure
                pack_root = context.pack_structure.root_dir
                
                for root, dirs, files in os.walk(pack_root):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate relative path for archive
                        arcname = os.path.relpath(file_path, os.path.dirname(pack_root))
                        zf.write(file_path, arcname)
            
            # Get ZIP size
            zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            
            context.generated_files.append(zip_path)
            
            return ModuleResult(
                success=True,
                message=f"Pack exported: {os.path.basename(zip_path)} ({zip_size_mb:.1f} MB)",
                data={'zip_path': zip_path, 'size_mb': zip_size_mb}
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Export failed: {str(e)}"
            )
