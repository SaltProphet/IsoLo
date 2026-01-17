#!/usr/bin/env python3
"""
Example Usage Script for Sample Pack Generator Agents

This script demonstrates how to use the modular agent system to create
a sample pack from an audio file. Each agent is used independently to
show the modular nature of the system.

Usage:
    python examples/sample_pack_generator_example.py

Note: This is a demonstration of the agent interfaces. The actual processing
      logic is marked as TODO and will be implemented in future phases.
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.engine.agents import (
    StemSeparationAgent,
    VocalBuilderAgent,
    LoopGeneratorAgent,
    LyricExtractionAgent,
    VideoExportAgent,
    PackExportAgent,
    UIAgent
)


def example_basic_agent_usage():
    """
    Example 1: Basic agent usage - single agent processing
    """
    print("=" * 70)
    print("Example 1: Basic Agent Usage")
    print("=" * 70)
    
    # Initialize agent with configuration
    agent = StemSeparationAgent(config={
        "model": "htdemucs",
        "device": "cpu"
    })
    
    print(f"\nAgent Name: {agent.name}")
    print(f"Agent Version: {agent.version}")
    
    # Process audio (stub - will return placeholder data)
    result = agent.process({
        "audio_path": "/path/to/song.mp3",
        "output_dir": "/tmp/output"
    })
    
    print(f"\nResult Status: {result['status']}")
    print(f"Result Message: {result['message']}")
    print(f"Agent: {result['agent']}")
    print(f"Timestamp: {result['timestamp']}")
    
    if result['status'] == 'success':
        print("\nGenerated Data:")
        for key, value in result['data'].items():
            print(f"  {key}: {value}")


def example_pipeline_usage():
    """
    Example 2: Pipeline usage - chaining multiple agents
    """
    print("\n" + "=" * 70)
    print("Example 2: Pipeline Usage - Sequential Agent Processing")
    print("=" * 70)
    
    # Step 1: Stem Separation
    print("\n[Step 1] Stem Separation & Analysis")
    print("-" * 70)
    stem_agent = StemSeparationAgent()
    stem_result = stem_agent.process({
        "audio_path": "/path/to/song.mp3",
        "output_dir": "/tmp/output/stems"
    })
    print(f"Status: {stem_result['status']}")
    print(f"Stems: {list(stem_result['data']['stems'].keys())}")
    
    # Step 2: Build Vocal Versions
    print("\n[Step 2] Building Instrumental/Karaoke/Acapella")
    print("-" * 70)
    vocal_agent = VocalBuilderAgent(config={"normalize_db": -3.0})
    vocal_result = vocal_agent.process({
        "stems": stem_result['data']['stems'],
        "manifest_path": stem_result['data']['manifest_path'],
        "output_dir": "/tmp/output/mixes"
    })
    print(f"Status: {vocal_result['status']}")
    if vocal_result['status'] == 'success':
        print(f"Generated:")
        for key, value in vocal_result['data'].items():
            print(f"  {key}: {value}")
    
    # Step 3: Generate Loops
    print("\n[Step 3] Generating Loops & One-shots")
    print("-" * 70)
    loop_agent = LoopGeneratorAgent(config={
        "min_loop_bars": 4,
        "max_loop_bars": 8
    })
    loop_result = loop_agent.process({
        "stems": stem_result['data']['stems'],
        "manifest_path": stem_result['data']['manifest_path'],
        "output_dir": "/tmp/output/loops"
    })
    print(f"Status: {loop_result['status']}")
    
    # Step 4: Extract Lyrics
    print("\n[Step 4] Extracting Lyrics")
    print("-" * 70)
    lyric_agent = LyricExtractionAgent(config={"model": "base"})
    lyric_result = lyric_agent.process({
        "vocals_path": stem_result['data']['stems']['vocals'],
        "manifest_path": stem_result['data']['manifest_path'],
        "output_dir": "/tmp/output/lyrics"
    })
    print(f"Status: {lyric_result['status']}")
    
    # Step 5: Pack Export
    print("\n[Step 5] Organizing & Exporting Pack")
    print("-" * 70)
    pack_agent = PackExportAgent(config={"include_readme": True})
    pack_result = pack_agent.process({
        "pack_name": "My Sample Pack",
        "files": {
            "stems": list(stem_result['data']['stems'].values()),
            "loops": loop_result['data']['loops'] if loop_result['status'] == 'success' else [],
            "oneshots": loop_result['data']['oneshots'] if loop_result['status'] == 'success' else [],
        },
        "metadata": {
            "artist": "Example Artist",
            "bpm": 120,
            "key": "C Major"
        },
        "output_dir": "/tmp/output/pack"
    })
    print(f"Status: {pack_result['status']}")


def example_ui_orchestration():
    """
    Example 3: UI Agent - High-level orchestration
    """
    print("\n" + "=" * 70)
    print("Example 3: UI Agent Orchestration")
    print("=" * 70)
    
    # Initialize UI agent
    ui_agent = UIAgent(config={
        "theme": "default",
        "enable_preview": True
    })
    
    # Register other agents
    ui_agent.register_agent("stem_separation", StemSeparationAgent())
    ui_agent.register_agent("vocal_builder", VocalBuilderAgent())
    ui_agent.register_agent("loop_generator", LoopGeneratorAgent())
    ui_agent.register_agent("lyric_extraction", LyricExtractionAgent())
    ui_agent.register_agent("pack_export", PackExportAgent())
    
    print(f"\nRegistered {len(ui_agent.agents)} agents")
    print("Agents:", list(ui_agent.agents.keys()))
    
    # Process full pipeline (stub - returns placeholder)
    result = ui_agent.process({
        "audio_file": "/path/to/song.mp3",
        "pack_name": "My Sample Pack",
        "artist_name": "Example Artist",
        "genre": "Electronic"
    })
    
    print(f"\nPipeline Status: {result['status']}")
    print(f"Message: {result['message']}")


def example_agent_configuration():
    """
    Example 4: Agent configuration and customization
    """
    print("\n" + "=" * 70)
    print("Example 4: Agent Configuration")
    print("=" * 70)
    
    # Different configurations for different use cases
    configs = {
        "High Quality": {
            "StemSeparation": {"model": "htdemucs_ft", "device": "cuda"},
            "VocalBuilder": {"normalize_db": -3.0, "apply_effects": True},
            "LoopGenerator": {"min_loop_bars": 8, "generate_midi": True},
            "LyricExtraction": {"model": "large", "word_level": True},
            "VideoExport": {"style": "spectrum", "fps": 60, "resolution": (3840, 2160)},
            "PackExport": {"compression_level": 9}
        },
        "Fast Processing": {
            "StemSeparation": {"model": "htdemucs", "device": "cpu", "shifts": 1},
            "VocalBuilder": {"normalize_db": -3.0, "apply_effects": False},
            "LoopGenerator": {"min_loop_bars": 4, "generate_midi": False},
            "LyricExtraction": {"model": "tiny", "word_level": False},
            "VideoExport": {"style": "waveform", "fps": 30, "resolution": (1920, 1080)},
            "PackExport": {"compression_level": 6}
        }
    }
    
    for preset_name, preset_config in configs.items():
        print(f"\n{preset_name} Preset:")
        print("-" * 70)
        for agent_name, agent_config in preset_config.items():
            print(f"  {agent_name}:")
            for key, value in agent_config.items():
                print(f"    {key}: {value}")


def example_error_handling():
    """
    Example 5: Error handling and validation
    """
    print("\n" + "=" * 70)
    print("Example 5: Error Handling")
    print("=" * 70)
    
    agent = StemSeparationAgent()
    
    # Test invalid input (missing required fields)
    print("\nTest 1: Missing required input")
    print("-" * 70)
    result = agent.process({
        "audio_path": "/path/to/song.mp3"
        # Missing 'output_dir'
    })
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    # Test validation
    print("\nTest 2: Input validation")
    print("-" * 70)
    is_valid = agent.validate_input(
        {"audio_path": "test.mp3"},
        ["audio_path", "output_dir"]
    )
    print(f"Validation result: {is_valid}")
    
    # Test configuration
    print("\nTest 3: Configuration access")
    print("-" * 70)
    custom_agent = StemSeparationAgent(config={"model": "htdemucs_ft"})
    model = custom_agent.get_config_value("model", "default")
    device = custom_agent.get_config_value("device", "cpu")
    print(f"Model: {model}")
    print(f"Device: {device} (default value)")


def main():
    """
    Main function - run all examples
    """
    print("\n" + "=" * 70)
    print("Sample Pack Generator - Agent Examples")
    print("=" * 70)
    print("\nThese examples demonstrate the agent interfaces.")
    print("Actual processing logic is marked as TODO for future implementation.")
    print()
    
    # Run examples
    example_basic_agent_usage()
    example_pipeline_usage()
    example_ui_orchestration()
    example_agent_configuration()
    example_error_handling()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Implement TODO sections in each agent")
    print("2. Add actual processing logic")
    print("3. Integrate with Gradio UI")
    print("4. Add comprehensive tests")
    print()


if __name__ == "__main__":
    main()
