# 🎵 SAM Audio Integration - README

## What's New?

Loop Architect now supports **SAM Audio** (Segment Anything Model for Audio) by Meta AI! 

This means you can now isolate **literally ANY sound you can name** from your audio files - not just traditional stems like vocals, drums, and bass.

## Quick Start

### 1. Install SAM Audio (Optional)

The integration works without SAM Audio installed, but to use the named sound isolation features:

```bash
# Lightweight version (recommended for most users)
pip install sam-audio-infer

# OR Official version (maximum quality, requires GPU)
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio && pip install .
```

### 2. Use It!

```python
from sam_audio_integration import SAMAudioSeparator

# Isolate any sound by name
separator = SAMAudioSeparator()
sr, audio = separator.separate_by_description(
    "song.mp3",
    "lead vocals"  # or "saxophone solo", "crowd applause", etc.
)
```

## What Can You Isolate?

🎸 **Musical Instruments**
- "lead vocals", "background vocals"
- "electric guitar", "acoustic guitar", "bass guitar"
- "drum kit", "snare drum", "kick drum"
- "piano melody", "keyboard chords"
- "saxophone solo", "trumpet", "violin"

🗣️ **Voice & Speech**
- "male voice", "female voice", "child speaking"
- "laughter", "crying", "whispering"

🌍 **Environmental Sounds**
- "crowd applause", "cheering"
- "rain sounds", "thunder", "wind"
- "bird chirping", "dog barking"
- "car engine", "traffic"

🔊 **Sound Effects**
- "door slam", "footsteps"
- "glass breaking"
- "phone ringing"
- And literally anything else you can describe!

## Key Features

### ✅ Backward Compatible
- Existing code works exactly as before
- SAM Audio is an optional enhancement
- Falls back to traditional stems if not installed

### ✅ Easy to Use
```python
# Simple single sound
from sam_audio_integration import create_named_stem_separations
results = create_named_stem_separations("song.mp3", ["vocals", "guitar"])

# Multiple sounds with Loop Architect
from app import separate_named_sounds
stems, bpm, key, recs = separate_named_sounds(
    "song.mp3",
    "lead vocals, electric guitar, bass line, drum beat"
)
```

### ✅ Production Ready
- Comprehensive error handling
- Automatic device selection (GPU/CPU)
- Lazy model loading
- Type hints throughout
- Full test suite included

## Documentation

- **[SAM_AUDIO_INTEGRATION.md](SAM_AUDIO_INTEGRATION.md)** - Complete guide (installation, usage, troubleshooting)
- **[SAM_AUDIO_QUICKREF.md](SAM_AUDIO_QUICKREF.md)** - Quick reference for developers
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[examples_sam_audio.py](examples_sam_audio.py)** - Usage examples

## Testing

Run the test suite to verify everything works:

```bash
python test_sam_audio.py
```

View usage examples:

```bash
python examples_sam_audio.py
```

## Architecture

```
┌───────────────────────┐
│  Your Code / UI       │
│  (app.py)             │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  SAM Audio Module     │
│  (sam_audio_          │
│   integration.py)     │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  SAM Audio Package    │
│  (sam-audio-infer or  │
│   facebook/sam-audio) │
└───────────────────────┘
```

## Files

| File | Description | Lines |
|------|-------------|-------|
| `sam_audio_integration.py` | Core wrapper module | 368 |
| `app.py` | Enhanced with SAM Audio | Modified |
| `SAM_AUDIO_INTEGRATION.md` | Complete documentation | 487 |
| `SAM_AUDIO_QUICKREF.md` | Quick reference | 152 |
| `IMPLEMENTATION_SUMMARY.md` | Implementation details | 362 |
| `examples_sam_audio.py` | Usage examples | 324 |
| `test_sam_audio.py` | Test suite | 216 |
| `requirements (1).txt` | Updated dependencies | Updated |

## API Overview

### SAMAudioSeparator Class

```python
from sam_audio_integration import SAMAudioSeparator

separator = SAMAudioSeparator(
    model_type="large",  # "small", "base", or "large"
    device="auto"        # "auto", "cpu", or "cuda"
)

# Single sound
sr, audio = separator.separate_by_description(
    audio_path="input.wav",
    description="lead vocals",
    output_path="vocals.wav"  # optional
)

# Multiple sounds
results = separator.separate_multiple(
    audio_path="input.wav",
    descriptions=["vocals", "guitar", "drums"],
    output_dir="outputs/"  # optional
)

# Check availability
if separator.is_available():
    print("Ready to use!")
```

### Integration Functions

```python
# High-level convenience function
from sam_audio_integration import create_named_stem_separations
results = create_named_stem_separations(
    "song.mp3",
    ["vocals", "guitar", "drums", "bass"]
)

# With Loop Architect features
from app import separate_stems_with_sam_audio
stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
    "song.mp3",
    use_sam_audio=True,
    sam_prompts=["lead vocals", "guitar", "bass", "drums"]
)

# Convenience wrapper with text input
from app import separate_named_sounds
stems_dict, bpm, key, recs = separate_named_sounds(
    "song.mp3",
    "lead vocals, electric guitar, bass line, drum beat"
)
```

## Performance

| Model | Quality | Speed | VRAM | Use Case |
|-------|---------|-------|------|----------|
| `small` | Good | Fast | ~2 GB | Quick tests |
| `base` | Better | Medium | ~4 GB | Balanced |
| `large` | Best | Slow | ~8 GB | Max quality |

**Tips:**
- Use GPU for best performance
- Use smaller models for faster processing
- Process shorter segments to save memory
- Model loads only when first used (lazy loading)

## Troubleshooting

### SAM Audio not installed?
```bash
pip install sam-audio-infer
```

### Out of memory?
```python
# Use smaller model or CPU
separator = SAMAudioSeparator(model_type="small", device="cpu")
```

### Slow on CPU?
```python
# Use GPU or smaller model
separator = SAMAudioSeparator(model_type="base", device="cuda")
```

See [SAM_AUDIO_INTEGRATION.md](SAM_AUDIO_INTEGRATION.md) for more troubleshooting.

## Comparison

| Feature | Traditional Stems | SAM Audio |
|---------|------------------|-----------|
| **Flexibility** | 4-6 fixed categories | Unlimited - any sound you can name |
| **Specificity** | "vocals", "drums" | "saxophone solo", "crowd cheering" |
| **Speed** | Fast | Moderate to slow |
| **Quality** | Good for standard stems | Excellent for specific sounds |
| **Use Cases** | Music production | Sound design, precise editing |

## Examples

### Isolate Specific Instruments
```python
separator = SAMAudioSeparator()
sr, sax = separator.separate_by_description("jazz.wav", "saxophone solo")
sr, piano = separator.separate_by_description("jazz.wav", "piano melody")
```

### Extract Environmental Sounds
```python
sr, applause = separator.separate_by_description("concert.wav", "crowd applause")
sr, rain = separator.separate_by_description("nature.wav", "rain sounds")
```

### Isolate Vocals by Type
```python
sr, lead = separator.separate_by_description("song.wav", "lead vocals")
sr, backing = separator.separate_by_description("song.wav", "background vocals")
```

## Status

✅ **Backend Implementation**: Complete  
✅ **API Design**: Complete  
✅ **Documentation**: Complete  
✅ **Testing**: Complete  
⏭️ **UI Integration**: Deferred (per user request)

## Contributing

The SAM Audio integration is modular and extensible. To contribute:

1. Review the implementation in `sam_audio_integration.py`
2. Check tests in `test_sam_audio.py`
3. See examples in `examples_sam_audio.py`
4. Read full docs in `SAM_AUDIO_INTEGRATION.md`

## Resources

- [SAM Audio Official Repo](https://github.com/facebookresearch/sam-audio)
- [Lightweight Wrapper](https://github.com/openmirlab/sam-audio-infer)
- [Meta AI Blog Post](https://about.fb.com/news/2025/12/our-new-sam-audio-model-transforms-audio-editing/)

## License

SAM Audio is developed by Meta AI Research. Review license terms for commercial use.

---

**Questions?** See [SAM_AUDIO_INTEGRATION.md](SAM_AUDIO_INTEGRATION.md) for comprehensive documentation.

**Issues?** Check the troubleshooting section in the full documentation.

**Want UI?** UI integration is planned for a future release. Backend is ready now!
