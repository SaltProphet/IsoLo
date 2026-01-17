# Sample Pack Generator - Modular Agent System Specification

## Purpose

Create a modular foundation for a music/video sample pack generator using a multi-agent architecture. Each agent handles a specific aspect of the audio/video processing pipeline, from stem separation to final pack export. This specification defines the architecture, interfaces, and responsibilities for each agent module.

## Requirements

### Functional Requirements

1. **Modular Architecture**: Each agent must be independent, with clear interfaces and minimal coupling
2. **Agent-Based Processing**: Seven distinct agents, each handling specific processing tasks
3. **JSON-Based Communication**: Agents communicate via JSON manifests and metadata files
4. **Extensible Design**: Easy to add new agents or extend existing ones
5. **Type-Safe Interfaces**: All functions must have proper type hints
6. **Documentation**: Each agent must have comprehensive docstrings and API documentation
7. **Error Handling**: Graceful error handling with informative error messages

### Non-Functional Requirements

- **Modularity**: Each agent in a separate file under `backend/engine/agents/`
- **Performance**: Designed for batch processing of audio/video files
- **Maintainability**: Clear separation of concerns, well-documented code
- **Testability**: Each agent can be tested independently

## Architecture

### Directory Structure

```
backend/
├── engine/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Base class for all agents
│   │   ├── stem_separation_agent.py   # Agent 1
│   │   ├── vocal_builder_agent.py     # Agent 2
│   │   ├── loop_generator_agent.py    # Agent 3
│   │   ├── lyric_extraction_agent.py  # Agent 4
│   │   ├── video_export_agent.py      # Agent 5
│   │   ├── pack_export_agent.py       # Agent 6
│   │   └── ui_agent.py                # Agent 7 (interface stub)
│   └── README.md
```

### Agent Responsibilities

#### 1. Stem Separation & Core Analysis Agent
- **Purpose**: Ingest audio, perform stem separation, analyze musical properties
- **Inputs**: Audio file path
- **Outputs**: Stems (wav files), JSON manifest with BPM, key, bar grid, duration
- **Key Functions**:
  - `separate_stems(audio_path: str, output_dir: str) -> Dict[str, str]`
  - `analyze_audio(audio_path: str) -> Dict[str, Any]`
  - `detect_bpm(audio_path: str) -> float`
  - `detect_key(audio_path: str) -> str`
  - `generate_manifest(audio_path: str, output_dir: str) -> str`

#### 2. Instrumental & Vocal Builder Agent
- **Purpose**: Combine stems to create instrumental, karaoke, acapella versions
- **Inputs**: Stem files, manifest JSON
- **Outputs**: Combined audio files with proper normalization and metadata
- **Key Functions**:
  - `build_instrumental(stems: Dict[str, str], output_path: str) -> str`
  - `build_karaoke(stems: Dict[str, str], output_path: str) -> str`
  - `build_acapella(stems: Dict[str, str], output_path: str) -> str`
  - `normalize_audio(audio_path: str) -> np.ndarray`
  - `apply_metadata(audio_path: str, metadata: Dict[str, str]) -> None`

#### 3. Loop/One-Shot & MIDI Generator Agent
- **Purpose**: Slice stems into loops, extract drum one-shots, generate MIDI
- **Inputs**: Stems, manifest with bar grid
- **Outputs**: Loop files, one-shot samples, MIDI files, ranked by quality
- **Key Functions**:
  - `slice_loops(stem_path: str, bar_grid: List[float], output_dir: str) -> List[str]`
  - `extract_oneshots(drums_path: str, output_dir: str) -> List[str]`
  - `rank_loops(loops: List[str]) -> List[Tuple[str, float]]`
  - `generate_midi(melodic_stem: str, output_path: str) -> Optional[str]`

#### 4. Lyric Extraction & Sync Agent
- **Purpose**: Extract lyrics from vocals using speech-to-text, sync with timestamps
- **Inputs**: Vocals stem, manifest
- **Outputs**: LRC/SRT files with timestamped lyrics
- **Key Functions**:
  - `extract_lyrics(vocals_path: str) -> List[Tuple[float, str]]`
  - `sync_lyrics(lyrics: List[Tuple[float, str]], bar_grid: List[float]) -> List[Tuple[float, str]]`
  - `export_lrc(lyrics: List[Tuple[float, str]], output_path: str) -> str`
  - `export_srt(lyrics: List[Tuple[float, str]], output_path: str) -> str`

#### 5. Visualizer & Video Export Agent
- **Purpose**: Generate music-reactive visualizations and export videos
- **Inputs**: Audio files, lyrics, visual preferences
- **Outputs**: Video files with waveforms, lyrics overlay, tagged metadata
- **Key Functions**:
  - `generate_waveform(audio_path: str, output_path: str) -> str`
  - `create_visualizer(audio_path: str, style: str) -> np.ndarray`
  - `overlay_lyrics(video_path: str, lyrics_path: str, output_path: str) -> str`
  - `export_video(audio_path: str, visuals: np.ndarray, output_path: str, metadata: Dict) -> str`

#### 6. Metadata & Pack Export Agent
- **Purpose**: Collect metadata, organize files, create folder structure, export pack
- **Inputs**: All generated files, user metadata
- **Outputs**: Organized folder structure, metadata sheets, zipped pack
- **Key Functions**:
  - `collect_metadata(sources: List[str]) -> Dict[str, Any]`
  - `organize_files(files: List[str], output_structure: Dict) -> str`
  - `generate_metadata_sheet(metadata: Dict, output_path: str) -> str`
  - `create_pack(pack_dir: str, output_path: str) -> str`

#### 7. UI/UX Agent
- **Purpose**: Web interface to connect all agents, preview results, control workflow
- **Inputs**: User interactions, agent outputs
- **Outputs**: UI state, user selections, export triggers
- **Key Functions**:
  - `create_interface() -> Any`  # Gradio interface
  - `preview_results(agent_output: Dict) -> Any`
  - `collect_user_metadata() -> Dict[str, str]`
  - `trigger_export(pack_config: Dict) -> str`

## API Contracts

### Base Agent Class

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

class BaseAgent(ABC):
    """
    Base class for all sample pack generator agents.
    
    Provides common functionality for logging, error handling,
    and file management.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the agent with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method - must be implemented by subclasses.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing output data and metadata
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data before processing."""
        pass
    
    def log_info(self, message: str) -> None:
        """Log informational message."""
        pass
    
    def log_error(self, message: str) -> None:
        """Log error message."""
        pass
```

### Manifest JSON Schema

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

## Implementation Notes

### Each Agent Module Should Include:

1. **Class Definition**: Main agent class inheriting from `BaseAgent`
2. **Type Hints**: All parameters and return types must be typed
3. **Docstrings**: Comprehensive documentation for all public methods
4. **TODO Comments**: Mark areas for future expansion
5. **Error Handling**: Try/except blocks with informative errors
6. **Example Usage**: Docstring examples showing how to use the agent

### Code Style

- Follow PEP 8 style guidelines
- Use type hints from `typing` module
- Maximum line length: 100 characters
- Use descriptive variable names
- Add comments for complex logic

## Acceptance Criteria

- [x] Directory structure created under `backend/engine/agents/`
- [ ] Base agent class implemented with common functionality
- [ ] All 7 agent modules created with proper structure
- [ ] Each agent has comprehensive docstrings and type hints
- [ ] TODO comments mark areas for future expansion
- [ ] All modules have proper `__init__.py` for Python imports
- [ ] README.md documents the architecture and usage
- [ ] No implementation dependencies on external AI models (stubs for Demucs, Whisper, etc.)
- [ ] All agents can be imported without errors

## Testing Strategy

For this initial implementation (stubs/interfaces):
- Validate that all modules can be imported
- Verify class inheritance structure
- Check that type hints are correct
- Ensure docstrings are present and comprehensive

Future testing (when implemented):
- Unit tests for each agent's core functions
- Integration tests for agent pipelines
- End-to-end tests for complete pack generation

## Dependencies

### Required (Already in project):
- numpy
- scipy
- soundfile
- librosa

### Future Dependencies (marked as TODO):
- demucs (stem separation)
- openai-whisper (lyric extraction)
- mido (MIDI generation)
- opencv-python (video export)
- moviepy (video processing)

## Future Considerations

1. **Agent Orchestration**: Implement a pipeline manager to coordinate agents
2. **Progress Tracking**: Add callbacks for progress updates
3. **Caching**: Cache intermediate results to avoid reprocessing
4. **Parallel Processing**: Support parallel processing of multiple files
5. **Cloud Integration**: Support for cloud storage and processing
6. **Quality Control**: Automated quality checks for generated content
7. **Preset System**: Save and load agent configurations as presets

## References

- Existing codebase: `backend/app.py` for audio processing patterns
- SAM Audio integration: `backend/sam_audio_integration.py` for agent pattern
- Project standards: `.github/copilot-instructions.md`
