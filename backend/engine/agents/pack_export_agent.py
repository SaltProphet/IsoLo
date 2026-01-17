"""
Metadata & Pack Export Agent

Collects metadata from user and other agents, organizes all generated files into
a consistent folder structure, creates metadata sheets, and exports the final
sample pack as a ZIP file.

This agent handles the final packaging and organization of the sample pack.
"""

from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import json

from backend.engine.agents.base_agent import BaseAgent


class PackExportAgent(BaseAgent):
    """
    Agent for organizing and exporting the final sample pack.
    
    This agent:
    1. Collects metadata from all sources (user input, manifest, analysis)
    2. Organizes files into a consistent folder structure
    3. Tags and renames files with descriptive names
    4. Generates metadata sheets (JSON, CSV, TXT)
    5. Creates a README for the pack
    6. Exports everything as a ZIP file
    
    Attributes:
        config: Configuration for pack structure and export settings
    
    Example:
        >>> agent = PackExportAgent(config={"include_readme": True})
        >>> result = agent.process({
        ...     "pack_name": "My Sample Pack",
        ...     "files": {"loops": [...], "oneshots": [...], ...},
        ...     "metadata": {"artist": "Artist Name", "bpm": 120},
        ...     "output_dir": "/path/to/output"
        ... })
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Pack Export Agent.
        
        Args:
            config: Optional configuration dictionary with keys:
                - structure_template: Folder structure template name
                - include_readme: Whether to generate README (default: True)
                - metadata_formats: List of formats for metadata (default: ["json", "csv"])
                - compression_level: ZIP compression level 0-9 (default: 9)
        """
        super().__init__(config)
        self.structure_template = self.get_config_value("structure_template", "standard")
        self.include_readme = self.get_config_value("include_readme", True)
        self.metadata_formats = self.get_config_value("metadata_formats", ["json", "csv"])
        self.compression_level = self.get_config_value("compression_level", 9)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process all files and metadata to create final sample pack.
        
        Args:
            input_data: Dictionary containing:
                - pack_name: Name of the sample pack
                - files: Dictionary of file lists by category:
                    - stems: List of stem file paths
                    - loops: List of loop file paths
                    - oneshots: List of one-shot file paths
                    - midi: List of MIDI file paths
                    - videos: List of video file paths
                    - lyrics: List of lyric file paths
                - metadata: User-provided and generated metadata
                - output_dir: Directory for final pack
                
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - message: Result message
                - data: Dictionary with:
                    - pack_dir: Path to organized pack folder
                    - zip_path: Path to zipped pack file
                    - metadata_sheet: Path to metadata sheet
        """
        # Validate input
        if not self.validate_input(input_data, ["pack_name", "files", "output_dir"]):
            return self.create_error_response("Invalid input data")
        
        pack_name = input_data["pack_name"]
        files = input_data["files"]
        metadata = input_data.get("metadata", {})
        output_dir = input_data["output_dir"]
        
        try:
            self.log_info(f"Creating sample pack: {pack_name}")
            
            # Create pack directory structure
            self.log_info("Creating folder structure...")
            pack_dir = self.create_pack_structure(pack_name, output_dir)
            
            # Organize and copy files
            self.log_info("Organizing files...")
            self.organize_files(files, pack_dir)
            
            # Rename files with metadata
            self.log_info("Renaming files with descriptive names...")
            self.rename_files_with_metadata(pack_dir, metadata)
            
            # Generate metadata sheets
            self.log_info("Generating metadata sheets...")
            metadata_sheet = self.generate_metadata_sheet(metadata, pack_dir)
            
            # Generate README
            if self.include_readme:
                self.log_info("Generating README...")
                self.generate_readme(pack_name, metadata, pack_dir)
            
            # Create ZIP file
            self.log_info("Creating ZIP archive...")
            zip_path = self.create_pack(pack_dir, output_dir)
            
            return self.create_success_response(
                data={
                    "pack_dir": str(pack_dir),
                    "zip_path": zip_path,
                    "metadata_sheet": metadata_sheet
                },
                message=f"Sample pack '{pack_name}' created successfully"
            )
            
        except Exception as e:
            self.log_error(f"Error creating pack: {str(e)}")
            return self.create_error_response(str(e))
    
    def collect_metadata(
        self,
        sources: List[str]
    ) -> Dict[str, Any]:
        """
        Collect metadata from multiple sources.
        
        Args:
            sources: List of file paths (manifests, user input files, etc.)
            
        Returns:
            Consolidated metadata dictionary
            
        TODO: Implement metadata collection
            - Load each source file
            - Merge metadata dictionaries
            - Resolve conflicts (user input takes precedence)
            - Validate required fields
            - Return consolidated metadata
        """
        self.log_info("TODO: Implement metadata collection")
        
        return {
            "pack_name": "Sample Pack",
            "artist": "Artist Name",
            "bpm": 120,
            "key": "C Major",
            "genre": "Electronic",
            "created_at": self.get_timestamp()
        }
    
    def create_pack_structure(
        self,
        pack_name: str,
        base_dir: str
    ) -> Path:
        """
        Create the folder structure for the sample pack.
        
        Standard structure:
        pack_name/
        ├── Stems/
        ├── Loops/
        │   ├── Drums/
        │   ├── Bass/
        │   └── Melodic/
        ├── One-Shots/
        │   ├── Kicks/
        │   ├── Snares/
        │   └── Hats/
        ├── MIDI/
        ├── Videos/
        ├── Lyrics/
        └── Metadata/
        
        Args:
            pack_name: Name of the pack (used as root folder)
            base_dir: Base directory for the pack
            
        Returns:
            Path to created pack directory
            
        TODO: Implement structure creation
            - Create root folder
            - Create all subdirectories
            - Handle custom structure templates
            - Return pack root path
        """
        self.log_info("TODO: Implement pack structure creation")
        
        pack_dir = Path(base_dir) / pack_name
        pack_dir.mkdir(parents=True, exist_ok=True)
        return pack_dir
    
    def organize_files(
        self,
        files: Dict[str, List[str]],
        pack_dir: Path
    ) -> Dict[str, List[str]]:
        """
        Organize and copy files into pack structure.
        
        Args:
            files: Dictionary mapping categories to file lists
            pack_dir: Pack root directory
            
        Returns:
            Dictionary mapping categories to new file paths
            
        TODO: Implement file organization
            - For each category:
                - Create appropriate subdirectory
                - Copy files to subdirectory
                - Organize by type (e.g., drum one-shots by hit type)
            - Return mapping of new file paths
        """
        self.log_info("TODO: Implement file organization")
        
        return {}
    
    def rename_files_with_metadata(
        self,
        pack_dir: Path,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Rename files with descriptive, metadata-based names.
        
        Example naming patterns:
        - Stems: "Artist - Title - Vocals.wav"
        - Loops: "120 BPM - C Major - Drum Loop 01.wav"
        - One-shots: "Kick - Heavy - 01.wav"
        
        Args:
            pack_dir: Pack root directory
            metadata: Metadata dictionary
            
        TODO: Implement file renaming
            - Walk through all files
            - Generate descriptive name based on:
                - File type/category
                - Musical metadata (BPM, key)
                - Artist/title
            - Sanitize filenames
            - Rename files
        """
        self.log_info("TODO: Implement metadata-based file renaming")
    
    def generate_metadata_sheet(
        self,
        metadata: Dict[str, Any],
        output_dir: Path
    ) -> str:
        """
        Generate metadata sheet in multiple formats.
        
        Args:
            metadata: Metadata dictionary
            output_dir: Directory to save metadata sheets
            
        Returns:
            Path to primary metadata file (JSON)
            
        TODO: Implement metadata sheet generation
            - Create JSON format with full metadata
            - Create CSV format for spreadsheet import
            - Create TXT format for human readability
            - Save all formats in Metadata/ folder
            - Return path to JSON file
        """
        self.log_info("TODO: Implement metadata sheet generation")
        
        metadata_path = output_dir / "Metadata" / "metadata.json"
        return str(metadata_path)
    
    def generate_readme(
        self,
        pack_name: str,
        metadata: Dict[str, Any],
        pack_dir: Path
    ) -> str:
        """
        Generate README file for the sample pack.
        
        README should include:
        - Pack name and description
        - Artist/producer information
        - Musical information (BPM, key, genre)
        - Contents list
        - Usage guidelines
        - Credits and licensing
        
        Args:
            pack_name: Name of the pack
            metadata: Metadata dictionary
            pack_dir: Pack root directory
            
        Returns:
            Path to README.md file
            
        TODO: Implement README generation
            - Create markdown formatted content
            - Include all relevant information
            - List pack contents with counts
            - Add usage examples
            - Save as README.md
        """
        self.log_info("TODO: Implement README generation")
        
        readme_path = pack_dir / "README.md"
        return str(readme_path)
    
    def create_pack(
        self,
        pack_dir: Path,
        output_dir: str
    ) -> str:
        """
        Create a ZIP file of the complete sample pack.
        
        Args:
            pack_dir: Path to organized pack directory
            output_dir: Directory to save ZIP file
            
        Returns:
            Path to created ZIP file
            
        TODO: Implement ZIP creation
            - Create ZIP archive
            - Add all files from pack_dir
            - Use compression level from config
            - Preserve folder structure
            - Name: "pack_name.zip"
            - Return ZIP path
        """
        self.log_info("TODO: Implement pack ZIP creation")
        
        zip_path = Path(output_dir) / f"{pack_dir.name}.zip"
        return str(zip_path)
    
    def validate_pack(
        self,
        pack_dir: Path
    ) -> Tuple[bool, List[str]]:
        """
        Validate that the pack is complete and properly structured.
        
        Args:
            pack_dir: Pack root directory
            
        Returns:
            Tuple of (is_valid, list_of_issues)
            
        TODO: Implement pack validation
            - Check folder structure exists
            - Verify files are in correct locations
            - Check metadata completeness
            - Validate file formats
            - Check for empty folders
            - Return validation result
        """
        self.log_info("TODO: Implement pack validation")
        
        return (True, [])
    
    def calculate_pack_stats(
        self,
        pack_dir: Path
    ) -> Dict[str, Any]:
        """
        Calculate statistics about the pack.
        
        Args:
            pack_dir: Pack root directory
            
        Returns:
            Dictionary with statistics:
                - total_files: Total number of files
                - total_size: Total size in bytes
                - file_counts: Dictionary of counts by type
                - total_duration: Total audio duration in seconds
                
        TODO: Implement pack statistics
            - Walk through all files
            - Count files by type
            - Calculate total size
            - Sum audio durations
            - Return statistics dictionary
        """
        self.log_info("TODO: Implement pack statistics")
        
        return {
            "total_files": 0,
            "total_size": 0,
            "file_counts": {},
            "total_duration": 0.0
        }
