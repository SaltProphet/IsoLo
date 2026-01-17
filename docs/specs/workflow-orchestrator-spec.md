# Workflow Orchestrator Specification

## Purpose

The Workflow Orchestrator is the core system that coordinates all steps in the music/video sample pack generation process. It connects modular processing modules in a defined sequence, handles errors gracefully, and reports progress throughout the workflow.

## Requirements

### Functional Requirements

1. **Sequential Processing**: Execute workflow steps in order:
   - Input Handling → Stem Separation → Instrumental Building → Audio Analysis → Slicing → Lyric Extraction → Visualization → Video Composition → Metadata Tagging → Pack Building → Export

2. **Modular Architecture**: Each workflow step is an independent, replaceable module with a well-defined interface

3. **Progress Tracking**: Report progress at each step with percentage completion and status messages

4. **Error Handling**: Gracefully handle errors at any step, with option to continue or abort

5. **Configurable Steps**: Enable/disable optional steps (e.g., skip video generation, skip MIDI export)

6. **State Management**: Maintain workflow state including:
   - Current step
   - Completed steps
   - Failed steps
   - Generated files
   - Metadata

### Non-Functional Requirements

- **Performance**: Process typical 3-minute song in < 5 minutes (excluding video generation)
- **Extensibility**: Easy to add new processing modules
- **Type Safety**: Full Python type hints for all interfaces
- **Testability**: Each module independently testable

## Architecture

### Workflow Steps

```
1. Input Handling
   ├── Upload audio file or provide URL
   └── Validate format and size

2. Stem Separation
   ├── Traditional stems (vocals, drums, bass, etc.)
   └── OR SAM Audio named isolation

3. Instrumental Builder
   └── Mix non-vocal stems with normalization

4. BPM/Key/Bar Grid Detection
   ├── Detect tempo
   ├── Detect key
   ├── Calculate harmonic recommendations
   └── Detect time signature

5. Loop & One-Shot Slicing
   ├── Bar-aligned loops (1, 2, 4 bars)
   ├── One-shots (onset detection)
   └── MIDI generation for melodic stems

6. Lyric Extraction/Sync (STUB)
   ├── Run Whisper/STT on vocals
   └── Output timestamped lyrics

7. Visualizer Generation (STUB)
   └── Audio-reactive waveform/background

8. Video Composer (STUB)
   └── Overlay visuals/lyrics, render video

9. Metadata Tagging
   ├── UI form for pack metadata
   └── Tag all audio files with BPM/Key

10. Pack Structure
    ├── Organize files into folders
    ├── Rename with metadata
    └── Create metadata sheet/README

11. Export/Download
    └── ZIP full pack for user
```

### Component Structure

#### WorkflowOrchestrator Class

```python
class WorkflowOrchestrator:
    """Coordinates execution of all workflow modules."""
    
    def __init__(self, config: WorkflowConfig):
        """Initialize with configuration."""
        
    def execute(self, input_file: str) -> WorkflowResult:
        """Execute full workflow."""
        
    def get_status(self) -> WorkflowStatus:
        """Get current workflow status."""
```

#### Module Interface

All modules implement the `WorkflowModule` protocol:

```python
class WorkflowModule(Protocol):
    """Protocol for workflow modules."""
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """Process this workflow step."""
        
    def get_name(self) -> str:
        """Get module name."""
        
    def is_required(self) -> bool:
        """Whether this module is required."""
```

### Data Flow

```python
WorkflowContext:
  - input_file: str
  - temp_dir: str
  - config: WorkflowConfig
  - stems: Dict[str, AudioData]
  - instrumental: AudioData
  - bpm: float
  - key: str
  - time_signature: str
  - sliced_files: List[str]
  - midi_files: List[str]
  - lyrics: Optional[LyricData]
  - visualizer: Optional[VisualizerData]
  - video: Optional[str]
  - metadata: Dict[str, Any]
  - pack_structure: PackStructure
```

### State Management

Workflow status tracked through:
- **Pending**: Not started
- **Running**: Currently executing
- **Complete**: Successfully finished
- **Failed**: Error occurred
- **Skipped**: Optional step skipped

## API Contracts

### WorkflowConfig

```python
@dataclass
class WorkflowConfig:
    """Configuration for workflow execution."""
    
    # Separation settings
    separation_mode: Literal['traditional', 'sam-audio']
    sam_prompts: Optional[List[str]]
    
    # Musical settings
    manual_bpm: Optional[float]
    transpose_semitones: int
    time_signature: str
    
    # Slicing settings
    loop_type: Literal['1-bar', '2-bar', '4-bar', 'one-shots']
    one_shot_sensitivity: float
    crossfade_ms: int
    
    # FX settings
    normalize_peak: float
    apply_modulation: bool
    
    # Output settings
    include_instrumental: bool
    include_midi: bool
    include_lyrics: bool
    include_visualizer: bool
    include_video: bool
    
    # Metadata
    pack_name: str
    artist_name: Optional[str]
    description: Optional[str]
```

### WorkflowResult

```python
@dataclass
class WorkflowResult:
    """Result of workflow execution."""
    
    success: bool
    output_zip: Optional[str]
    error: Optional[str]
    steps_completed: List[str]
    steps_failed: List[str]
    execution_time: float
    generated_files: List[str]
```

### WorkflowStatus

```python
@dataclass
class WorkflowStatus:
    """Current status of workflow."""
    
    current_step: str
    current_step_index: int
    total_steps: int
    progress_percent: float
    status_message: str
    is_complete: bool
    has_error: bool
```

## Module Specifications

### 1. Input Handler

**Purpose**: Validate and prepare input audio

**Interface**:
```python
def handle_input(file_path: str, context: WorkflowContext) -> ModuleResult:
    """
    Validate audio file and prepare for processing.
    
    Returns:
        ModuleResult with validated file path
    """
```

### 2. Stem Separator

**Purpose**: Separate audio into stems using Demucs or SAM Audio

**Interface**:
```python
def separate_stems(context: WorkflowContext) -> ModuleResult:
    """
    Separate audio into stems based on config.
    
    Updates context.stems with separated audio data.
    """
```

### 3. Instrumental Builder

**Purpose**: Mix non-vocal stems into instrumental track

**Interface**:
```python
def build_instrumental(context: WorkflowContext) -> ModuleResult:
    """
    Mix non-vocal stems and normalize.
    
    Updates context.instrumental with mixed audio.
    """
```

### 4. Audio Analyzer

**Purpose**: Detect BPM, key, and time signature

**Interface**:
```python
def analyze_audio(context: WorkflowContext) -> ModuleResult:
    """
    Detect musical attributes.
    
    Updates context.bpm, context.key, context.time_signature.
    """
```

### 5. Slicer

**Purpose**: Slice stems into loops and one-shots

**Interface**:
```python
def slice_audio(context: WorkflowContext) -> ModuleResult:
    """
    Slice all stems based on settings.
    
    Updates context.sliced_files and context.midi_files.
    """
```

### 6. Lyric Extractor (STUB)

**Purpose**: Extract and sync lyrics from vocals

**Interface**:
```python
def extract_lyrics(context: WorkflowContext) -> ModuleResult:
    """
    STUB: Extract timestamped lyrics using Whisper.
    
    Updates context.lyrics (currently returns stub data).
    """
```

### 7. Visualizer Generator (STUB)

**Purpose**: Generate audio-reactive visualizations

**Interface**:
```python
def generate_visualizer(context: WorkflowContext) -> ModuleResult:
    """
    STUB: Generate audio-reactive waveform visualization.
    
    Updates context.visualizer (currently returns stub data).
    """
```

### 8. Video Composer (STUB)

**Purpose**: Compose video with visualizations and lyrics

**Interface**:
```python
def compose_video(context: WorkflowContext) -> ModuleResult:
    """
    STUB: Render video with ffmpeg/moviepy.
    
    Updates context.video (currently returns stub data).
    """
```

### 9. Metadata Tagger

**Purpose**: Tag all files with metadata

**Interface**:
```python
def tag_metadata(context: WorkflowContext) -> ModuleResult:
    """
    Add BPM, key, and custom metadata to all audio files.
    
    Updates file tags in place.
    """
```

### 10. Pack Builder

**Purpose**: Organize files into pack structure

**Interface**:
```python
def build_pack(context: WorkflowContext) -> ModuleResult:
    """
    Create folder structure and organize files.
    
    Updates context.pack_structure with final layout.
    """
```

### 11. Exporter

**Purpose**: ZIP and prepare for download

**Interface**:
```python
def export_pack(context: WorkflowContext) -> ModuleResult:
    """
    Create final ZIP file.
    
    Returns path to ZIP file.
    """
```

## Acceptance Criteria

- [x] Workflow executes all 11 steps sequentially
- [x] Each step is a separate, modular component
- [x] Progress is reported at each step
- [x] Errors are caught and handled gracefully
- [x] Advanced features (lyrics, visualizer, video) are stubs
- [x] Final pack is downloadable as ZIP
- [x] All files are properly organized and named
- [x] Metadata is correctly applied to audio files

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock WorkflowContext for isolation
- Verify correct error handling

### Integration Tests
- Test full workflow end-to-end
- Verify file generation
- Check pack structure

### Manual Testing
- Upload various audio formats
- Test with different configuration options
- Verify downloadable pack quality

## Dependencies

### Existing
- librosa (audio analysis)
- numpy, scipy (signal processing)
- soundfile (audio I/O)
- gradio (web interface)

### New (if needed)
- mutagen (metadata tagging)
- zipfile (built-in, pack export)

### Future (for full implementation)
- openai-whisper (lyric extraction)
- ffmpeg-python (video composition)
- moviepy (video editing)

## Future Considerations

### Phase 2 Enhancements
- Parallel processing of independent steps
- Caching of intermediate results
- Resume from failed step
- Multiple output formats
- Real-time preview
- Collaborative editing

### Advanced Features Implementation
- Replace lyric extractor stub with Whisper integration
- Replace visualizer stub with real-time audio visualization
- Replace video composer stub with ffmpeg pipeline
- Add cloud storage integration
- Add batch processing for multiple files

## Implementation Notes

### Priority Order
1. Core workflow infrastructure (orchestrator + modules)
2. File organization and metadata
3. Integration with existing UI
4. Stub implementation for advanced features
5. Documentation and examples

### Modular Design Benefits
- Each module can be developed independently
- Easy to test in isolation
- Simple to replace or upgrade modules
- Clear interfaces between components
- Extensible for future features

---

**Status**: Ready for implementation
**Last Updated**: 2026-01-17
