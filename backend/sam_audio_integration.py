"""
SAM Audio Integration Module

This module provides integration with Meta's SAM Audio (Segment Anything Model for Audio)
to enable isolation of any named sound from audio files using text prompts.

SAM Audio allows users to isolate literally anything they can name, not just traditional
stems like vocals, drums, bass, etc.
"""

import os
import tempfile
from typing import Tuple, Optional, List, Dict, Any
import numpy as np
import soundfile as sf


class SAMAudioSeparator:
    """
    Wrapper class for SAM Audio separation capabilities.
    
    This class provides a simple interface to isolate specific sounds from audio
    using natural language descriptions.
    """
    
    def __init__(self, model_type: str = "large", device: str = "auto") -> None:
        """
        Initialize the SAM Audio separator.
        
        Args:
            model_type: Model size to use ("large", "base", "small")
            device: Device to use for inference ("auto", "cuda", "cpu")
        """
        self.model_type = model_type
        self.device = self._setup_device(device)
        self.model = None
        self.processor = None
        self._initialized = False
        
    def _setup_device(self, device: str) -> str:
        """Determine the appropriate device for inference."""
        if device == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return device
    
    def _initialize_model(self) -> None:
        """
        Lazy initialization of the SAM Audio model.
        
        This loads the model only when first needed to save memory and startup time.
        """
        if self._initialized:
            return
            
        try:
            # Try using the lightweight inference wrapper first
            try:
                from sam_audio_infer import SamAudio
                print(f"Loading SAM Audio model (type: {self.model_type})...")
                self.model = SamAudio(model_type=self.model_type)
                self._initialized = True
                print("SAM Audio model loaded successfully (using sam-audio-infer)")
                return
            except ImportError:
                print("sam-audio-infer not available, trying official package...")
            
            # Fall back to official Facebook Research package
            try:
                from sam_audio import SAMAudio, SAMAudioProcessor
                import torch
                
                print(f"Loading official SAM Audio model (facebook/sam-audio-{self.model_type})...")
                self.model = SAMAudio.from_pretrained(f"facebook/sam-audio-{self.model_type}")
                self.processor = SAMAudioProcessor.from_pretrained(f"facebook/sam-audio-{self.model_type}")
                
                # Move to appropriate device
                if self.device == "cuda" and torch.cuda.is_available():
                    self.model = self.model.cuda()
                self.model = self.model.eval()
                
                self._initialized = True
                print("SAM Audio model loaded successfully (using official facebook/sam-audio)")
                return
            except ImportError:
                print("Official sam-audio package not available")
            except Exception as e:
                print(f"Error loading official SAM Audio: {e}")
            
            # If both fail, raise an error with instructions
            raise ImportError(
                "SAM Audio is not installed. Please install one of:\n"
                "1. Lightweight version:\n"
                "   pip install sam-audio-infer\n"
                "2. Official version:\n"
                "   git clone https://github.com/facebookresearch/sam-audio\n"
                "   cd sam-audio\n"
                "   pip install .\n"
                "\nNote: Official version requires GPU and Hugging Face authentication."
            )
            
        except Exception as e:
            print(f"Error initializing SAM Audio model: {e}")
            raise
    
    def separate_by_description(
        self,
        audio_path: str,
        description: str,
        output_path: Optional[str] = None
    ) -> Tuple[int, np.ndarray]:
        """
        Separate and isolate a specific sound from audio using a text description.
        
        Args:
            audio_path: Path to the input audio file
            description: Natural language description of what to isolate
                        Examples: "lead vocals", "guitar solo", "dog barking",
                                "piano melody", "crowd cheering", "rain sounds"
            output_path: Optional path to save the isolated audio
            
        Returns:
            Tuple of (sample_rate, audio_data) for the isolated sound
            
        Examples:
            >>> separator = SAMAudioSeparator()
            >>> sr, isolated = separator.separate_by_description("song.wav", "guitar solo")
        """
        # Initialize model on first use
        self._initialize_model()
        
        try:
            # Use lightweight inference wrapper if available
            if hasattr(self.model, 'infer'):
                result = self.model.infer(audio_path=audio_path, text=description)
                
                # Extract the isolated audio from result
                if isinstance(result, dict) and 'target' in result:
                    audio_data = result['target']
                    sample_rate = result.get('sample_rate', 44100)
                else:
                    audio_data = result
                    sample_rate = 44100
                    
            # Use official package if available
            else:
                import torch
                import torchaudio
                
                # Process the audio with the text prompt
                batch = self.processor(
                    audios=[audio_path],
                    descriptions=[description]
                ).to(self.device)
                
                with torch.inference_mode():
                    result = self.model.separate(
                        batch,
                        predict_spans=False,
                        reranking_candidates=1
                    )
                
                # Extract the target (isolated) audio
                audio_data = result.target.cpu().numpy()
                sample_rate = self.processor.audio_sampling_rate
            
            # Convert to proper format
            if audio_data.ndim == 1:
                audio_data = audio_data.reshape(-1, 1)
            elif audio_data.ndim == 3:
                audio_data = audio_data.squeeze(0).T
            elif audio_data.shape[0] < audio_data.shape[1] and audio_data.ndim == 2:
                audio_data = audio_data.T
            
            # Save if output path provided
            if output_path:
                sf.write(output_path, audio_data, sample_rate)
            
            return sample_rate, audio_data
            
        except Exception as e:
            print(f"Error during SAM Audio separation: {e}")
            raise
    
    def separate_multiple(
        self,
        audio_path: str,
        descriptions: List[str],
        output_dir: Optional[str] = None
    ) -> Dict[str, Tuple[int, np.ndarray]]:
        """
        Separate multiple sounds from the same audio file.
        
        Args:
            audio_path: Path to the input audio file
            descriptions: List of natural language descriptions for each sound to isolate
            output_dir: Optional directory to save all isolated sounds
            
        Returns:
            Dictionary mapping description to (sample_rate, audio_data) tuples
            
        Examples:
            >>> separator = SAMAudioSeparator()
            >>> results = separator.separate_multiple(
            ...     "band.wav",
            ...     ["lead vocals", "bass guitar", "drum kit", "keyboard"]
            ... )
        """
        self._initialize_model()
        
        results: Dict[str, Tuple[int, np.ndarray]] = {}
        
        for description in descriptions:
            print(f"Isolating: {description}...")
            
            # Determine output path if directory provided
            output_path = None
            if output_dir:
                safe_desc = description.replace(" ", "_").replace("/", "_")
                output_path = os.path.join(output_dir, f"{safe_desc}.wav")
            
            try:
                sr, audio = self.separate_by_description(
                    audio_path,
                    description,
                    output_path
                )
                results[description] = (sr, audio)
                print(f"Successfully isolated: {description}")
            except Exception as e:
                print(f"Failed to isolate '{description}': {e}")
                continue
        
        return results
    
    def is_available(self) -> bool:
        """
        Check if SAM Audio is available and can be used.
        
        Returns:
            True if SAM Audio can be initialized, False otherwise
        """
        try:
            self._initialize_model()
            return True
        except Exception:
            return False


def create_named_stem_separations(
    audio_file_path: str,
    prompts: List[str],
    model_type: str = "large"
) -> Dict[str, Tuple[int, np.ndarray]]:
    """
    High-level function to separate named sounds from an audio file.
    
    This is the main entry point for SAM Audio integration into the Loop Architect tool.
    
    Args:
        audio_file_path: Path to the audio file to process
        prompts: List of text descriptions for sounds to isolate
        model_type: SAM Audio model size ("large", "base", "small")
        
    Returns:
        Dictionary mapping prompt to (sample_rate, audio_data) tuples
        
    Examples:
        >>> results = create_named_stem_separations(
        ...     "song.mp3",
        ...     ["lead vocals", "electric guitar", "bass line", "drum beat"]
        ... )
        >>> for name, (sr, audio) in results.items():
        ...     print(f"{name}: {audio.shape}")
    """
    separator = SAMAudioSeparator(model_type=model_type)
    return separator.separate_multiple(audio_file_path, prompts)


# Example usage and testing
if __name__ == "__main__":
    print("SAM Audio Integration Module")
    print("=" * 60)
    print("\nThis module provides integration with Meta's SAM Audio model")
    print("for isolating any named sound from audio files.\n")
    
    # Check if SAM Audio is available
    separator = SAMAudioSeparator()
    if separator.is_available():
        print("✓ SAM Audio is available and ready to use!")
        print(f"  Device: {separator.device}")
        print(f"  Model type: {separator.model_type}")
    else:
        print("✗ SAM Audio is not available.")
        print("\nTo install SAM Audio:")
        print("  Option 1 (Lightweight): pip install sam-audio-infer")
        print("  Option 2 (Official): Follow instructions at")
        print("             https://github.com/facebookresearch/sam-audio")
    
    print("\n" + "=" * 60)
    print("Example usage:")
    print("  from sam_audio_integration import create_named_stem_separations")
    print("  results = create_named_stem_separations(")
    print("      'song.mp3',")
    print("      ['vocals', 'guitar', 'drums', 'bass']")
    print("  )")
