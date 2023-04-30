from dataclasses import dataclass 
from .config import load_internal_marker

@dataclass
class MARKER_FORMATTER: 
    TYPE_INFO_SP = "(markerType={0}:markerInfo={1}:markerSpeaker={2}"
