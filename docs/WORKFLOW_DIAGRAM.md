# Loop Architect Workflow Diagram

## Complete Workflow Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOOP ARCHITECT WORKFLOW                       │
│                     Music/Video Pack Generator                   │
└─────────────────────────────────────────────────────────────────┘

  ┌───────────────┐
  │ 1. Input      │ ← Upload audio file or URL
  │    Handling   │   Validate format & size
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 2. Stem       │ ← Traditional: vocals, drums, bass, guitar, piano, other
  │    Separation │   OR SAM Audio: "saxophone", "crowd noise", etc.
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 3. Instrument │ ← Mix non-vocal stems
  │    Builder    │   Normalize & balance levels
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 4. Audio      │ ← BPM detection (librosa.beat_track)
  │    Analysis   │   Key detection (chromagram + K-S algorithm)
  │               │   Harmonic recommendations (Camelot wheel)
  │               │   Time signature detection
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 5. Slicing    │ ← Bar-aligned loops (1, 2, 4 bars)
  │               │   OR One-shots (onset detection)
  │               │   MIDI generation for melodic stems
  │               │   Crossfade, transpose, FX
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 6. Lyric      │ ← [STUB] Whisper/STT integration
  │    Extraction │   Word-level timestamped lyrics
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 7. Visualizer │ ← [STUB] Audio-reactive waveform
  │               │   Frequency spectrum visualization
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 8. Video      │ ← [STUB] ffmpeg/moviepy rendering
  │    Composer   │   Overlay lyrics on visualizations
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 9. Metadata   │ ← Tag WAV files with BPM/key
  │    Tagging    │   Add artist, title, comments
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 10. Pack      │ ← Organize into folders:
  │     Building  │     WAV/ (loops & one-shots)
  │               │     MIDI/ (generated MIDI)
  │               │     Stems/ (original stems)
  │               │   Create README.md & metadata.txt
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ 11. Export    │ ← ZIP entire pack
  │               │   Ready for download
  └───────┬───────┘
          │
          ▼
     📦 Final Pack
```

## Module Dependencies

```
Input Handler
  └──> Audio Analyzer
         └──> Stem Separation (External)
                └──> Instrumental Builder
                       └──> Slicer
                              ├──> Lyric Extractor (Optional)
                              ├──> Visualizer (Optional)
                              └──> Video Composer (Optional)
                                     └──> Metadata Tagger
                                            └──> Pack Builder
                                                   └──> Exporter
```

## Data Flow

```
User Input
    ↓
Audio File → Stems Dict → Analysis Results → Sliced Files → Tagged Files → ZIP Package
    ↓           ↓              ↓                ↓               ↓            ↓
 Validation  Separation    BPM/Key         Loops/Shots      Metadata     Download
```

## File Structure Output

```
Loop_Architect_Pack/
├── WAV/
│   ├── vocals_4Bar_001_CMaj_128BPM.wav
│   ├── drums_4Bar_001_CMaj_128BPM.wav
│   └── ...
├── MIDI/
│   ├── vocals_MELODY_CMaj_128BPM.mid
│   ├── bass_MELODY_CMaj_128BPM.mid
│   └── ...
├── Stems/
│   ├── vocals.wav
│   ├── drums.wav
│   ├── bass.wav
│   └── Loop_Architect_Pack_Instrumental.wav
├── README.md (Usage instructions)
└── metadata.txt (Pack information)
```

## Module Status

| Module | Status | Dependencies |
|--------|--------|-------------|
| Input Handler | ✅ Complete | os, tempfile |
| Audio Analyzer | ✅ Complete | librosa, numpy |
| Instrumental Builder | ✅ Complete | soundfile, numpy |
| Slicer | ✅ Complete | librosa, soundfile, scipy |
| Lyric Extractor | 🔶 Stub | (openai-whisper) |
| Visualizer | 🔶 Stub | (matplotlib, PIL) |
| Video Composer | 🔶 Stub | (ffmpeg-python) |
| Metadata Tagger | ✅ Complete | mutagen (optional) |
| Pack Builder | ✅ Complete | os, shutil |
| Exporter | ✅ Complete | zipfile |

## Workflow Configuration

All workflow modules are configured via `WorkflowConfig`:

```python
@dataclass
class WorkflowConfig:
    # Separation
    separation_mode: 'traditional' | 'sam-audio'
    sam_prompts: Optional[List[str]]
    
    # Musical
    manual_bpm: Optional[float]
    transpose_semitones: int
    time_signature: str
    
    # Slicing
    loop_type: '1-bar' | '2-bar' | '4-bar' | 'one-shots'
    one_shot_sensitivity: float
    crossfade_ms: int
    
    # FX
    normalize_peak: float
    apply_modulation: bool
    # ... more FX settings
    
    # Output
    include_instrumental: bool
    include_midi: bool
    include_lyrics: bool  # Stub
    include_visualizer: bool  # Stub
    include_video: bool  # Stub
    
    # Metadata
    pack_name: str
    artist_name: Optional[str]
    description: Optional[str]
```

## Extensibility

The modular architecture allows easy addition of new processing steps:

1. **Create Module**: Implement `WorkflowModule` protocol
2. **Register**: Add to `WorkflowOrchestrator`
3. **Configure**: Add settings to `WorkflowConfig`
4. **Process**: Module receives `WorkflowContext`, updates it, returns `ModuleResult`

Example:

```python
class CustomProcessor:
    def get_name(self) -> str:
        return "Custom Processor"
    
    def is_required(self) -> bool:
        return False
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        # Your processing logic
        return ModuleResult(success=True, message="Processed!")

# Register in orchestrator
orchestrator.register_module(CustomProcessor())
```

---

**Built with modular, AI-native architecture** 🤖✨
