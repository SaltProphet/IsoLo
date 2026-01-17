"""
Workflow Orchestrator for Loop Architect.

This module coordinates the execution of all workflow steps.
"""

import time
from typing import List, Callable, Optional
from workflow_types import (
    WorkflowConfig,
    WorkflowContext,
    WorkflowResult,
    WorkflowStatus,
    ModuleResult,
    StepStatus
)


class WorkflowModule:
    """Base class for workflow modules."""
    
    def get_name(self) -> str:
        """Get module name."""
        raise NotImplementedError
    
    def is_required(self) -> bool:
        """Whether this module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """Process this workflow step."""
        raise NotImplementedError


class WorkflowOrchestrator:
    """
    Orchestrates execution of all workflow modules.
    
    Executes modules in sequence, tracks progress, and handles errors.
    """
    
    def __init__(self, config: WorkflowConfig):
        """
        Initialize orchestrator with configuration.
        
        Args:
            config: Workflow configuration
        """
        self.config = config
        self.modules: List[WorkflowModule] = []
        self.current_step_index = 0
        self.status_callback: Optional[Callable[[WorkflowStatus], None]] = None
        self.steps_completed: List[str] = []
        self.steps_failed: List[str] = []
        
    def register_module(self, module: WorkflowModule) -> None:
        """
        Register a workflow module.
        
        Args:
            module: Module to register
        """
        self.modules.append(module)
        
    def set_status_callback(self, callback: Callable[[WorkflowStatus], None]) -> None:
        """
        Set callback for status updates.
        
        Args:
            callback: Function to call with status updates
        """
        self.status_callback = callback
        
    def _update_status(
        self,
        current_step: str,
        status_message: str,
        is_complete: bool = False,
        has_error: bool = False,
        error_message: Optional[str] = None
    ) -> None:
        """Update and report workflow status."""
        if self.status_callback:
            total_steps = len(self.modules)
            progress = (self.current_step_index / total_steps) * 100 if total_steps > 0 else 0
            
            status = WorkflowStatus(
                current_step=current_step,
                current_step_index=self.current_step_index,
                total_steps=total_steps,
                progress_percent=progress,
                status_message=status_message,
                is_complete=is_complete,
                has_error=has_error,
                error_message=error_message
            )
            self.status_callback(status)
    
    def execute(self, input_file: str, temp_dir: str) -> WorkflowResult:
        """
        Execute the full workflow.
        
        Args:
            input_file: Path to input audio file
            temp_dir: Temporary directory for processing
            
        Returns:
            WorkflowResult with execution details
        """
        start_time = time.time()
        
        # Create workflow context
        context = WorkflowContext(
            input_file=input_file,
            temp_dir=temp_dir,
            config=self.config
        )
        
        # Reset tracking
        self.steps_completed = []
        self.steps_failed = []
        self.current_step_index = 0
        
        # Execute each module
        for i, module in enumerate(self.modules):
            self.current_step_index = i
            module_name = module.get_name()
            
            # Check if module should be skipped
            if not self._should_execute_module(module):
                self._update_status(
                    current_step=module_name,
                    status_message=f"Skipping {module_name} (optional)"
                )
                continue
            
            # Execute module
            self._update_status(
                current_step=module_name,
                status_message=f"Processing {module_name}..."
            )
            
            try:
                result = module.process(context)
                
                if result.success:
                    self.steps_completed.append(module_name)
                    self._update_status(
                        current_step=module_name,
                        status_message=result.message
                    )
                else:
                    self.steps_failed.append(module_name)
                    
                    # If required module fails, abort workflow
                    if module.is_required():
                        execution_time = time.time() - start_time
                        self._update_status(
                            current_step=module_name,
                            status_message=f"Failed: {result.error}",
                            has_error=True,
                            error_message=result.error
                        )
                        
                        return WorkflowResult(
                            success=False,
                            output_zip=None,
                            error=f"Required module '{module_name}' failed: {result.error}",
                            steps_completed=self.steps_completed,
                            steps_failed=self.steps_failed,
                            execution_time=execution_time,
                            generated_files=context.generated_files
                        )
                    else:
                        # Optional module failed, continue
                        self._update_status(
                            current_step=module_name,
                            status_message=f"Optional module failed: {result.error}"
                        )
                        
            except Exception as e:
                self.steps_failed.append(module_name)
                
                # If required module crashes, abort workflow
                if module.is_required():
                    execution_time = time.time() - start_time
                    error_msg = f"Module '{module_name}' crashed: {str(e)}"
                    
                    self._update_status(
                        current_step=module_name,
                        status_message=f"Error: {str(e)}",
                        has_error=True,
                        error_message=error_msg
                    )
                    
                    return WorkflowResult(
                        success=False,
                        output_zip=None,
                        error=error_msg,
                        steps_completed=self.steps_completed,
                        steps_failed=self.steps_failed,
                        execution_time=execution_time,
                        generated_files=context.generated_files
                    )
                else:
                    # Optional module crashed, continue
                    self._update_status(
                        current_step=module_name,
                        status_message=f"Optional module error: {str(e)}"
                    )
        
        # Workflow complete
        execution_time = time.time() - start_time
        
        # Get output ZIP from context (should be set by Exporter module)
        output_zip = context.pack_structure.root_dir + '.zip' if context.pack_structure else None
        
        self._update_status(
            current_step="Complete",
            status_message="Workflow completed successfully",
            is_complete=True
        )
        
        return WorkflowResult(
            success=True,
            output_zip=output_zip,
            error=None,
            steps_completed=self.steps_completed,
            steps_failed=self.steps_failed,
            execution_time=execution_time,
            generated_files=context.generated_files
        )
    
    def _should_execute_module(self, module: WorkflowModule) -> bool:
        """
        Determine if a module should be executed based on config.
        
        Args:
            module: Module to check
            
        Returns:
            True if module should execute
        """
        module_name = module.get_name()
        
        # Check config flags for optional modules
        if 'Lyric' in module_name and not self.config.include_lyrics:
            return False
        if 'Visualizer' in module_name and not self.config.include_visualizer:
            return False
        if 'Video' in module_name and not self.config.include_video:
            return False
        if 'Instrumental' in module_name and not self.config.include_instrumental:
            return False
        if 'MIDI' in module_name and not self.config.include_midi:
            return False
            
        return True
    
    def get_status(self) -> WorkflowStatus:
        """
        Get current workflow status.
        
        Returns:
            Current workflow status
        """
        total_steps = len(self.modules)
        progress = (self.current_step_index / total_steps) * 100 if total_steps > 0 else 0
        
        if self.current_step_index < len(self.modules):
            current_step = self.modules[self.current_step_index].get_name()
        else:
            current_step = "Complete"
        
        return WorkflowStatus(
            current_step=current_step,
            current_step_index=self.current_step_index,
            total_steps=total_steps,
            progress_percent=progress,
            status_message="Processing...",
            is_complete=self.current_step_index >= total_steps,
            has_error=len(self.steps_failed) > 0
        )
