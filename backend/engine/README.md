# IsoLo Sample Pack Generator - Engine Architecture

## Overview

The Sample Pack Generator is a modular, agent-based system for creating professional music sample packs from audio files. The system uses a pipeline of specialized agents, each handling a specific aspect of audio/video processing and pack creation.

## Architecture

### Agent-Based Design

The system is built on a **modular agent architecture** where each agent:
- Inherits from `BaseAgent` for consistent interfaces
- Handles a single responsibility (separation of concerns)
- Communicates via JSON manifests and standardized data structures
- Can be used independently or as part of a pipeline
- Provides comprehensive error handling and logging

### Directory Structure

```
backend/engine/
├── __init__.py                      # Engine package initialization
├── agents/                          # Agent modules
│   ├── __init__.py                  # Agents package exports
│   ├── base_agent.py                # Base class for all agents
│   ├── stem_separation_agent.py     # Agent 1: Stem separation & analysis
│   ├── vocal_builder_agent.py       # Agent 2: Vocal & instrumental builds
│   ├── loop_generator_agent.py      # Agent 3: Loops & one-shots
│   ├── lyric_extraction_agent.py    # Agent 4: Lyric extraction & sync
│   ├── video_export_agent.py        # Agent 5: Video generation
│   ├── pack_export_agent.py         # Agent 6: Pack organization & export
│   └── ui_agent.py                  # Agent 7: UI orchestration
└── README.md                        # This file
```

## Agents

### 1. Stem Separation & Core Analysis Agent

**Purpose**: First stage of the pipeline - ingests audio and performs core analysis.

**Responsibilities**:
- Audio file ingestion and validation
- Stem separation using Demucs (vocals, drums, bass, other, guitar, piano)
- BPM (tempo) detection
- Musical key detection
- Bar grid generation for accurate slicing
- JSON manifest generation

**Key Methods**:
- `separate_stems(audio_path, output_dir)` - Separate audio into stems
- `analyze_audio(audio_path)` - Extract BPM, key, and other metadata
- `detect_bpm(audio_path)` - Detect tempo
- `detect_key(audio_path)` - Detect musical key
- `generate_manifest(...)` - Create JSON manifest with all analysis data

**Output**: Separated stem files + JSON manifest

### 2. Instrumental & Vocal Builder Agent

**Purpose**: Create different mix-downs from separated stems.

**Responsibilities**:
- Build instrumental version (all stems except vocals)
- Build karaoke version (reduced vocals + backing)
- Build acapella version (vocals only)
- Audio normalization to consistent levels
- Metadata tagging (ID3/RIFF tags)
- Filename generation with metadata

**Key Methods**:
- `build_instrumental(stems, output_dir)` - Create instrumental mix
- `build_karaoke(stems, output_dir)` - Create karaoke mix
- `build_acapella(stems, output_dir)` - Create acapella version
- `normalize_audio(audio, target_db)` - Normalize audio levels
- `apply_metadata(audio_path, metadata)` - Tag audio files

**Output**: Instrumental.wav, Karaoke.wav, Acapella.wav with metadata

### 3. Loop/One-Shot & MIDI Generator Agent

**Purpose**: Create reusable sample content from stems.

**Responsibilities**:
- Slice stems into loops based on bar grid
- Extract drum one-shots using onset detection
- Classify drum hits (kick, snare, hihat, etc.)
- Rank loops by quality metrics
- Generate MIDI from melodic stems
- Organize outputs by category

**Key Methods**:
- `slice_loops(stem_path, bar_grid, output_dir, stem_name)` - Create loops
- `extract_oneshots(drums_path, output_dir)` - Extract drum hits
- `rank_loops(loops)` - Quality ranking
- `generate_midi(melodic_stem, output_dir, stem_name)` - MIDI generation
- `classify_drum_hit(audio, sample_rate)` - Classify drum types

**Output**: Loops (organized by stem), one-shots (organized by type), MIDI files

### 4. Lyric Extraction & Sync Agent

**Purpose**: Extract and synchronize lyrics from vocals.

**Responsibilities**:
- Speech-to-text using Whisper or similar
- Timestamp extraction (line-level and word-level)
- Synchronization with bar grid
- Lyric cleaning and formatting
- Multi-format export (LRC, SRT, JSON)

**Key Methods**:
- `extract_lyrics(vocals_path)` - STT extraction with timestamps
- `sync_lyrics(lyrics, bar_grid)` - Align to musical bars
- `export_lrc(lyrics, output_dir)` - Export LRC format (karaoke)
- `export_srt(lyrics, output_dir)` - Export SRT format (subtitles)
- `export_json(lyrics, output_dir)` - Export JSON format

**Output**: lyrics.lrc, lyrics.srt, lyrics.json

### 5. Visualizer & Video Export Agent

**Purpose**: Create engaging video content with visualizations and lyrics.

**Responsibilities**:
- Generate music-reactive visualizations
- Support multiple visualization styles (waveform, spectrum, bars, circular)
- Overlay synchronized lyrics on video
- Composite with backgrounds
- Video encoding with metadata
- Thumbnail generation

**Key Methods**:
- `create_visualizer(audio_path, style)` - Generate visualization frames
- `overlay_lyrics_on_frames(frames, lyrics_path, audio_path)` - Add lyrics
- `composite_background(frames, background_path)` - Add background
- `export_video(audio_path, visuals, output_dir, metadata)` - Encode video
- `generate_thumbnail(video_path, output_dir)` - Create thumbnail

**Output**: video.mp4, thumbnail.jpg

### 6. Metadata & Pack Export Agent

**Purpose**: Final organization and packaging of the sample pack.

**Responsibilities**:
- Collect metadata from all sources
- Create consistent folder structure
- Organize files by category
- Rename files with descriptive, metadata-based names
- Generate metadata sheets (JSON, CSV, TXT)
- Create README documentation
- Export as ZIP archive
- Pack validation and statistics

**Key Methods**:
- `collect_metadata(sources)` - Consolidate metadata
- `create_pack_structure(pack_name, base_dir)` - Create folders
- `organize_files(files, pack_dir)` - Organize and copy files
- `rename_files_with_metadata(pack_dir, metadata)` - Descriptive naming
- `generate_metadata_sheet(metadata, output_dir)` - Create sheets
- `generate_readme(pack_name, metadata, pack_dir)` - Create README
- `create_pack(pack_dir, output_dir)` - Create ZIP

**Output**: Organized pack folder + pack.zip

### 7. UI/UX Agent

**Purpose**: Web interface and pipeline orchestration.

**Responsibilities**:
- Create Gradio web interface
- Coordinate all agents in a pipeline
- Manage workflow state and progress
- Provide preview functionality
- Collect user metadata input
- Handle file uploads and downloads
- Progress tracking and error handling

**Key Methods**:
- `create_interface()` - Build Gradio UI
- `run_pipeline(input_data)` - Execute full pipeline
- `preview_results(agent_output, agent_type)` - Generate previews
- `collect_user_metadata(form_data)` - Collect user input
- `trigger_export(pack_config)` - Finalize and export
- `update_progress(stage, progress, message)` - Track progress

**Output**: Web interface + orchestration logic

## Base Agent Class

All agents inherit from `BaseAgent`, which provides:

### Common Functionality
- **Logging**: Structured logging with agent name
- **Error Handling**: Standardized error responses
- **Configuration**: Config management with defaults
- **Validation**: Input validation helpers
- **File Management**: Directory creation utilities
- **Response Formatting**: Success/error response helpers

### Abstract Method
- `process(input_data)` - Main processing method (must be implemented by subclasses)

### Example Usage

```python
from backend.engine.agents import StemSeparationAgent

# Initialize agent with config
agent = StemSeparationAgent(config={
    "model": "htdemucs",
    "device": "cpu"
})

# Process audio
result = agent.process({
    "audio_path": "/path/to/song.mp3",
    "output_dir": "/path/to/output"
})

# Check result
if result["status"] == "success":
    stems = result["data"]["stems"]
    manifest = result["data"]["manifest_path"]
    print(f"Stems separated: {stems}")
```

## Pipeline Flow

The typical pipeline flow:

```
1. Audio Input
   ↓
2. StemSeparationAgent
   → Stems + Manifest
   ↓
3. VocalBuilderAgent (parallel)
   → Instrumental, Karaoke, Acapella
   ↓
4. LoopGeneratorAgent (parallel)
   → Loops, One-shots, MIDI
   ↓
5. LyricExtractionAgent (parallel, if vocals)
   → Lyrics (LRC, SRT, JSON)
   ↓
6. VideoExportAgent (optional)
   → Video with visualizations
   ↓
7. PackExportAgent
   → Organized pack folder + ZIP
```

**Note**: Some agents can run in parallel (steps 3-6) as they don't depend on each other's outputs.

## Data Flow

### Manifest JSON Schema

The manifest is the primary data structure passed between agents:

```json
{
  "audio_file": "path/to/original.mp3",
  "duration": 180.5,
  "sample_rate": 44100,
  "bpm": 120.0,
  "key": "C Major",
  "camelot_key": "8B",
  "time_signature": "4/4",
  "bar_grid": [0.0, 2.0, 4.0, 6.0, ...],
  "stems": {
    "vocals": "path/to/vocals.wav",
    "drums": "path/to/drums.wav",
    "bass": "path/to/bass.wav",
    "other": "path/to/other.wav"
  },
  "generated_at": "2026-01-17T22:21:04Z",
  "generator_version": "1.0.0"
}
```

### Agent Response Format

All agents return responses in this format:

```python
{
    "status": "success",  # or "error"
    "message": "Processing completed successfully",
    "data": {
        # Agent-specific output data
    },
    "agent": "StemSeparationAgent",
    "version": "1.0.0",
    "timestamp": "2026-01-17T22:21:04Z"
}
```

## Implementation Status

### Current Status: **Stub/Interface Phase**

All agents are currently **stub implementations** with:
- ✅ Complete class structure
- ✅ Comprehensive docstrings
- ✅ Type hints for all methods
- ✅ TODO comments marking implementation areas
- ✅ Example usage in docstrings
- ⏳ Core functionality (marked as TODO)

### Next Steps for Implementation

For each agent, implement the TODO sections:

1. **StemSeparationAgent**
   - Integrate Demucs for stem separation
   - Implement BPM detection with librosa
   - Implement key detection
   - Implement bar grid generation

2. **VocalBuilderAgent**
   - Implement audio mixing functions
   - Implement normalization
   - Integrate mutagen for metadata tagging

3. **LoopGeneratorAgent**
   - Implement onset detection for slicing
   - Implement quality ranking algorithm
   - Integrate pitch detection for MIDI
   - Implement mido for MIDI export

4. **LyricExtractionAgent**
   - Integrate OpenAI Whisper for STT
   - Implement lyric synchronization
   - Implement format exporters (LRC, SRT)

5. **VideoExportAgent**
   - Integrate opencv-python or moviepy
   - Implement visualization generators
   - Implement video encoding
   - Implement lyric overlay

6. **PackExportAgent**
   - Implement folder structure creation
   - Implement file organization logic
   - Implement ZIP creation
   - Implement README generation

7. **UIAgent**
   - Create Gradio interface
   - Implement pipeline orchestration
   - Implement preview components
   - Implement progress tracking

## Dependencies

### Currently Required (Already in Project)
- numpy - Numerical computing
- scipy - Scientific computing
- soundfile - Audio I/O
- librosa - Audio analysis

### Future Dependencies (Marked as TODO)
- **demucs** - Stem separation (Agent 1)
- **openai-whisper** - Speech-to-text (Agent 4)
- **mido** - MIDI file creation (Agent 3)
- **opencv-python** or **moviepy** - Video processing (Agent 5)
- **mutagen** - Audio metadata tagging (Agent 2)
- **gradio** - Web UI (Agent 7)

## Configuration

Each agent accepts a configuration dictionary. Example:

```python
config = {
    # StemSeparationAgent
    "model": "htdemucs",
    "device": "cpu",
    
    # VocalBuilderAgent
    "normalize_db": -3.0,
    "karaoke_vocal_level": 0.3,
    
    # LoopGeneratorAgent
    "min_loop_bars": 4,
    "max_loop_bars": 8,
    "generate_midi": True,
    
    # LyricExtractionAgent
    "model": "base",
    "language": "en",
    "word_level": True,
    
    # VideoExportAgent
    "style": "waveform",
    "fps": 30,
    "resolution": (1920, 1080),
    
    # PackExportAgent
    "include_readme": True,
    "compression_level": 9,
    
    # UIAgent
    "theme": "default",
    "share": False
}
```

## Testing

To validate the agent structure (current phase):

```python
# Test imports
from backend.engine.agents import (
    StemSeparationAgent,
    VocalBuilderAgent,
    LoopGeneratorAgent,
    LyricExtractionAgent,
    VideoExportAgent,
    PackExportAgent,
    UIAgent
)

# Test instantiation
agents = [
    StemSeparationAgent(),
    VocalBuilderAgent(),
    LoopGeneratorAgent(),
    LyricExtractionAgent(),
    VideoExportAgent(),
    PackExportAgent(),
    UIAgent()
]

print("All agents instantiated successfully!")
```

## Future Enhancements

1. **Agent Orchestration**
   - Pipeline manager for automatic agent coordination
   - Dependency resolution
   - Parallel execution where possible

2. **Progress Tracking**
   - Real-time progress callbacks
   - Detailed stage-by-stage updates
   - ETA calculations

3. **Caching**
   - Cache intermediate results
   - Avoid reprocessing on parameter changes
   - Resume interrupted pipelines

4. **Quality Control**
   - Automated quality checks
   - Validation of outputs
   - Error recovery strategies

5. **Cloud Integration**
   - Cloud storage support (S3, GCS)
   - Distributed processing
   - API endpoints for remote access

6. **Preset System**
   - Save/load agent configurations
   - Genre-specific presets
   - User customization

## Contributing

When extending or implementing agents:

1. Follow the existing pattern in `base_agent.py`
2. Add comprehensive docstrings with examples
3. Include type hints for all parameters and returns
4. Use TODO comments for future expansion areas
5. Test independently before pipeline integration
6. Update this README with significant changes

## License

[Same as parent project]

---

**Status**: Phase 1 Complete - Agent Interfaces and Structure Defined
**Next Phase**: Implementation of core agent functionality
