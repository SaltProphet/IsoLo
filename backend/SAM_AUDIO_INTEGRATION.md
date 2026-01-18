# SAM Audio Integration Guide

## Overview

IsoLo now integrates **SAM Audio** (Segment Anything Model for Audio) by Meta AI, enabling you to isolate **literally any sound you can name** from your audio files, not just traditional stems like vocals, drums, and bass.

## What is SAM Audio?

SAM Audio is Meta's breakthrough AI model that can separate and isolate specific sounds from complex audio mixtures using natural language descriptions. Instead of being limited to predefined categories, you can describe any sound you want to isolate.

### Examples of What You Can Isolate:

**Traditional Music Stems:**
- "lead vocals"
- "background vocals" 
- "electric guitar"
- "acoustic guitar"
- "bass guitar"
- "drum kit"
- "snare drum"
- "kick drum"
- "piano melody"
- "keyboard chords"
- "string section"
- "brass section"

**Specific Instruments:**
- "saxophone solo"
- "trumpet melody"
- "violin"
- "cello"
- "flute"
- "harmonica"
- "tambourine"
- "cowbell"

**Environmental Sounds:**
- "crowd cheering"
- "applause"
- "rain sounds"
- "thunder"
- "bird chirping"
- "dog barking"
- "car engine"
- "footsteps"

**Speech Elements:**
- "male voice"
- "female voice"
- "child speaking"
- "laughter"
- "crying"
- "whispering"

**Any Other Sound:**
- "phone ringing"
- "door slam"
- "glass breaking"
- "wind blowing"
- "water flowing"
- Literally anything you can describe!

## Installation

### Option 1: Lightweight Inference (Recommended)

For most users, the lightweight inference wrapper is recommended:

```bash
pip install sam-audio-infer
```

This provides:
- ✅ Smaller download size
- ✅ Lower memory usage
- ✅ Faster installation
- ✅ Simpler setup
- ❌ May have slightly lower quality than official version

### Option 2: Official Facebook Research Package

For maximum quality and features:

```bash
# Clone the repository
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio

# Install dependencies
pip install .
```

**Additional Requirements:**
- Python 3.11 or higher
- CUDA-compatible GPU (recommended)
- Hugging Face account and authentication
- Model access approval from Meta

**Authentication Steps:**
1. Go to https://huggingface.co/facebook/sam-audio-large
2. Request access (approval may take a few hours)
3. Generate a Hugging Face access token
4. Authenticate:
   ```bash
   huggingface-cli login
   ```

This provides:
- ✅ Maximum separation quality
- ✅ Full feature set
- ✅ Latest model updates
- ❌ Larger download (~2-5 GB)
- ❌ More complex setup
- ❌ Requires GPU for good performance

### Installing PyTorch (Required for Both Options)

If you don't already have PyTorch installed:

**CPU-only:**
```bash
pip install torch torchaudio
```

**With NVIDIA GPU (CUDA 11.8):**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For Apple Silicon (M1/M2/M3):**
```bash
pip install torch torchaudio
```

## Usage

### Basic Usage in Python

```python
from sam_audio_integration import create_named_stem_separations

# Isolate specific sounds from an audio file
results = create_named_stem_separations(
    "song.mp3",
    prompts=[
        "lead vocals",
        "electric guitar solo",
        "bass line",
        "drum beat"
    ]
)

# Access each isolated sound
for sound_name, (sample_rate, audio_data) in results.items():
    print(f"{sound_name}: {audio_data.shape}")
    # Process or save the isolated audio...
```

### Advanced Usage

```python
from sam_audio_integration import SAMAudioSeparator

# Create a separator instance
separator = SAMAudioSeparator(model_type="large", device="cuda")

# Check if SAM Audio is available
if separator.is_available():
    print("SAM Audio ready!")
else:
    print("SAM Audio not installed")

# Isolate a single sound
sr, audio = separator.separate_by_description(
    "recording.wav",
    "crowd applause",
    output_path="applause_isolated.wav"
)

# Isolate multiple sounds
results = separator.separate_multiple(
    "band_performance.wav",
    descriptions=[
        "lead singer",
        "rhythm guitar", 
        "bass guitar",
        "drums",
        "keyboard"
    ],
    output_dir="isolated_sounds/"
)
```

### Integration with IsoLo

The SAM Audio integration is built into the IsoLo tool. You can use it programmatically:

```python
from app import separate_stems_with_sam_audio, separate_named_sounds

# Method 1: Use enhanced stem separation
stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
    "song.mp3",
    use_sam_audio=True,
    sam_prompts=["vocals", "guitar", "drums", "bass"]
)

# Method 2: Use convenience function with text input
stems_dict, bpm, key, recs = separate_named_sounds(
    "song.mp3",
    "lead vocals, electric guitar, bass line, drum beat"
)
```

## Architecture

### Module Structure

```
FileUploads/
├── sam_audio_integration.py    # SAM Audio wrapper module
├── app.py                       # Main application with integration
└── requirements (1).txt         # Updated dependencies
```

### Key Components

1. **`SAMAudioSeparator` Class**
   - Handles model initialization and inference
   - Supports both lightweight and official packages
   - Lazy loading for efficient memory usage
   - Automatic device selection (CPU/GPU)

2. **`separate_by_description()` Function**
   - Isolates a single named sound
   - Returns sample rate and audio data
   - Optional file output

3. **`separate_multiple()` Function**
   - Batch isolation of multiple sounds
   - Efficient processing of multiple prompts
   - Optional directory output

4. **`create_named_stem_separations()` Function**
   - High-level convenience function
   - Simple interface for common use cases

### Integration Points

The SAM Audio functionality is integrated into the existing IsoLo workflow:

- **`separate_stems_with_sam_audio()`**: Enhanced version of stem separation
- **`separate_named_sounds()`**: New convenience function for named isolation
- **Backward Compatibility**: Original `separate_stems()` function still works

## Performance Considerations

### Model Size vs. Quality

| Model Type | Quality | Speed | VRAM Usage | Use Case |
|------------|---------|-------|------------|----------|
| `small`    | Good    | Fast  | ~2 GB      | Quick tests, CPU inference |
| `base`     | Better  | Medium| ~4 GB      | Balanced performance |
| `large`    | Best    | Slow  | ~8 GB      | Maximum quality |

### Speed Optimization

**For Faster Processing:**
- Use smaller model sizes (`small` or `base`)
- Use GPU if available
- Process shorter audio segments
- Use the lightweight inference wrapper

**For Better Quality:**
- Use `large` model size
- Use the official package
- Ensure GPU acceleration
- Allow longer processing time

### Memory Management

SAM Audio uses lazy initialization, so the model is only loaded when first needed. This saves memory and startup time.

```python
# Model is not loaded yet
separator = SAMAudioSeparator()

# Model loads on first use
sr, audio = separator.separate_by_description("file.wav", "vocals")

# Subsequent calls reuse the loaded model
sr, audio2 = separator.separate_by_description("file2.wav", "guitar")
```

## Troubleshooting

### "SAM Audio is not available" Error

**Solution:**
```bash
# Try installing the lightweight version first
pip install sam-audio-infer

# Or install the official version
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio
pip install .
```

### CUDA Out of Memory

**Solutions:**
- Use smaller model: `SAMAudioSeparator(model_type="small")`
- Use CPU instead: `SAMAudioSeparator(device="cpu")`
- Process shorter audio segments
- Close other GPU-using applications

### Slow Processing on CPU

**Solutions:**
- Install CUDA and PyTorch with GPU support
- Use smaller model size
- Process shorter audio clips
- Consider using cloud GPU services

### Import Errors

**Solutions:**
```bash
# Ensure all dependencies are installed
pip install torch torchaudio
pip install numpy scipy soundfile librosa

# Then install SAM Audio
pip install sam-audio-infer
```

### Model Download Issues

**For Official Package:**
- Ensure you have Hugging Face authentication
- Check that you have model access approval
- Try re-authenticating: `huggingface-cli login`

## Comparison with Traditional Stem Separation

| Feature | Traditional Stems | SAM Audio |
|---------|------------------|-----------|
| **Flexibility** | Fixed categories only | Any sound you can name |
| **Categories** | 4-6 stems (vocals, drums, bass, other) | Unlimited |
| **Specificity** | Cannot isolate specific instruments within category | Can isolate very specific sounds |
| **Examples** | "vocals", "drums" | "saxophone solo", "crowd cheering", "dog barking" |
| **Quality** | Good for standard stems | Excellent for named isolation |
| **Speed** | Fast | Moderate to slow |
| **Use Cases** | Music production, remixing | Sound design, foley, precise editing |

## Best Practices

### Writing Effective Prompts

**Good Prompts:**
- ✅ "lead vocals"
- ✅ "electric guitar solo"
- ✅ "snare drum"
- ✅ "crowd applause"
- ✅ "rain sounds"

**Less Effective Prompts:**
- ❌ "music" (too vague)
- ❌ "stuff" (not descriptive)
- ❌ "everything except vocals" (use positive descriptions)

**Tips:**
- Be specific: "saxophone solo" > "saxophone"
- Use common terms: "guitar" > "stringed instrument"
- Describe what you want, not what you don't want
- One sound per prompt for best results

### Combining Traditional Stems and SAM Audio

You can use both approaches together:

```python
# 1. First do traditional stem separation for main categories
stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
    "song.mp3",
    use_sam_audio=False
)

# 2. Then use SAM Audio to isolate specific sounds from vocals stem
separator = SAMAudioSeparator()
sr, lead_vocals = separator.separate_by_description(
    "vocals.wav",  # from traditional separation
    "lead singer"
)
sr, backing_vocals = separator.separate_by_description(
    "vocals.wav",
    "background vocals"
)
```

## Future Enhancements

Planned improvements for SAM Audio integration:

- [ ] **UI Integration**: Add SAM Audio controls to Gradio interface
- [ ] **Batch Processing**: Process multiple files with same prompts
- [ ] **Preset Prompts**: Common prompt templates for quick selection
- [ ] **Quality Presets**: Easy switching between speed/quality modes
- [ ] **Caching**: Cache separated sounds for faster re-processing
- [ ] **Export Options**: Multiple format support for isolated sounds
- [ ] **Visualization**: Show spectrograms of isolated sounds
- [ ] **Mixing**: Remix isolated sounds with effects

## Resources

### Documentation
- [SAM Audio Official Repository](https://github.com/facebookresearch/sam-audio)
- [SAM Audio Paper](https://arxiv.org/abs/2412.xxxxx) *(when published)*
- [Lightweight Inference Wrapper](https://github.com/openmirlab/sam-audio-infer)

### Community
- [GitHub Issues](https://github.com/facebookresearch/sam-audio/issues)
- [Hugging Face Model Page](https://huggingface.co/facebook/sam-audio-large)

### Related Tools
- [Demucs](https://github.com/facebookresearch/demucs) - Traditional stem separation
- [Spleeter](https://github.com/deezer/spleeter) - Alternative stem separation
- [AudioCraft](https://github.com/facebookresearch/audiocraft) - Audio generation

## License

SAM Audio is developed by Meta AI Research and is subject to Meta's research license. Please review the license terms before commercial use.

## Support

For issues or questions:
1. Check this documentation
2. Review [SAM Audio GitHub Issues](https://github.com/facebookresearch/sam-audio/issues)
3. Open an issue in this repository
4. Check the troubleshooting section above

---

**Last Updated:** January 2025  
**Status:** ✅ Integrated and Functional (Backend Only)  
**UI Status:** 📅 Planned for future release
