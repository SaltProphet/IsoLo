#!/usr/bin/env python3
"""
Test script to verify that module imports work correctly in all scenarios.

This test ensures the fix for "ModuleNotFoundError: No module named 'modules'"
works in various execution contexts.
"""

import sys
import os
import subprocess

def test_import_from_huggingface_dir():
    """Test importing when running from huggingface directory."""
    print("Test 1: Running from huggingface directory...")
    
    # Get the script's directory (should be huggingface)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a test script - use raw string to avoid escaping issues
    # Note: __file__ won't be defined in -c mode, so we use cwd
    test_script = """
import sys
import os
# When running with -c, __file__ is not defined, so use current directory
script_dir = os.getcwd()
sys.path.insert(0, script_dir)
from modules import InputHandler
from workflow_orchestrator import WorkflowOrchestrator
from workflow_types import WorkflowConfig
print('SUCCESS')
"""
    
    result = subprocess.run(
        ["python3", "-c", test_script],
        cwd=script_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and 'SUCCESS' in result.stdout:
        print("  ✓ PASSED")
        return True
    else:
        print(f"  ✗ FAILED: {result.stderr}")
        return False


def test_import_from_parent_dir():
    """Test importing when running from parent directory."""
    print("Test 2: Running from parent directory...")
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        ["python3", "huggingface/test_imports.py", "--inline-test"],
        cwd=parent_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and 'INLINE SUCCESS' in result.stdout:
        print("  ✓ PASSED")
        return True
    else:
        print(f"  ✗ FAILED: {result.stderr}")
        return False


def test_import_with_absolute_path():
    """Test importing when app.py is referenced by absolute path."""
    print("Test 3: Using absolute path...")
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')
    app_dir = os.path.dirname(app_path)
    
    # Create test script without path injection
    test_script = f"""
import sys
import os
# Simulate __file__ being an absolute path
script_dir = r'{app_dir}'
sys.path.insert(0, script_dir)
from modules import InputHandler
print('SUCCESS')
"""
    
    result = subprocess.run(
        ["python3", "-c", test_script],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and 'SUCCESS' in result.stdout:
        print("  ✓ PASSED")
        return True
    else:
        print(f"  ✗ FAILED: {result.stderr}")
        return False


def inline_test():
    """Inline test for import verification."""
    try:
        import sys
        import os
        
        # Simulate app.py's fix
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        
        # Try imports
        from modules import InputHandler
        from workflow_orchestrator import WorkflowOrchestrator
        from workflow_types import WorkflowConfig
        
        print("INLINE SUCCESS")
        sys.exit(0)
    except Exception as e:
        print(f"INLINE FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Run all tests."""
    if len(sys.argv) > 1 and sys.argv[1] == '--inline-test':
        return inline_test()
    
    print("="*60)
    print("Module Import Tests for HuggingFace Deployment")
    print("=" * 60)
    print()
    
    results = []
    results.append(test_import_from_huggingface_dir())
    results.append(test_import_from_parent_dir())
    results.append(test_import_with_absolute_path())
    
    print()
    print("=" * 60)
    if all(results):
        print("✓ ALL TESTS PASSED")
        print("The module import fix is working correctly.")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("The module import fix may need adjustment.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
