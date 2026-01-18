#!/usr/bin/env python3
"""Quick test to verify all app.py imports work."""

import sys
import os

# Replicate the fix from app.py
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Test all imports that app.py uses
print('Testing imports from app.py...')

from modules import (
    InputHandler, AudioAnalyzer, InstrumentalBuilder, Slicer,
    LyricExtractor, Visualizer, VideoComposer, MetadataTagger,
    PackBuilder, Exporter
)
print('✓ modules imports successful')

from workflow_orchestrator import WorkflowOrchestrator
print('✓ workflow_orchestrator import successful')

from workflow_types import WorkflowConfig, WorkflowContext
print('✓ workflow_types imports successful')

print()
print('SUCCESS: All imports working correctly!')
print('The module import fix in app.py is functioning properly.')
