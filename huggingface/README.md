---
title: Loop Architect
emoji: 🎵
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🎵 Loop Architect - AI-Powered Audio Processing

Loop Architect is a powerful audio processing tool that combines traditional stem separation with AI-powered named sound isolation. Upload any audio file to separate it into stems, detect musical attributes (BPM, key), and generate perfectly tagged loops ready for your DAW.

## ✨ Features

### 🎼 Audio Analysis
- **BPM Detection** - Automatic tempo detection with manual override
- **Key Detection** - Musical key identification using Krumhansl-Schmuckler algorithm
- **Harmonic Recommendations** - Compatible keys based on the Camelot Wheel

### ✂️ Stem Separation
Traditional stem separation into:
- 🎤 Vocals
- 🥁 Drums
- 🎸 Bass
- 🎹 Guitar
- 🎹 Piano
- 🎶 Other

### 🤖 SAM Audio Integration (Optional)
Isolate **any sound you can name** using AI:
- "lead vocals" - Extract just the main vocal line
- "saxophone solo" - Isolate specific instruments
- "crowd applause" - Extract ambient sounds
- "rain sounds" - Isolate environmental audio

### 🔧 Advanced Processing

**Loop Generation:**
- 1/2/4 Bar Loops with tempo sync
- One-shot slicing with adjustable sensitivity
- Automatic crossfading for seamless loops

**Effects & Modulation:**
- Tempo-synced LFO for panning and tremolo
- Filter modulation (low-pass/high-pass)
- Peak normalization
- Attack/sustain envelope shaping
- Pitch transposition

**Professional Output:**
- WAV file export (16-bit PCM)
- MIDI file generation for melodic stems
- BPM and key tags in filenames
- ZIP package download with organized folders

## 🚀 Usage

### Basic Workflow

1. **Upload & Analyze**
   - Upload your audio file (WAV, MP3, etc.)
   - Click "Separate Stems & Analyze"
   - Review detected BPM and key

2. **Configure Settings**
   - Adjust BPM if needed
   - Choose loop type (Bar Loops or One-Shots)
   - Set time signature (4/4 or 3/4)
   - Optional: Apply effects and transposition

3. **Generate Loops**
   - Click "SLICE ALL & GENERATE PACK"
   - Download your complete loop pack as a ZIP file

### Advanced Features

**LFO Modulation:**
- Add movement with tempo-synced panning and volume modulation
- Create filter sweeps with adjustable depth

**One-Shot Shaping:**
- Adjust sensitivity to control slice detection
- Shape transients with attack/sustain envelopes

**Key Transposition:**
- Transpose loops while maintaining key tags
- Perfect for fitting samples into your project's key

## 📦 Output Structure

Your loop pack ZIP contains:
```
Loop_Architect_Pack.zip
├── WAV/
│   ├── vocals_4Bar_001_CMaj_120BPM.wav
│   ├── drums_4Bar_001_CMaj_120BPM.wav
│   └── ...
└── MID/
    ├── vocals_MELODY_CMaj_120BPM.mid
    └── ...
```

## 🛠️ Installation (Local Deployment)

### Prerequisites
- Python 3.8+
- FFmpeg (for audio file format support)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Optional: SAM Audio

For named sound isolation capabilities:

```bash
# Lightweight version (recommended)
pip install sam-audio-infer

# OR Official version (maximum quality)
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio && pip install .
```

### Run Locally

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

## 📋 System Requirements

### Minimum
- 4GB RAM
- CPU with AVX support
- 1GB free disk space

### Recommended for SAM Audio
- 8GB+ RAM
- CUDA-capable GPU (for faster processing)
- 2GB+ free disk space

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file:

```bash
# SAM Audio Model Path (if using custom model)
SAM_AUDIO_MODEL_PATH=/path/to/model

# Processing Settings
MAX_AUDIO_LENGTH=600  # seconds
ENABLE_SAM_AUDIO=true
```

## 📚 Documentation

Full documentation available in the [main repository](https://github.com/SaltProphet/IsoLo):
- [Backend Documentation](../backend/README.md)
- [SAM Audio Integration](../backend/SAM_AUDIO_INTEGRATION.md)
- [Project Overview](../README.md)

## 🎯 Use Cases

### Music Production
- Extract stems for remixing
- Generate loop libraries
- Create sample packs
- Isolate instruments for study

### DJs
- Prepare acapellas and instrumentals
- Create mashup-ready stems
- Build custom effect loops

### Sound Design
- Extract specific sounds from field recordings
- Isolate individual elements from complex audio
- Generate one-shot samples

### Audio Analysis
- Study arrangement and production techniques
- Analyze individual instrument performances
- Educational music theory applications

## 🤝 Contributing

This project is part of the IsoLo repository. Contributions welcome!

Visit the [main repository](https://github.com/SaltProphet/IsoLo) for contribution guidelines.

## 📄 License

MIT License - See repository for details

## 🙏 Acknowledgments

- **Librosa** - Audio analysis and processing
- **Gradio** - Web interface framework
- **Meta SAM Audio** - AI-powered sound isolation (optional)
- Built with AI-Native Development principles

## ⚠️ Notes

### Stem Separation Limitations
This demo uses mock stem separation for demonstration. For production use, integrate with:
- [Demucs](https://github.com/facebookresearch/demucs) - High-quality stem separation
- [Spleeter](https://github.com/deezer/spleeter) - Fast stem separation
- Or any other source separation model

### SAM Audio
SAM Audio integration is optional and requires additional setup. The app works perfectly without it using traditional stem separation.

### Processing Time
- Analysis: ~5-30 seconds
- Stem separation: ~30-120 seconds (depends on audio length and model)
- Slicing: ~5-15 seconds per stem

---

**Powered by AI-Aware Development** 🤖✨
