"""
Core workflow types and data structures for Loop Architect.

This module defines the shared types used across all workflow modules.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Literal, Tuple
import numpy as np

# Type aliases
AudioData = Tuple[int, np.ndarray]  # (sample_rate, audio_array)
SeparationMode = Literal['traditional', 'sam-audio']
LoopType = Literal['1-bar', '2-bar', '4-bar', 'one-shots']
StepStatus = Literal['pending', 'running', 'complete', 'failed', 'skipped']


@dataclass
class WorkflowConfig:
    """Configuration for workflow execution."""
    
    # Separation settings
    separation_mode: SeparationMode = 'traditional'
    sam_prompts: Optional[List[str]] = None
    
    # Musical settings
    manual_bpm: Optional[float] = None
    transpose_semitones: int = 0
    time_signature: str = '4/4'
    
    # Slicing settings
    loop_type: LoopType = '4-bar'
    one_shot_sensitivity: float = 0.5
    crossfade_ms: int = 10
    
    # FX settings
    normalize_peak: float = -1.0
    apply_modulation: bool = False
    modulation_rate: str = '1/4'
    pan_depth: float = 0.0
    level_depth: float = 0.0
    filter_type: str = 'None'
    filter_freq: float = 5000.0
    filter_depth: float = 0.0
    attack_gain: float = 0.0
    sustain_gain: float = 0.0
    
    # Output settings
    include_instrumental: bool = True
    include_midi: bool = True
    include_lyrics: bool = False  # Stub feature
    include_visualizer: bool = False  # Stub feature
    include_video: bool = False  # Stub feature
    
    # Metadata
    pack_name: str = 'Loop_Architect_Pack'
    artist_name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class LyricData:
    """Timestamped lyric data (stub)."""
    text: str
    timestamps: List[Tuple[float, float, str]]  # (start, end, text)


@dataclass
class VisualizerData:
    """Visualizer configuration data (stub)."""
    waveform_image: Optional[str] = None
    background_video: Optional[str] = None


@dataclass
class PackStructure:
    """Structure of the generated pack."""
    root_dir: str
    wav_dir: str
    midi_dir: str
    stems_dir: str
    metadata_file: str
    readme_file: str


@dataclass
class WorkflowContext:
    """
    Shared context for workflow execution.
    
    This is passed between modules and accumulates results.
    """
    
    # Input
    input_file: str
    temp_dir: str
    config: WorkflowConfig
    
    # Processing results
    stems: Dict[str, AudioData] = field(default_factory=dict)
    instrumental: Optional[AudioData] = None
    
    # Analysis results
    bpm: float = 120.0
    key: str = 'Unknown Key'
    harmonic_recs: str = '---'
    time_signature: str = '4/4'
    
    # Slicing results
    sliced_files: List[str] = field(default_factory=list)
    midi_files: List[str] = field(default_factory=list)
    
    # Advanced features (stubs)
    lyrics: Optional[LyricData] = None
    visualizer: Optional[VisualizerData] = None
    video: Optional[str] = None
    
    # Pack organization
    metadata: Dict[str, Any] = field(default_factory=dict)
    pack_structure: Optional[PackStructure] = None
    
    # Tracking
    generated_files: List[str] = field(default_factory=list)


@dataclass
class ModuleResult:
    """Result from a workflow module."""
    
    success: bool
    message: str
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowResult:
    """Result of complete workflow execution."""
    
    success: bool
    output_zip: Optional[str]
    error: Optional[str]
    steps_completed: List[str]
    steps_failed: List[str]
    execution_time: float
    generated_files: List[str]


@dataclass
class WorkflowStatus:
    """Current status of workflow execution."""
    
    current_step: str
    current_step_index: int
    total_steps: int
    progress_percent: float
    status_message: str
    is_complete: bool
    has_error: bool
    error_message: Optional[str] = None
