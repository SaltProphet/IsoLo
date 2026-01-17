"""Pack builder module for organizing files into final structure."""

import os
import shutil
from workflow_types import WorkflowContext, ModuleResult, PackStructure


class PackBuilder:
    """Organizes files into final pack structure."""
    
    def get_name(self) -> str:
        """Get module name."""
        return "Pack Builder"
    
    def is_required(self) -> bool:
        """This module is required."""
        return True
    
    def process(self, context: WorkflowContext) -> ModuleResult:
        """
        Create folder structure and organize files.
        
        Args:
            context: Workflow context
            
        Returns:
            ModuleResult with pack structure
        """
        try:
            # Create pack directory structure
            pack_root = os.path.join(context.temp_dir, context.config.pack_name)
            os.makedirs(pack_root, exist_ok=True)
            
            wav_dir = os.path.join(pack_root, "WAV")
            midi_dir = os.path.join(pack_root, "MIDI")
            stems_dir = os.path.join(pack_root, "Stems")
            
            os.makedirs(wav_dir, exist_ok=True)
            os.makedirs(midi_dir, exist_ok=True)
            os.makedirs(stems_dir, exist_ok=True)
            
            # Move sliced files to WAV folder
            for file_path in context.sliced_files:
                if os.path.exists(file_path):
                    dest = os.path.join(wav_dir, os.path.basename(file_path))
                    shutil.move(file_path, dest)
            
            # Move MIDI files to MIDI folder
            for file_path in context.midi_files:
                if os.path.exists(file_path):
                    dest = os.path.join(midi_dir, os.path.basename(file_path))
                    shutil.move(file_path, dest)
            
            # Copy stems to Stems folder
            for stem_name in context.stems.keys():
                # Look for stem files in temp directory
                for file in os.listdir(context.temp_dir):
                    if stem_name.lower() in file.lower() and file.endswith('.wav'):
                        src = os.path.join(context.temp_dir, file)
                        dest = os.path.join(stems_dir, file)
                        if os.path.exists(src):
                            shutil.copy2(src, dest)
            
            # Copy instrumental if present
            if context.instrumental and context.config.include_instrumental:
                instrumental_path = os.path.join(
                    context.temp_dir,
                    f"{context.config.pack_name}_Instrumental.wav"
                )
                if os.path.exists(instrumental_path):
                    dest = os.path.join(stems_dir, os.path.basename(instrumental_path))
                    shutil.copy2(instrumental_path, dest)
            
            # Create metadata README
            readme_path = os.path.join(pack_root, "README.md")
            self._create_readme(readme_path, context)
            
            # Create metadata JSON
            metadata_path = os.path.join(pack_root, "metadata.txt")
            self._create_metadata_file(metadata_path, context)
            
            # Update context with pack structure
            context.pack_structure = PackStructure(
                root_dir=pack_root,
                wav_dir=wav_dir,
                midi_dir=midi_dir,
                stems_dir=stems_dir,
                metadata_file=metadata_path,
                readme_file=readme_path
            )
            
            # Count files
            total_files = len(os.listdir(wav_dir)) + len(os.listdir(midi_dir)) + len(os.listdir(stems_dir))
            
            return ModuleResult(
                success=True,
                message=f"Pack structure created: {total_files} files organized"
            )
            
        except Exception as e:
            return ModuleResult(
                success=False,
                message="",
                error=f"Pack building failed: {str(e)}"
            )
    
    def _create_readme(self, readme_path: str, context: WorkflowContext) -> None:
        """Create README file for the pack."""
        content = f"""# {context.config.pack_name}

## Pack Information

- **BPM**: {int(context.bpm)}
- **Key**: {context.key}
- **Time Signature**: {context.time_signature}
- **Harmonic Recommendations**: {context.harmonic_recs}

## Contents

### WAV Folder
Contains sliced audio loops and one-shots.

### MIDI Folder
Contains MIDI files generated from melodic stems.

### Stems Folder
Contains individual stem tracks (vocals, drums, bass, etc.).

## Usage

These files are ready to import into your DAW (Digital Audio Workstation).

1. Drag and drop WAV files directly into your project
2. Import MIDI files and assign to instruments
3. Use stems for further processing or remixing

## Metadata

All audio files are tagged with BPM and key information for easy organization.

---

Generated by Loop Architect
"""
        
        if context.config.artist_name:
            content += f"\nArtist: {context.config.artist_name}\n"
        
        if context.config.description:
            content += f"\nDescription: {context.config.description}\n"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_metadata_file(self, metadata_path: str, context: WorkflowContext) -> None:
        """Create simple metadata text file."""
        content = f"""Loop Architect Pack Metadata
=============================

Pack Name: {context.config.pack_name}
BPM: {int(context.bpm)}
Key: {context.key}
Time Signature: {context.time_signature}
Harmonic Recommendations: {context.harmonic_recs}

Configuration:
- Separation Mode: {context.config.separation_mode}
- Loop Type: {context.config.loop_type}
- Transpose: {context.config.transpose_semitones} semitones
- Normalization: {context.config.normalize_peak} dBFS

Generated Files:
- WAV Files: {len(context.sliced_files)}
- MIDI Files: {len(context.midi_files)}
- Stems: {len(context.stems)}
"""
        
        if context.config.artist_name:
            content += f"\nArtist: {context.config.artist_name}"
        
        if context.config.description:
            content += f"\nDescription: {context.config.description}"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(content)
