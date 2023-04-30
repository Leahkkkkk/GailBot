import os
from dataclasses import dataclass
import toml
from typing import List 
from dict_to_dataclass import DataclassFromDict, field_from_dict

@dataclass
class INTERNAL_MARKER(DataclassFromDict): 
    GAPS                 : str       = field_from_dict()
    OVERLAPS             : str       = field_from_dict()
    PAUSES               : str       = field_from_dict()
    FTO                  : str       = field_from_dict()
    LATCH                : str       = field_from_dict()
    MICROPAUSE           : str       = field_from_dict()
    MARKERTYPE           : str       = field_from_dict()
    MARKERINFO           : str       = field_from_dict()
    MARKERSPEAKER        : str       = field_from_dict()
    MARKER_SEP           : str       = field_from_dict()
    KEYVALUE_SEP         : str       = field_from_dict()
    NO_SPEAKER           : str       = field_from_dict()
    OVERLAP_FIRST_START  : str       = field_from_dict()
    OVERLAP_FIRST_END    : str       = field_from_dict()
    OVERLAP_SECOND_START : str       = field_from_dict()
    OVERLAP_SECOND_END   : str       = field_from_dict()
    SLOWSPEECH_DELIM     : str       = field_from_dict()
    FASTSPEECH_DELIM     : str       = field_from_dict()
    LATCH_DELIM          : str       = field_from_dict()
    SLOWSPEECH_START     : str       = field_from_dict()
    SLOWSPEECH_END       : str       = field_from_dict()
    FASTSPEECH_START     : str       = field_from_dict()
    FASTSPEECH_END       : str       = field_from_dict()
    DELIM_MARKER1        : str       = field_from_dict()
    DELIM_MARKER2        : str       = field_from_dict()
    UTT_PAUSE_MARKERS    : List[str] = field_from_dict()
    INTERNAL_MARKER_SET = {GAPS, OVERLAPS, PAUSES, OVERLAP_FIRST_START, OVERLAP_FIRST_END, OVERLAP_SECOND_START, OVERLAP_SECOND_END,
        SLOWSPEECH_START, SLOWSPEECH_END, SLOWSPEECH_START, SLOWSPEECH_END}
    # marker text
@dataclass
class THRESHOLD(DataclassFromDict): 
    GAPS_LB                     : float = field_from_dict()
    OVERLAP_MARKERLIMIT         : float = field_from_dict()
    LB_LATCH                    : float = field_from_dict()
    UB_LATCH                    : float = field_from_dict()
    LB_PAUSE                    : float = field_from_dict()
    UB_PAUSE                    : float = field_from_dict()
    LB_MICROPAUSE               : float = field_from_dict()
    UB_MICROPAUSE               : float = field_from_dict()
    LB_LARGE_PAUSE              : float = field_from_dict()
    TURN_END_THRESHOLD_SECS     : float = field_from_dict()

@dataclass 
class LABEL(DataclassFromDict): 
    SPEAKERLABEL            : str = field_from_dict()
    GAPMARKER               : str = field_from_dict()
    OVERLAPMARKER           : str = field_from_dict()
    PAUSE                   : str = field_from_dict()
    OVERLAPMARKER_CURR_START: str = field_from_dict()
    OVERLAPMARKER_CURR_END  : str = field_from_dict()
    OVERLAPMARKER_NEXT_START: str = field_from_dict()
    OVERLAPMARKER_NEXT_END  : str = field_from_dict()

@dataclass
class ALL_LABELS(DataclassFromDict):
    DEFAULT : LABEL = field_from_dict()
    TXT : LABEL = field_from_dict()
    XML : LABEL = field_from_dict()
    CSV : LABEL = field_from_dict()
    CHAT : LABEL = field_from_dict()

@dataclass 
class PLUGIN_NAME: 
    WordTree     = "WordTreePlugin"
    ConvModel    = "ConversationModelPlugin"
    ConvMap      = "ConversationMapPlugin"
    UttMap       = "UtteranceMapPlugin"
    SpeakerMap   = "SpeakerMapPlugin"
    ConvMap      = "ConversationMapPlugin"
    Overlap      = "OverlapPlugin"
    Pause        = "PausePlugin"
    Gap          = "GapPlugin"
    SyllableRate = "SyllableRatePlugin"
    Chat         = "ChatPlugin"
    Text         = "TextPlugin"
    CSV          = "CSVPlugin"
    XML          = "XMLPlugin"

def load_label():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return  ALL_LABELS.from_dict(d["LABEL"])

def load_threshold():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return  THRESHOLD.from_dict(d["THRESHOLD"])

def load_internal_marker():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return  INTERNAL_MARKER.from_dict(d["INTERNAL_MARKER"])
