# 🎵 Automatic Music Video Generator

An AI-powered application for generating music videos automatically from audio files. The system uses advanced audio analysis, speech-to-text lyric extraction, and customizable visual generation to create engaging music videos.

## 🌟 Overview

This project provides a modular, extensible framework for automatic music video generation. It combines state-of-the-art audio processing, lyric synchronization, and video composition into a user-friendly application.

### Key Features

- **🎼 Audio Analysis**: Automatic stem separation (vocals, drums, bass, other), BPM detection, key detection, and bar/beat analysis
- **📝 Lyric Extraction**: Speech-to-text transcription with word-level timestamps using Whisper
- **🎨 Visual Generation**: Multiple visualization styles including waveforms, spectrograms, and lyric overlays
- **🖥️ User-Friendly Interface**: Simple web-based UI powered by Gradio
- **🔧 Modular Architecture**: Clean separation of concerns for easy extension and maintenance

## 📋 Project Roadmap

The development follows a phased approach:

### Phase 1: Audio Analysis ✅ (In Progress)
- [x] Project scaffolding and directory structure
- [x] Audio analysis module stub (stem separation, BPM, key detection)
- [ ] Implement demucs integration for stem separation
- [ ] Implement librosa-based BPM/key/bar detection
- [ ] Add audio feature extraction pipeline

### Phase 2: Lyric Extraction & Synchronization 🔄 (Next)
- [x] Lyric synchronization module stub
- [ ] Integrate OpenAI Whisper for speech-to-text
- [ ] Implement word-level timestamp extraction
- [ ] Add manual lyric alignment support
- [ ] Implement SRT/LRC export functionality

### Phase 3: Visual Generation 📅 (Planned)
- [x] Visual generation module stub
- [ ] Implement waveform visualization
- [ ] Implement spectrum/frequency visualization
- [ ] Add lyric overlay with karaoke-style highlighting
- [ ] Implement beat-reactive visual effects
- [ ] Add background customization (solid, gradient, image, video)

### Phase 4: User Experience & Interface 📅 (Planned)
- [x] Basic Gradio interface stub
- [ ] Implement full Gradio UI with all controls
- [ ] Add real-time progress tracking
- [ ] Add video preview functionality
- [ ] Implement batch processing support
- [ ] Add preset/template system

### Phase 5: Advanced Features 🔮 (Future)
- [ ] AI-driven visual selection based on audio characteristics
- [ ] Style transfer for video backgrounds
- [ ] Multiple aspect ratio support (16:9, 9:16, 1:1)
- [ ] Integration with external video sources (stock footage, generative AI)
- [ ] Advanced transitions and effects library
- [ ] Export to multiple formats and quality levels
- [ ] Cloud processing support for heavy workloads

## 🏗️ System Architecture

```
music_video_gen/
│
├── app.py                    # Main application entry point (Gradio UI)
│
├── engine/                   # Core backend modules
│   ├── __init__.py          # Package initialization
│   ├── audio_analysis.py    # Audio processing & feature extraction
│   │   └── AudioAnalyzer    # Stem separation, BPM, key, bar detection
│   ├── lyric_sync.py        # Lyric extraction & synchronization
│   │   └── LyricSynchronizer # Whisper STT, timestamp alignment
│   ├── visual_gen.py        # Video generation & composition
│   │   └── VisualGenerator  # Waveforms, spectrums, lyric videos
│   └── utils.py             # Common utilities
│       └── Helpers          # Logging, file handling, caching
│
├── static/                   # Static assets (fonts, templates, etc.)
│
├── tests/                    # Unit and integration tests
│
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Gradio Web Interface                     │
│                        (app.py)                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  MusicVideoGenerator                         │
│                   (Orchestration Layer)                      │
└──────────┬──────────────┬──────────────┬────────────────────┘
           │              │              │
           ▼              ▼              ▼
   ┌───────────┐  ┌──────────────┐  ┌──────────────┐
   │   Audio   │  │    Lyric     │  │   Visual     │
   │ Analyzer  │  │ Synchronizer │  │  Generator   │
   └───────────┘  └──────────────┘  └──────────────┘
        │                 │                  │
        ▼                 ▼                  ▼
   ┌─────────────────────────────────────────────┐
   │   External Libraries & Dependencies         │
   │  (demucs, librosa, whisper, moviepy)       │
   └─────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: User uploads audio file via web interface
2. **Audio Analysis**: 
   - Load and validate audio file
   - Separate stems (vocals, drums, bass, other)
   - Extract features (BPM, key, bars, beats)
3. **Lyric Processing** (if requested):
   - Extract lyrics using Whisper STT
   - Generate word-level timestamps
   - Format and clean transcription
4. **Visual Generation**:
   - Generate visualization frames based on selected style
   - Synchronize visuals with audio features (beats, bars)
   - Add lyric overlays with animations
5. **Composition**:
   - Combine all visual layers
   - Attach audio track
   - Render final video
6. **Output**: Return video file to user for download/preview

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** (3.10 or 3.11 recommended)
- **FFmpeg** (required for audio/video processing)
- **CUDA** (optional, for GPU acceleration)

### Installation

#### 1. Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH.

#### 2. Clone the Repository

```bash
git clone https://github.com/SaltProphet/FileUploads.git
cd FileUploads/music_video_gen
```

#### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 4. Install Dependencies

**CPU-only installation:**
```bash
pip install -r requirements.txt
```

**With GPU support (NVIDIA CUDA):**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

**For Apple Silicon (M1/M2/M3):**
```bash
pip install torch torchaudio
pip install -r requirements.txt
```

### Running the Application

#### Web Interface (Gradio)

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

**Additional options:**
```bash
python app.py --share          # Create public share link
python app.py --port 8080      # Use custom port
python app.py --debug          # Enable debug mode
```

#### Command-Line Interface (Coming Soon)

```bash
python app.py --cli \
  --input song.mp3 \
  --style waveform \
  --extract-lyrics \
  --output video.mp4
```

## 📖 Usage Guide

### Basic Workflow

1. **Upload Audio**: Select an audio file (MP3, WAV, FLAC, etc.)
2. **Choose Style**: Select visualization style:
   - Waveform: Classic audio waveform visualization
   - Spectrum: Frequency spectrum/spectrogram
   - Lyric Video: Text-based lyric video
   - Minimal: Clean, minimal design
3. **Lyric Options**:
   - Auto-extract: Use Whisper to transcribe lyrics
   - Manual: Provide your own lyrics for alignment
4. **Generate**: Click "Generate Video" and wait for processing
5. **Preview & Download**: View the generated video and download

### Advanced Options (Coming Soon)

- Custom color schemes
- Font selection for lyrics
- Background customization (image, video, gradient)
- Beat-reactive effects intensity
- Video resolution and frame rate
- Multiple export formats

## 🧪 Development

### Project Structure Notes

- **Modular Design**: Each engine module is independent and can be used standalone
- **Stub Implementation**: Current version contains fully documented stubs with TODO comments
- **Type Hints**: All functions use Python type hints for clarity
- **Docstrings**: Comprehensive documentation for all classes and functions

### Current Status

**✅ Completed:**
- Project scaffolding and directory structure
- Engine module stubs with comprehensive docstrings
- Requirements specification
- Architecture documentation
- Basic Gradio interface stub

**🔄 In Progress:**
- Audio analysis implementation
- Lyric extraction integration
- Visual generation pipeline

**📅 Planned:**
- Full UI implementation
- Batch processing
- Advanced visual effects
- Performance optimizations

### Contributing

This project follows a spec-driven development approach:

1. Review specifications in `/docs/specs/`
2. Check TODO comments in engine modules
3. Implement features according to docstrings
4. Add tests for new functionality
5. Update documentation

## 📚 Technical Details

### Stem Separation

Uses [Demucs](https://github.com/facebookresearch/demucs) for state-of-the-art source separation:
- Separates audio into vocals, drums, bass, and other
- Multiple model options (htdemucs, mdx, mdx_extra)
- GPU-accelerated when available

### Lyric Extraction

Uses [OpenAI Whisper](https://github.com/openai/whisper) for accurate transcription:
- Multiple model sizes (tiny to large)
- Word-level timestamps
- Multi-language support
- High accuracy on musical vocals

### Video Composition

Uses [MoviePy](https://zulko.github.io/moviepy/) for video editing:
- Flexible compositing system
- Support for various codecs
- Text rendering and effects
- Audio-video synchronization

### Audio Analysis

Uses [Librosa](https://librosa.org/) for audio processing:
- BPM detection via beat tracking
- Musical key detection via chroma features
- Bar/beat alignment
- Comprehensive feature extraction

## 🎯 Design Principles

1. **Modularity**: Each component is self-contained and reusable
2. **Extensibility**: Easy to add new visualization styles and effects
3. **Performance**: Caching and optimization for large files
4. **User-Friendly**: Simple interface for non-technical users
5. **Professional Output**: High-quality video generation
6. **Open Source**: Built on open-source tools and libraries

## 🔧 Troubleshooting

### Common Issues

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your system PATH
- Test with: `ffmpeg -version`

**CUDA out of memory:**
- Use smaller model sizes (tiny, base instead of large)
- Process audio in chunks
- Use CPU mode instead: `--device cpu`

**Slow processing:**
- Enable GPU acceleration if available
- Use smaller/faster models for real-time work
- Consider reducing video resolution

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.9+ required)

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

This project builds on excellent open-source tools:
- [Demucs](https://github.com/facebookresearch/demucs) by Meta AI Research
- [Whisper](https://github.com/openai/whisper) by OpenAI
- [Librosa](https://librosa.org/) for audio analysis
- [MoviePy](https://zulko.github.io/moviepy/) for video editing
- [Gradio](https://gradio.app/) for the web interface

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation in `/docs/`
- Review TODO comments in engine modules

---

**Built with ❤️ and 🎵** | Status: 🏗️ In Development (Phase 1)
