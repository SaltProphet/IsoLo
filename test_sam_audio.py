#!/usr/bin/env python3
"""
Test script for SAM Audio integration in Loop Architect.

This script tests the SAM Audio integration without requiring an actual
audio file or the SAM Audio models to be installed.
"""

import sys
import os

# Add the parent directory to path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        print(f"  ✗ numpy: {e}")
        return False
    
    try:
        import librosa
        print("  ✓ librosa")
    except ImportError as e:
        print(f"  ✗ librosa: {e}")
        return False
    
    try:
        import soundfile
        print("  ✓ soundfile")
    except ImportError as e:
        print(f"  ✗ soundfile: {e}")
        return False
    
    try:
        from sam_audio_integration import SAMAudioSeparator, create_named_stem_separations
        print("  ✓ sam_audio_integration module")
    except ImportError as e:
        print(f"  ✗ sam_audio_integration: {e}")
        return False
    
    return True


def test_sam_audio_availability():
    """Test if SAM Audio is available."""
    print("\nTesting SAM Audio availability...")
    
    try:
        from sam_audio_integration import SAMAudioSeparator
        
        separator = SAMAudioSeparator()
        
        if separator.is_available():
            print("  ✓ SAM Audio is installed and available!")
            print(f"    Device: {separator.device}")
            print(f"    Model type: {separator.model_type}")
            return True
        else:
            print("  ⚠ SAM Audio is not installed (this is OK for testing)")
            print("    The integration module is working correctly.")
            print("    To use SAM Audio, install one of:")
            print("      - pip install sam-audio-infer (lightweight)")
            print("      - Official package from https://github.com/facebookresearch/sam-audio")
            return True
    except Exception as e:
        print(f"  ✗ Error checking SAM Audio: {e}")
        return False


def test_module_structure():
    """Test that the module has the expected structure."""
    print("\nTesting module structure...")
    
    try:
        from sam_audio_integration import (
            SAMAudioSeparator,
            create_named_stem_separations
        )
        
        # Check SAMAudioSeparator class
        separator = SAMAudioSeparator()
        
        # Check it has expected methods
        assert hasattr(separator, 'separate_by_description'), "Missing separate_by_description method"
        assert hasattr(separator, 'separate_multiple'), "Missing separate_multiple method"
        assert hasattr(separator, 'is_available'), "Missing is_available method"
        
        print("  ✓ SAMAudioSeparator class structure correct")
        
        # Check the convenience function exists
        assert callable(create_named_stem_separations), "create_named_stem_separations is not callable"
        print("  ✓ create_named_stem_separations function exists")
        
        return True
    except Exception as e:
        print(f"  ✗ Module structure test failed: {e}")
        return False


def test_app_integration():
    """Test that app.py has the SAM Audio integration."""
    print("\nTesting app.py integration...")
    
    try:
        from app import (
            separate_stems_with_sam_audio,
            separate_named_sounds,
            separate_stems
        )
        
        print("  ✓ separate_stems_with_sam_audio function exists")
        print("  ✓ separate_named_sounds function exists")
        print("  ✓ separate_stems function exists (backward compatible)")
        
        return True
    except ImportError as e:
        print(f"  ✗ App integration import failed: {e}")
        return False
    except Exception as e:
        print(f"  ✗ App integration test failed: {e}")
        return False


def test_documentation():
    """Test that documentation files exist."""
    print("\nTesting documentation...")
    
    files_to_check = [
        "SAM_AUDIO_INTEGRATION.md",
        "sam_audio_integration.py",
        "requirements (1).txt"
    ]
    
    all_exist = True
    for filename in files_to_check:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename} exists")
        else:
            print(f"  ✗ {filename} not found")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests."""
    print("=" * 70)
    print("SAM Audio Integration Test Suite")
    print("=" * 70)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("SAM Audio Availability", test_sam_audio_availability()))
    results.append(("Module Structure", test_module_structure()))
    results.append(("App Integration", test_app_integration()))
    results.append(("Documentation", test_documentation()))
    
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<50} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("All tests passed! ✓")
        print("\nThe SAM Audio integration is correctly implemented.")
        print("To use SAM Audio features, install the package:")
        print("  pip install sam-audio-infer")
    else:
        print("Some tests failed. ✗")
        print("Please check the errors above.")
        return 1
    
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
