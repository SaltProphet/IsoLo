"""
Instrumental & Vocal Builder Agent

Combines separated stems to create instrumental, karaoke, and acapella versions
of the audio. Handles audio normalization, mixing, and metadata tagging.

This agent takes the output from the Stem Separation Agent and creates various
mix-downs suitable for different use cases.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import numpy as np

from backend.engine.agents.base_agent import BaseAgent


class VocalBuilderAgent(BaseAgent):
    """
    Agent for building instrumental, karaoke, and acapella versions.
    
    This agent combines separated stems in different ways to create:
    1. Instrumental (all stems except vocals)
    2. Karaoke (reduced vocals, all other stems)
    3. Acapella (vocals only, optionally with reverb/effects)
    
    All outputs are normalized and tagged with appropriate metadata.
    
    Attributes:
        config: Configuration for mixing and normalization settings
    
    Example:
        >>> agent = VocalBuilderAgent(config={"normalize_db": -3.0})
        >>> result = agent.process({
        ...     "stems": {"vocals": "vocals.wav", "drums": "drums.wav", ...},
        ...     "manifest_path": "manifest.json",
        ...     "output_dir": "/path/to/output"
        ... })
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Vocal Builder Agent.
        
        Args:
            config: Optional configuration dictionary with keys:
                - normalize_db: Target normalization level in dB (default: -3.0)
                - karaoke_vocal_level: Vocal level for karaoke (default: 0.3)
                - apply_effects: Whether to apply effects to acapella (default: False)
        """
        super().__init__(config)
        self.normalize_db = self.get_config_value("normalize_db", -3.0)
        self.karaoke_vocal_level = self.get_config_value("karaoke_vocal_level", 0.3)
        self.apply_effects = self.get_config_value("apply_effects", False)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process stems to create instrumental, karaoke, and acapella versions.
        
        Args:
            input_data: Dictionary containing:
                - stems: Dictionary mapping stem names to file paths
                - manifest_path: Path to manifest JSON (for metadata)
                - output_dir: Directory for output files
                
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - message: Result message
                - data: Dictionary with:
                    - instrumental: Path to instrumental version
                    - karaoke: Path to karaoke version
                    - acapella: Path to acapella version
        """
        # Validate input
        if not self.validate_input(input_data, ["stems", "output_dir"]):
            return self.create_error_response("Invalid input data")
        
        stems = input_data["stems"]
        output_dir = input_data["output_dir"]
        manifest_path = input_data.get("manifest_path")
        
        try:
            self.log_info("Building vocal and instrumental mixes...")
            
            # Ensure output directory exists
            self.ensure_output_dir(output_dir)
            
            # Build different versions
            self.log_info("Creating instrumental version...")
            instrumental_path = self.build_instrumental(stems, output_dir)
            
            self.log_info("Creating karaoke version...")
            karaoke_path = self.build_karaoke(stems, output_dir)
            
            self.log_info("Creating acapella version...")
            acapella_path = self.build_acapella(stems, output_dir)
            
            # Apply metadata if manifest provided
            if manifest_path:
                self.log_info("Applying metadata tags...")
                self.apply_metadata_to_all(
                    [instrumental_path, karaoke_path, acapella_path],
                    manifest_path
                )
            
            return self.create_success_response(
                data={
                    "instrumental": instrumental_path,
                    "karaoke": karaoke_path,
                    "acapella": acapella_path
                },
                message="Vocal and instrumental builds completed successfully"
            )
            
        except Exception as e:
            self.log_error(f"Error building mixes: {str(e)}")
            return self.create_error_response(str(e))
    
    def build_instrumental(
        self,
        stems: Dict[str, str],
        output_dir: str
    ) -> str:
        """
        Build instrumental version (all stems except vocals).
        
        Args:
            stems: Dictionary mapping stem names to file paths
            output_dir: Directory to save output
            
        Returns:
            Path to instrumental.wav file
            
        TODO: Implement instrumental mixing
            - Load all non-vocal stems
            - Mix stems together with proper balance
            - Normalize to target level
            - Save as WAV file
            - Include metadata-based filename
        """
        self.log_info("TODO: Implement instrumental mixing")
        
        output_path = Path(output_dir) / "instrumental.wav"
        return str(output_path)
    
    def build_karaoke(
        self,
        stems: Dict[str, str],
        output_dir: str
    ) -> str:
        """
        Build karaoke version (reduced vocals with backing track).
        
        Args:
            stems: Dictionary mapping stem names to file paths
            output_dir: Directory to save output
            
        Returns:
            Path to karaoke.wav file
            
        TODO: Implement karaoke mixing
            - Load all stems including vocals
            - Reduce vocal level (typically -12dB to -18dB)
            - Mix all stems together
            - Normalize to target level
            - Save as WAV file
        """
        self.log_info("TODO: Implement karaoke mixing")
        
        output_path = Path(output_dir) / "karaoke.wav"
        return str(output_path)
    
    def build_acapella(
        self,
        stems: Dict[str, str],
        output_dir: str
    ) -> str:
        """
        Build acapella version (vocals only, optionally with effects).
        
        Args:
            stems: Dictionary mapping stem names to file paths
            output_dir: Directory to save output
            
        Returns:
            Path to acapella.wav file
            
        TODO: Implement acapella processing
            - Load vocals stem
            - Optionally apply reverb/effects for richness
            - Normalize to target level
            - Save as WAV file
        """
        self.log_info("TODO: Implement acapella processing")
        
        output_path = Path(output_dir) / "acapella.wav"
        return str(output_path)
    
    def normalize_audio(
        self,
        audio: np.ndarray,
        target_db: float
    ) -> np.ndarray:
        """
        Normalize audio to target dB level.
        
        Args:
            audio: Audio array (samples x channels)
            target_db: Target peak level in dB
            
        Returns:
            Normalized audio array
            
        TODO: Implement audio normalization
            - Calculate current peak level
            - Compute gain needed to reach target
            - Apply gain with clipping prevention
            - Return normalized audio
        """
        self.log_info("TODO: Implement audio normalization")
        return audio
    
    def mix_stems(
        self,
        stem_paths: List[str],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Mix multiple stems together with optional weights.
        
        Args:
            stem_paths: List of paths to stem files
            weights: Optional list of mixing weights (default: equal weight)
            
        Returns:
            Mixed audio as numpy array
            
        TODO: Implement stem mixing
            - Load all stem files
            - Ensure same length (pad if needed)
            - Apply weights to each stem
            - Sum stems together
            - Check for clipping
        """
        self.log_info("TODO: Implement stem mixing")
        return np.array([])
    
    def apply_metadata(
        self,
        audio_path: str,
        metadata: Dict[str, str]
    ) -> None:
        """
        Apply ID3/metadata tags to audio file.
        
        Args:
            audio_path: Path to audio file
            metadata: Dictionary of metadata tags:
                - title: Track title
                - artist: Artist name
                - album: Album name
                - bpm: Tempo in BPM
                - key: Musical key
                
        TODO: Implement metadata tagging
            - Use mutagen or similar library
            - Apply ID3v2 tags for MP3
            - Apply RIFF tags for WAV
            - Include custom tags for BPM/key
        """
        self.log_info("TODO: Implement metadata tagging")
    
    def apply_metadata_to_all(
        self,
        audio_paths: List[str],
        manifest_path: str
    ) -> None:
        """
        Apply metadata from manifest to all audio files.
        
        Args:
            audio_paths: List of audio file paths
            manifest_path: Path to manifest JSON file
            
        TODO: Implement batch metadata application
            - Load manifest JSON
            - Extract relevant metadata
            - Apply to each audio file
            - Customize title based on version type
        """
        self.log_info("TODO: Implement batch metadata application")
    
    def generate_filename(
        self,
        metadata: Dict[str, Any],
        version_type: str
    ) -> str:
        """
        Generate metadata-based filename.
        
        Args:
            metadata: Metadata dictionary from manifest
            version_type: Type of version ("instrumental", "karaoke", "acapella")
            
        Returns:
            Generated filename (e.g., "Artist - Title (120 BPM, C Major) - Instrumental.wav")
            
        TODO: Implement filename generation
            - Extract artist and title from metadata
            - Include BPM and key information
            - Add version type suffix
            - Sanitize for filesystem compatibility
        """
        self.log_info("TODO: Implement filename generation")
        return f"{version_type}.wav"
