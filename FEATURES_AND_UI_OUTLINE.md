# SAM Audio Integration - Features & UI Menu Outline

## Current Status

✅ **Backend Implementation**: Complete (as of commit 16ef6e2)
⏭️ **UI Implementation**: Planned for future phase

---

## Available Features (Backend API - Ready Now)

### 1. Named Sound Isolation

**What it does**: Isolate ANY sound from audio files by describing it in natural language.

**Available via Python API**:
```python
from sam_audio_integration import SAMAudioSeparator

separator = SAMAudioSeparator()
sr, audio = separator.separate_by_description("song.mp3", "lead vocals")
```

**Examples of what can be isolated**:
- Musical instruments: "saxophone solo", "piano melody", "electric guitar"
- Vocals: "lead vocals", "background vocals", "male voice", "female voice"
- Environmental: "crowd applause", "rain sounds", "bird chirping"
- Sound effects: "door slam", "phone ringing", "footsteps"

### 2. Batch Sound Isolation

**What it does**: Isolate multiple sounds from the same audio file in one operation.

**Available via Python API**:
```python
results = separator.separate_multiple(
    "band.wav",
    descriptions=["vocals", "guitar", "drums", "bass"]
)
```

### 3. Integration with Loop Architect

**What it does**: Combines SAM Audio with existing Loop Architect features (BPM detection, key detection, etc.)

**Available via Python API**:
```python
from app import separate_named_sounds

stems_dict, bpm, key, harmonic_recs = separate_named_sounds(
    "song.mp3",
    "lead vocals, electric guitar, bass line, drum beat"
)
```

### 4. Traditional Stem Separation

**What it does**: Standard separation into vocals, drums, bass, other, guitar, piano (unchanged from original).

**Available via Python API**:
```python
from app import separate_stems

vocals, drums, bass, other, guitar, piano, bpm, key, recs = separate_stems("song.mp3")
```

---

## Planned UI Features (Future Phase)

When the UI is implemented in the Gradio interface, users will have access to:

### Main Menu Structure

```
┌─────────────────────────────────────────────────────────┐
│              🎵 Loop Architect (Pro Edition)            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  1. Upload & Analyze                                    │
│     ├─ Upload Song                                      │
│     ├─ Separation Mode Toggle: [Traditional / SAM Audio]│
│     └─ Separate Stems & Analyze Button                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  2. Separation Settings (New)                           │
│     ├─ Mode Selection:                                  │
│     │   • Traditional Stems (vocals, drums, bass, etc.) │
│     │   • SAM Audio (Named Sound Isolation)            │
│     │                                                    │
│     └─ SAM Audio Options (when selected):               │
│         ├─ Text Prompts Input (comma-separated)        │
│         ├─ Preset Prompt Templates [Dropdown]          │
│         └─ Model Quality: [Fast/Balanced/High Quality] │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  3. Global Musical Settings (Existing)                  │
│     ├─ BPM (auto-detected, editable)                   │
│     ├─ Detected Key                                     │
│     ├─ Harmonic Recommendations                         │
│     ├─ Transpose (Semitones)                           │
│     └─ Time Signature                                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  4. Global Slicing Settings (Existing)                  │
│     ├─ Loop Type (1 Bar / 2 Bar / 4 Bar / One-Shots)  │
│     ├─ One-Shot Sensitivity                            │
│     └─ Loop Crossfade (ms)                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  5. Global FX Settings (Existing)                       │
│     ├─ Normalize Peak to (dBFS)                        │
│     ├─ LFO Modulation (Pan/Level)                      │
│     ├─ LFO Modulation (Filter)                         │
│     └─ One-Shot Shaping                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  6. Review Stems & Slices (Enhanced)                    │
│     ├─ Tab for each isolated sound (dynamic)           │
│     ├─ Preview waveform                                │
│     ├─ Generated slices & MIDI                         │
│     └─ Slice individual stem button                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  7. Generate Pack (Existing)                            │
│     └─ SLICE ALL & GENERATE PACK Button               │
└─────────────────────────────────────────────────────────┘
```

---

## Detailed UI Features (Planned)

### 🆕 Feature 1: Separation Mode Toggle

**Location**: Section 1 - Upload & Analyze

**Options**:
- **Traditional Stems** (default)
  - Uses fixed categories: vocals, drums, bass, other, guitar, piano
  - Fast processing
  - No additional input needed
  
- **SAM Audio - Named Isolation**
  - Uses text prompts to describe sounds
  - Flexible - isolate any sound
  - Requires text input

**UI Element**: Radio button or toggle switch

---

### 🆕 Feature 2: Text Prompt Input

**Location**: Section 2 - Separation Settings (shown when SAM Audio mode selected)

**What it does**: Allows users to type descriptions of sounds they want to isolate

**UI Element**: Multi-line text area

**Input Format**: Comma-separated list of sound descriptions

**Examples**:
```
lead vocals, electric guitar, bass line, drum beat
```
```
saxophone solo, piano melody, audience applause
```
```
male voice, female voice, background music
```

**Features**:
- Real-time character count
- Placeholder text with examples
- Input validation (minimum 1 prompt required)
- Support for multiple prompts (batch processing)

---

### 🆕 Feature 3: Preset Prompt Templates

**Location**: Section 2 - Separation Settings

**What it does**: Quick-select common prompt combinations

**UI Element**: Dropdown menu

**Preset Options**:

**Music Production**:
- "Standard Band" → `lead vocals, electric guitar, bass guitar, drums`
- "Vocal Focus" → `lead vocals, background vocals, instrumental accompaniment`
- "Jazz Ensemble" → `saxophone, piano, upright bass, drums`
- "Orchestra" → `string section, brass section, woodwinds, percussion`

**Sound Design**:
- "Nature Sounds" → `bird chirping, water flowing, wind, leaves rustling`
- "Urban Environment" → `traffic, footsteps, talking, doors`
- "Foley Effects" → `door slam, glass breaking, phone ringing, footsteps`

**Podcast/Speech**:
- "Interview" → `host voice, guest voice, background music`
- "Narration" → `narrator voice, background ambience, music`

**Live Recording**:
- "Concert" → `lead vocals, instruments, crowd applause, crowd noise`
- "Street Performance" → `performer, audience, ambient city sounds`

**Custom**:
- "Custom..." → Opens text input for manual entry

---

### 🆕 Feature 4: Model Quality Selection

**Location**: Section 2 - Separation Settings

**What it does**: Balance between processing speed and isolation quality

**UI Element**: Radio buttons or slider

**Options**:

- **Fast** (small model)
  - ⚡ Fastest processing
  - 💾 Low memory usage (~2 GB VRAM)
  - ✓ Good quality
  - Best for: Quick tests, CPU-only systems
  
- **Balanced** (base model) - Default
  - ⚖️ Medium processing time
  - 💾 Moderate memory (~4 GB VRAM)
  - ✓✓ Better quality
  - Best for: Most use cases
  
- **High Quality** (large model)
  - 🐌 Slower processing
  - 💾 High memory (~8 GB VRAM)
  - ✓✓✓ Best quality
  - Best for: Final production, maximum accuracy

**Visual Indicator**: Shows estimated processing time and memory requirements

---

### 🆕 Feature 5: Dynamic Stem Tabs

**Location**: Section 6 - Review Stems & Slices

**What it does**: Creates tabs dynamically based on isolated sounds

**Current Behavior** (Traditional Mode):
- Fixed tabs: Vocals, Drums, Bass, Other, Guitar, Piano

**New Behavior** (SAM Audio Mode):
- Dynamic tabs based on prompts
- Examples:
  - If prompts = "saxophone, piano, drums"
  - Tabs show: Saxophone, Piano, Drums

**Tab Features** (per isolated sound):
- Waveform preview
- Audio player
- Generated slices (WAV files)
- Generated MIDI (for melodic content)
- "Slice This [Sound Name]" button

---

### 🆕 Feature 6: Isolation Status Indicator

**Location**: Throughout the interface during processing

**What it does**: Shows progress of SAM Audio isolation

**UI Elements**:
- Progress bar with percentage
- Current prompt being processed
- Estimated time remaining
- Success/failure indicators per prompt

**Example**:
```
Processing SAM Audio Isolation...
━━━━━━━━━━━━━━━━━━━━━━ 75% (3/4)

✓ lead vocals - Complete
✓ electric guitar - Complete  
✓ bass line - Complete
⏳ drum beat - Processing...

Estimated time: 45 seconds
```

---

### 🆕 Feature 7: Prompt Suggestions

**Location**: Section 2 - Separation Settings (below text input)

**What it does**: Suggests related prompts based on what user types

**UI Element**: Auto-complete suggestions or quick-add chips

**Example Flow**:
1. User types: "guitar"
2. Suggestions appear:
   - "electric guitar"
   - "acoustic guitar"
   - "bass guitar"
   - "guitar solo"
   - "rhythm guitar chords"
   - "lead guitar"
3. User clicks to add suggestion

---

### 🆕 Feature 8: Isolation Quality Preview

**Location**: Section 6 - Review Stems & Slices (per tab)

**What it does**: Visual/audio feedback on isolation quality

**UI Elements**:
- Spectrogram comparison (original vs isolated)
- Quality score indicator (Good/Fair/Poor)
- SNR (Signal-to-Noise Ratio) metric
- Audio A/B comparison player

---

### 🆕 Feature 9: Export Options

**Location**: Section 7 - Generate Pack

**Enhanced Options**:
- Include isolated sounds: ☑ (new)
- Include traditional stems: ☑
- Include MIDI files: ☑
- Include sliced loops: ☑
- Include documentation: ☑ (lists which prompts were used)

---

### 🆕 Feature 10: SAM Audio Settings Panel

**Location**: New collapsible section in Settings area

**Advanced Options**:
- Device selection: [Auto / CPU / CUDA]
- Model caching: [Enabled / Disabled]
- Reranking candidates: [1-5]
- Predict spans: [Enabled / Disabled]
- Batch size: [1-10]

---

## User Workflow Examples

### Workflow 1: Standard Music Production

1. Upload song → "Upload Song" button
2. Select "SAM Audio" mode
3. Choose preset: "Standard Band"
4. Click "Separate Stems & Analyze"
5. Wait for processing (progress shown)
6. Review each tab (Vocals, Guitar, Bass, Drums)
7. Adjust global settings (BPM, key, etc.)
8. Click "SLICE ALL & GENERATE PACK"
9. Download ZIP file with all stems and loops

### Workflow 2: Custom Sound Isolation

1. Upload audio file
2. Select "SAM Audio" mode
3. Choose "Custom..." preset
4. Enter prompts: "audience laughter, speaker voice, microphone feedback"
5. Select quality: "High Quality"
6. Click "Separate Stems & Analyze"
7. Review isolated sounds
8. Export specific sounds only

### Workflow 3: Traditional + SAM Audio Hybrid

1. Upload song
2. First pass: Use "Traditional Stems" to get main categories
3. Export vocal stem
4. Upload vocal stem as new file
5. Switch to "SAM Audio" mode
6. Enter: "lead singer, background vocals, vocal ad-libs"
7. Get detailed vocal separation

---

## Feature Comparison Matrix

| Feature | Traditional Stems | SAM Audio |
|---------|------------------|-----------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Moderate |
| **Flexibility** | ❌ Fixed 6 categories | ✅ Unlimited prompts |
| **Specificity** | ❌ General categories | ✅ Very specific sounds |
| **Memory Usage** | 💾 Low (~1-2 GB) | 💾💾 Medium-High (~2-8 GB) |
| **CPU Support** | ✅ Yes, fast | ⚠️ Yes, but slow |
| **GPU Acceleration** | ✅ Yes | ✅ Yes, recommended |
| **Quality** | ✓✓ Good | ✓✓✓ Excellent |
| **Setup Required** | ✅ Built-in | ⚠️ Package install needed |

---

## Keyboard Shortcuts (Planned)

- `Ctrl + U` - Upload audio file
- `Ctrl + S` - Start separation
- `Ctrl + M` - Toggle separation mode
- `Ctrl + P` - Focus prompt input
- `Ctrl + Enter` - Process with current settings
- `Ctrl + E` - Export/Generate pack
- `Tab` - Navigate between stem tabs
- `Space` - Play/pause audio preview

---

## Accessibility Features (Planned)

- Screen reader support for all controls
- Keyboard navigation throughout
- High contrast mode option
- Audio waveform descriptions
- Progress announcements
- Error message clarity

---

## Mobile/Responsive Design (Planned)

- Collapsible sections for small screens
- Touch-friendly controls
- Simplified mode for mobile
- Swipe between stem tabs
- Optimized processing for limited resources

---

## Summary

### ✅ Currently Available (Backend API)
- Named sound isolation via Python API
- Batch processing multiple sounds
- Integration with Loop Architect features
- Traditional stem separation (unchanged)
- All core functionality ready to use programmatically

### ⏭️ Planned for UI (Future Phase)
- Separation mode toggle (Traditional / SAM Audio)
- Text prompt input with validation
- Preset prompt templates
- Model quality selection
- Dynamic stem tabs based on prompts
- Real-time progress indicators
- Isolation quality preview
- Enhanced export options
- Advanced settings panel
- Keyboard shortcuts
- Accessibility features
- Mobile responsive design

### 📚 Documentation Available Now
- `SAM_AUDIO_README.md` - Quick start guide
- `SAM_AUDIO_INTEGRATION.md` - Complete integration guide
- `SAM_AUDIO_QUICKREF.md` - Developer quick reference
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `examples_sam_audio.py` - Usage examples with code
- `test_sam_audio.py` - Test suite

---

**Next Steps**: 
1. Backend is complete and ready ✅
2. UI implementation can begin whenever ready
3. All features outlined above can be implemented incrementally
4. Backend API supports all planned UI features

For immediate use, see the Python API examples in the documentation files.
