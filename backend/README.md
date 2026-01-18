# IsoLo - Backend

This directory contains the Python backend for IsoLo, which provides audio processing capabilities including stem separation and SAM Audio integration.

## Files

- **`app.py`** - Main Gradio application providing a web interface for audio processing
- **`sam_audio_integration.py`** - Integration module for Meta's SAM Audio (Segment Anything Model for Audio)
- **`SAM_AUDIO_INTEGRATION.md`** - Complete documentation for SAM Audio integration

## Features

### Traditional Stem Separation
- Separate audio into vocals, drums, bass, other, guitar, and piano
- BPM detection and key detection
- Harmonic recommendations using Camelot Wheel
- Audio slicing and loop generation

### SAM Audio Integration
- Isolate **any sound you can name** using natural language descriptions
- Examples: "lead vocals", "saxophone solo", "crowd applause", "rain sounds"
- Batch processing of multiple sound descriptions
- See `SAM_AUDIO_INTEGRATION.md` for full documentation

## Installation

### Prerequisites
- Python 3.8+
- Required packages (see root `package.json` for full list):
  - numpy
  - scipy
  - soundfile
  - librosa
  - gradio
  - matplotlib
  - torch (for SAM Audio)

### Install Dependencies

```bash
pip install numpy scipy soundfile librosa gradio matplotlib
```

### Optional: SAM Audio

For named sound isolation capabilities:

```bash
# Lightweight version (recommended)
pip install sam-audio-infer

# OR Official version (for maximum quality)
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio && pip install .
```

## Usage

### Run the Gradio App

```bash
python backend/app.py
```

Then open your browser to `http://localhost:7860`

### Use as Python API

```python
from backend.sam_audio_integration import SAMAudioSeparator

# Isolate any sound by name
separator = SAMAudioSeparator()
sr, audio = separator.separate_by_description(
    "song.mp3",
    "lead vocals"
)
```

## Architecture

The backend is designed to work independently or integrate with the React frontend:

```
React Frontend (src/) ←→ Python Backend (backend/)
                          ├── app.py (Gradio interface)
                          └── sam_audio_integration.py (SAM Audio)
```

## Documentation

- **Main README**: See [../README.md](../README.md) for project overview
- **SAM Audio**: See [SAM_AUDIO_INTEGRATION.md](./SAM_AUDIO_INTEGRATION.md) for complete SAM Audio documentation
- **AI Agent Guides**: See [../AGENTS.md](../AGENTS.md) and [../GEMINI.md](../GEMINI.md)

## Development

The backend follows the same coding standards as the frontend:
- Type hints for all function parameters and returns
- Comprehensive docstrings
- Error handling with graceful fallbacks
- Modular, reusable components
