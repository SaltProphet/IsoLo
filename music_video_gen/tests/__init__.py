"""
Test Suite for Music Video Generator

This directory contains tests for all engine modules.

Test Structure:
    test_audio_analysis.py - Tests for audio analysis module
    test_lyric_sync.py - Tests for lyric synchronization
    test_visual_gen.py - Tests for visual generation
    test_utils.py - Tests for utility functions
    test_integration.py - End-to-end integration tests

Running Tests:
    # Run all tests
    pytest

    # Run specific test file
    pytest tests/test_audio_analysis.py

    # Run with coverage
    pytest --cov=engine tests/

TODO: Implement comprehensive test suite
TODO: Add test fixtures for audio/video files
TODO: Add performance benchmarks
"""

# Test configuration
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
