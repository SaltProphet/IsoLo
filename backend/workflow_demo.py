"""
Demo script for Loop Architect workflow.

This demonstrates the full workflow integration from input to final pack export.
"""

import sys
import os
import tempfile

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from workflow_orchestrator import WorkflowOrchestrator, WorkflowModule
from workflow_types import WorkflowConfig, WorkflowStatus
from modules import (
    InputHandler,
    AudioAnalyzer,
    InstrumentalBuilder,
    Slicer,
    LyricExtractor,
    Visualizer,
    VideoComposer,
    MetadataTagger,
    PackBuilder,
    Exporter
)


def status_callback(status: WorkflowStatus) -> None:
    """Print workflow status updates."""
    progress_bar = '█' * int(status.progress_percent / 5) + '░' * (20 - int(status.progress_percent / 5))
    print(f"\r[{progress_bar}] {status.progress_percent:.1f}% - {status.current_step}: {status.status_message}", end='')
    
    if status.is_complete:
        print()  # New line after completion
    
    if status.has_error:
        print(f"\n❌ Error: {status.error_message}")


def create_workflow(config: WorkflowConfig) -> WorkflowOrchestrator:
    """
    Create and configure workflow orchestrator.
    
    Args:
        config: Workflow configuration
        
    Returns:
        Configured WorkflowOrchestrator
    """
    orchestrator = WorkflowOrchestrator(config)
    
    # Register modules in execution order
    orchestrator.register_module(InputHandler())
    
    # Note: Stem separation would go here, but it's handled separately
    # in app.py's separate_stems function for now
    
    orchestrator.register_module(AudioAnalyzer())
    orchestrator.register_module(InstrumentalBuilder())
    orchestrator.register_module(Slicer())
    orchestrator.register_module(LyricExtractor())
    orchestrator.register_module(Visualizer())
    orchestrator.register_module(VideoComposer())
    orchestrator.register_module(MetadataTagger())
    orchestrator.register_module(PackBuilder())
    orchestrator.register_module(Exporter())
    
    # Set status callback
    orchestrator.set_status_callback(status_callback)
    
    return orchestrator


def demo_workflow(input_file: str, config: WorkflowConfig = None) -> None:
    """
    Run a demo of the full workflow.
    
    Args:
        input_file: Path to input audio file
        config: Optional workflow configuration (uses defaults if None)
    """
    if config is None:
        config = WorkflowConfig(
            pack_name="Demo_Pack",
            separation_mode='traditional',
            loop_type='4-bar',
            include_instrumental=True,
            include_midi=True,
            include_lyrics=False,
            include_visualizer=False,
            include_video=False
        )
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    
    print("🎵 Loop Architect Workflow Demo")
    print("=" * 50)
    print(f"Input: {os.path.basename(input_file)}")
    print(f"Config: {config.separation_mode} mode, {config.loop_type} loops")
    print("=" * 50)
    print()
    
    # Create workflow
    orchestrator = create_workflow(config)
    
    # Execute workflow
    # Note: In production, stems would be passed in context after separation
    # For now, this is a stub demonstration
    result = orchestrator.execute(input_file, temp_dir)
    
    print()
    print("=" * 50)
    
    if result.success:
        print("✅ Workflow completed successfully!")
        print(f"⏱️  Execution time: {result.execution_time:.2f}s")
        print(f"📦 Output ZIP: {result.output_zip}")
        print(f"📁 Generated files: {len(result.generated_files)}")
        print(f"✓ Completed steps: {', '.join(result.steps_completed)}")
        
        if result.steps_failed:
            print(f"⚠️  Failed steps: {', '.join(result.steps_failed)}")
    else:
        print("❌ Workflow failed!")
        print(f"Error: {result.error}")
        print(f"✓ Completed steps: {', '.join(result.steps_completed)}")
        print(f"✗ Failed steps: {', '.join(result.steps_failed)}")
    
    print("=" * 50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Loop Architect Workflow Demo')
    parser.add_argument('input_file', help='Path to input audio file')
    parser.add_argument('--pack-name', default='Demo_Pack', help='Name for the output pack')
    parser.add_argument('--loop-type', choices=['1-bar', '2-bar', '4-bar', 'one-shots'], 
                       default='4-bar', help='Loop type')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File not found: {args.input_file}")
        sys.exit(1)
    
    config = WorkflowConfig(
        pack_name=args.pack_name,
        loop_type=args.loop_type,
        separation_mode='traditional'
    )
    
    demo_workflow(args.input_file, config)
