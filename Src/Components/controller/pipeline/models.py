from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict
from ...services import Source
from ...plugin_manager import PluginExecutionSummary


class ProcessStatus(IntEnum):
    READY = 0
    TRANSCRIBED = 1
    PLUGINS_APPLIED = 2
    OUTPUTTED = 3
    FAILED = 4


@dataclass
class Payload:

    @dataclass
    class AddOns:
        source_to_audio_map: Dict = field(default_factory=dict)
        plugin_summaires: Dict[str, PluginExecutionSummary] = field(
            default_factory=dict)

    source: Source
    status: ProcessStatus = ProcessStatus.READY
    addons: AddOns = AddOns()


@dataclass
class Utt:
    speaker_label: str
    start_time_seconds: float
    end_time_seconds: float
    text: str
