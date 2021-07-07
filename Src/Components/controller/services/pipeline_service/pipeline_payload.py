# Standard library imports
from typing import Dict
from dataclasses import dataclass, field
# Local imports
from ....organizer import Conversation
from ....plugin_manager import PluginExecutionSummary
from ..fs_service import SourceHook

@dataclass
class SourcePayload:
    source_name : str
    conversation : Conversation
    hook : SourceHook
    # TranscriptionStage
    transcription_successful : bool = False
    source_to_audio_map : Dict[str,str] = field(default_factory=dict)
    # AnalysisStage
    analysis_successful : bool = False
    analysis_plugin_summaries : Dict[str,PluginExecutionSummary] = \
        field(default_factory=dict)
    # FormatStage
    format_successful : bool = False
    format_plugin_summaries : Dict[str,PluginExecutionSummary] =\
         field(default_factory=dict)