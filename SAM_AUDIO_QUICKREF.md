# SAM Audio Quick Reference

## Installation

```bash
# Option 1: Lightweight (recommended)
pip install sam-audio-infer

# Option 2: Official package
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio && pip install .
```

## Basic API

### Single Sound Isolation

```python
from sam_audio_integration import SAMAudioSeparator

separator = SAMAudioSeparator()
sr, audio = separator.separate_by_description(
    "input.wav",
    "lead vocals",
    output_path="vocals.wav"  # optional
)
```

### Multiple Sounds

```python
results = separator.separate_multiple(
    "input.wav",
    ["vocals", "guitar", "drums"],
    output_dir="outputs/"  # optional
)

for name, (sr, audio) in results.items():
    print(f"{name}: {audio.shape}")
```

### Convenience Function

```python
from sam_audio_integration import create_named_stem_separations

results = create_named_stem_separations(
    "song.mp3",
    ["vocals", "guitar", "drums", "bass"]
)
```

## Integration with Loop Architect

### Using Enhanced Separation

```python
from app import separate_stems_with_sam_audio

stems_dict, bpm, key, recs = separate_stems_with_sam_audio(
    "song.mp3",
    use_sam_audio=True,
    sam_prompts=["lead vocals", "guitar", "bass", "drums"]
)
```

### Using Convenience Wrapper

```python
from app import separate_named_sounds

stems_dict, bpm, key, recs = separate_named_sounds(
    "song.mp3",
    "lead vocals, electric guitar, bass line, drum beat"
)
```

## Example Prompts

### Music
- "lead vocals" / "background vocals"
- "electric guitar" / "acoustic guitar"
- "bass guitar" / "bass line"
- "drum kit" / "snare drum" / "kick drum"
- "piano melody" / "keyboard chords"
- "saxophone solo" / "trumpet"
- "string section" / "violin"

### Voice
- "male voice" / "female voice"
- "child speaking"
- "laughter" / "crying"
- "whispering" / "shouting"

### Environment
- "crowd applause" / "cheering"
- "rain sounds" / "thunder"
- "wind blowing"
- "bird chirping" / "dog barking"
- "car engine" / "traffic"
- "ocean waves" / "water flowing"

### Effects
- "door slam" / "footsteps"
- "glass breaking"
- "phone ringing"
- "clock ticking"

## Advanced Configuration

### Model Selection

```python
# Smaller, faster (less accurate)
separator = SAMAudioSeparator(model_type="small")

# Balanced
separator = SAMAudioSeparator(model_type="base")

# Larger, slower (most accurate)
separator = SAMAudioSeparator(model_type="large")
```

### Device Selection

```python
# Automatic (uses GPU if available)
separator = SAMAudioSeparator(device="auto")

# Force CPU
separator = SAMAudioSeparator(device="cpu")

# Force CUDA
separator = SAMAudioSeparator(device="cuda")
```

### Check Availability

```python
separator = SAMAudioSeparator()
if separator.is_available():
    print("SAM Audio ready!")
else:
    print("Please install SAM Audio")
```

## Error Handling

```python
try:
    sr, audio = separator.separate_by_description(
        "song.wav",
        "vocals"
    )
except ImportError:
    print("SAM Audio not installed")
except Exception as e:
    print(f"Separation failed: {e}")
```

## Performance Tips

1. **Use smaller models** for faster processing
2. **Use GPU** when available
3. **Process shorter segments** for memory efficiency
4. **Batch similar prompts** together
5. **Cache model** (automatic with lazy loading)

## Common Issues

### "SAM Audio is not installed"
```bash
pip install sam-audio-infer
```

### "CUDA out of memory"
```python
# Use smaller model
separator = SAMAudioSeparator(model_type="small", device="cpu")
```

### "Slow processing"
```python
# Use GPU or smaller model
separator = SAMAudioSeparator(model_type="base", device="cuda")
```

## Files

- `sam_audio_integration.py` - Core integration module
- `SAM_AUDIO_INTEGRATION.md` - Full documentation
- `test_sam_audio.py` - Test suite
- `examples_sam_audio.py` - Usage examples
- `app.py` - Main application with integration

## See Also

- Full documentation: `SAM_AUDIO_INTEGRATION.md`
- Examples: `examples_sam_audio.py`
- Tests: `python test_sam_audio.py`
