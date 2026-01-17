"""
Sample Pack Generator Agents

This module contains all the specialized agents for the sample pack
generation pipeline. Each agent handles a specific aspect of audio/video
processing and pack creation.

Available Agents:
- StemSeparationAgent: Handles audio ingestion and stem separation
- VocalBuilderAgent: Creates instrumental, karaoke, and acapella versions
- LoopGeneratorAgent: Slices loops and generates one-shots
- LyricExtractionAgent: Extracts and syncs lyrics with timestamps
- VideoExportAgent: Creates music visualizations and exports videos
- PackExportAgent: Organizes and exports final sample pack
- UIAgent: Interface for connecting all agents
"""

from backend.engine.agents.base_agent import BaseAgent
from backend.engine.agents.stem_separation_agent import StemSeparationAgent
from backend.engine.agents.vocal_builder_agent import VocalBuilderAgent
from backend.engine.agents.loop_generator_agent import LoopGeneratorAgent
from backend.engine.agents.lyric_extraction_agent import LyricExtractionAgent
from backend.engine.agents.video_export_agent import VideoExportAgent
from backend.engine.agents.pack_export_agent import PackExportAgent
from backend.engine.agents.ui_agent import UIAgent

__all__ = [
    "BaseAgent",
    "StemSeparationAgent",
    "VocalBuilderAgent",
    "LoopGeneratorAgent",
    "LyricExtractionAgent",
    "VideoExportAgent",
    "PackExportAgent",
    "UIAgent",
]
