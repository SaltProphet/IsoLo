#!/usr/bin/env python3
"""
Example usage script for SAM Audio integration in Loop Architect.

This demonstrates various ways to use the SAM Audio functionality
to isolate named sounds from audio files.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def example_basic_usage():
    """Basic usage example: Isolate a single sound."""
    print("\n" + "="*70)
    print("Example 1: Basic Single Sound Isolation")
    print("="*70)
    
    from sam_audio_integration import SAMAudioSeparator
    
    # Create a separator instance
    separator = SAMAudioSeparator(model_type="large")
    
    # Check if SAM Audio is available
    if not separator.is_available():
        print("⚠ SAM Audio is not installed. Install with:")
        print("  pip install sam-audio-infer")
        print("\nThis example will only show the API usage pattern.")
        return
    
    print("\nIsolating lead vocals from a song...")
    print("Code:")
    print("  sr, audio = separator.separate_by_description(")
    print("      'song.mp3',")
    print("      'lead vocals',")
    print("      output_path='vocals_isolated.wav'")
    print("  )")
    
    # Uncomment to actually run if you have an audio file:
    # sr, audio = separator.separate_by_description(
    #     "song.mp3",
    #     "lead vocals",
    #     output_path="vocals_isolated.wav"
    # )
    # print(f"\n✓ Isolated vocals saved to vocals_isolated.wav")
    # print(f"  Sample rate: {sr} Hz")
    # print(f"  Audio shape: {audio.shape}")


def example_multiple_sounds():
    """Example: Isolate multiple sounds from the same file."""
    print("\n" + "="*70)
    print("Example 2: Isolate Multiple Sounds")
    print("="*70)
    
    from sam_audio_integration import SAMAudioSeparator
    
    separator = SAMAudioSeparator()
    
    if not separator.is_available():
        print("⚠ SAM Audio is not installed.")
        print("\nThis example will only show the API usage pattern.")
        return
    
    print("\nIsolating multiple instruments from a band recording...")
    print("Code:")
    print("  results = separator.separate_multiple(")
    print("      'band_performance.wav',")
    print("      descriptions=[")
    print("          'lead vocals',")
    print("          'electric guitar',")
    print("          'bass guitar',")
    print("          'drum kit'")
    print("      ],")
    print("      output_dir='isolated_sounds/'")
    print("  )")
    
    # Uncomment to actually run if you have an audio file:
    # results = separator.separate_multiple(
    #     "band_performance.wav",
    #     descriptions=[
    #         "lead vocals",
    #         "electric guitar",
    #         "bass guitar",
    #         "drum kit"
    #     ],
    #     output_dir="isolated_sounds/"
    # )
    #
    # print(f"\n✓ Isolated {len(results)} sounds:")
    # for sound_name, (sr, audio) in results.items():
    #     print(f"  - {sound_name}: {audio.shape}")


def example_convenience_function():
    """Example: Use the high-level convenience function."""
    print("\n" + "="*70)
    print("Example 3: High-Level Convenience Function")
    print("="*70)
    
    from sam_audio_integration import create_named_stem_separations
    
    print("\nQuick and easy multi-sound isolation...")
    print("Code:")
    print("  results = create_named_stem_separations(")
    print("      'song.mp3',")
    print("      prompts=['vocals', 'guitar', 'drums', 'bass']")
    print("  )")
    print("  ")
    print("  for name, (sr, audio) in results.items():")
    print("      print(f'{name}: {audio.shape}')")
    
    # Uncomment to actually run if you have an audio file:
    # results = create_named_stem_separations(
    #     "song.mp3",
    #     prompts=["vocals", "guitar", "drums", "bass"]
    # )
    #
    # for name, (sr, audio) in results.items():
    #     print(f"  {name}: {audio.shape}")


def example_app_integration():
    """Example: Use through the main app.py integration."""
    print("\n" + "="*70)
    print("Example 4: Integration with Loop Architect")
    print("="*70)
    
    print("\nUsing SAM Audio through the Loop Architect app...")
    print("Code:")
    print("  from app import separate_stems_with_sam_audio")
    print("  ")
    print("  stems_dict, bpm, key, recs = separate_stems_with_sam_audio(")
    print("      'song.mp3',")
    print("      use_sam_audio=True,")
    print("      sam_prompts=['lead vocals', 'electric guitar', 'bass', 'drums']")
    print("  )")
    print("  ")
    print("  print(f'BPM: {bpm}, Key: {key}')")
    print("  print(f'Isolated {len(stems_dict)} sounds')")
    
    # Uncomment to actually run if you have an audio file:
    # from app import separate_stems_with_sam_audio
    #
    # stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
    #     "song.mp3",
    #     use_sam_audio=True,
    #     sam_prompts=["lead vocals", "electric guitar", "bass", "drums"]
    # )
    #
    # print(f"\n✓ Detected BPM: {bpm}")
    # print(f"  Key: {key}")
    # print(f"  Harmonic recs: {recs}")
    # print(f"  Isolated sounds: {list(stems_dict.keys())}")


def example_creative_sounds():
    """Example: Isolate creative/unusual sounds."""
    print("\n" + "="*70)
    print("Example 5: Creative Sound Isolation")
    print("="*70)
    
    from sam_audio_integration import SAMAudioSeparator
    
    print("\nSAM Audio can isolate ANY sound you can name!")
    print("\nMusical examples:")
    print("  - 'saxophone solo'")
    print("  - 'piano melody'")
    print("  - 'string section'")
    print("  - 'crowd applause'")
    
    print("\nEnvironmental examples:")
    print("  - 'rain sounds'")
    print("  - 'thunder'")
    print("  - 'bird chirping'")
    print("  - 'car engine'")
    
    print("\nVocal examples:")
    print("  - 'male voice'")
    print("  - 'female voice'")
    print("  - 'child speaking'")
    print("  - 'laughter'")
    
    print("\nSound effects examples:")
    print("  - 'door slam'")
    print("  - 'glass breaking'")
    print("  - 'phone ringing'")
    print("  - 'footsteps'")
    
    print("\nCode example:")
    print("  separator = SAMAudioSeparator()")
    print("  ")
    print("  # Isolate applause from a live recording")
    print("  sr, applause = separator.separate_by_description(")
    print("      'live_concert.wav',")
    print("      'crowd applause'")
    print("  )")
    print("  ")
    print("  # Isolate rain from a nature recording")
    print("  sr, rain = separator.separate_by_description(")
    print("      'nature_sounds.wav',")
    print("      'rain sounds'")
    print("  )")


def example_workflow():
    """Example: Complete workflow for music production."""
    print("\n" + "="*70)
    print("Example 6: Complete Music Production Workflow")
    print("="*70)
    
    print("\nStep 1: Analyze and isolate main elements")
    print("Code:")
    print("  from app import separate_stems_with_sam_audio")
    print("  ")
    print("  # Get traditional stems for main elements")
    print("  stems, bpm, key, recs = separate_stems_with_sam_audio(")
    print("      'original_song.mp3',")
    print("      use_sam_audio=True,")
    print("      sam_prompts=['lead vocals', 'backing vocals', 'guitar', 'bass', 'drums']")
    print("  )")
    
    print("\nStep 2: Further isolate specific elements")
    print("Code:")
    print("  from sam_audio_integration import SAMAudioSeparator")
    print("  ")
    print("  separator = SAMAudioSeparator()")
    print("  ")
    print("  # From the guitar stem, isolate lead vs rhythm")
    print("  sr, lead_guitar = separator.separate_by_description(")
    print("      'guitar.wav',")
    print("      'lead guitar solo'")
    print("  )")
    print("  ")
    print("  sr, rhythm_guitar = separator.separate_by_description(")
    print("      'guitar.wav',")
    print("      'rhythm guitar chords'")
    print("  )")
    
    print("\nStep 3: Process each isolated sound")
    print("  - Apply effects to lead vocals")
    print("  - EQ the guitar solo")
    print("  - Compress the drums")
    print("  - Add reverb to backing vocals")
    
    print("\nStep 4: Remix with Loop Architect tools")
    print("  - Slice stems into loops")
    print("  - Apply key and BPM adjustments")
    print("  - Export for DAW")


def main():
    """Run all examples."""
    print("="*70)
    print("SAM Audio Integration - Usage Examples")
    print("="*70)
    print("\nThese examples show how to use SAM Audio in Loop Architect")
    print("to isolate any named sound from audio files.")
    print("\nNote: To actually run these examples, you need to:")
    print("  1. Install SAM Audio: pip install sam-audio-infer")
    print("  2. Have audio files to process")
    print("  3. Uncomment the actual function calls in the code")
    
    example_basic_usage()
    example_multiple_sounds()
    example_convenience_function()
    example_app_integration()
    example_creative_sounds()
    example_workflow()
    
    print("\n" + "="*70)
    print("For more information, see SAM_AUDIO_INTEGRATION.md")
    print("="*70)


if __name__ == "__main__":
    main()
