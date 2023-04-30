from dataclasses import dataclass 
from .config import load_internal_marker

@dataclass
class MARKER_FORMATTER: 
    TYPE_INFO_SP = "(markerType={0}:markerInfo={1}:markerSpeaker={2}"


@dataclass
class CHAT_FORMATTER: 
    HEADER_LANGUAGE = "@Begin\n@Languages:\t{0}\n"
    TURN = "{0}\t{1} {2}{4}_{3}{4}\n"
    TXT_SEP = " "
