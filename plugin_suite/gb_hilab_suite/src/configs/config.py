import os
from dataclasses import dataclass
import toml
from typing import List
from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class INTERNAL_MARKER(DataclassFromDict):
    GAPS = "gaps"
    OVERLAPS = "overlaps"
    PAUSES = "pauses"
    FTO = "fto"
    LATCH = "latch"
    MICROPAUSE = "micropause"
    NO_SPEAKER = " "

    # marker text
    MARKERTYPE = "markerType"
    MARKERINFO = "markerInfo"
    MARKERSPEAKER = "markerSpeaker"
    MARKER_SEP = ":"
    KEYVALUE_SEP = "="
    TYPE_INFO_SP = "(markerType={0}:markerInfo={1}:markerSpeaker={2})"
    # invariant:
    # TYPE_INFO_SP ="({MARKERTYPE}{KEYVALUE_SEP}{0}
    #                 {MAKRER_SEP}{MARKERINFO}{KEYVALUE_SEP}{1}
    #                 {MARKER_SEP}MARKERSPEAKER{KEYVALUE_SEP}{2}"

    # Speaker label for underlying overlap markers
    OVERLAP_FIRST_START = "overlap-firstStart"
    OVERLAP_FIRST_END = "overlap-firstEnd"
    OVERLAP_SECOND_START = "overlap-secondStart"
    OVERLAP_SECOND_END = "overlap-secondEnd"

    SLOWSPEECH_DELIM = "\u2207"
    FASTSPEECH_DELIM = "\u2206"
    LATCH_DELIM = "\u2248"
    SLOWSPEECH_START = "slowspeech_start"
    SLOWSPEECH_END = "slowspeech_end"
    FASTSPEECH_START = "fastspeech_start"
    FASTSPEECH_END = "fastspeech_end"
    DELIM_MARKER1 = "."
    DELIM_MARKER2 = "%"

    UTT_PAUSE_MARKERS = ["%HESITATION"]
    INTERNAL_MARKER_SET = {
        GAPS,
        OVERLAPS,
        PAUSES,
        OVERLAP_FIRST_START,
        OVERLAP_FIRST_END,
        OVERLAP_SECOND_START,
        OVERLAP_SECOND_END,
        SLOWSPEECH_START,
        SLOWSPEECH_END,
        FASTSPEECH_END,
        FASTSPEECH_START,
    }
    # marker text


@dataclass
class THRESHOLD(DataclassFromDict):
    GAPS_LB: float = field_from_dict()
    OVERLAP_MARKERLIMIT: float = field_from_dict()
    LB_LATCH: float = field_from_dict()
    UB_LATCH: float = field_from_dict()
    LB_PAUSE: float = field_from_dict()
    UB_PAUSE: float = field_from_dict()
    LB_MICROPAUSE: float = field_from_dict()
    UB_MICROPAUSE: float = field_from_dict()
    LB_LARGE_PAUSE: float = field_from_dict()
    TURN_END_THRESHOLD_SECS: float = field_from_dict()


@dataclass
class LABEL(DataclassFromDict):
    SPEAKERLABEL: str = field_from_dict()
    GAPMARKER: str = field_from_dict()
    OVERLAPMARKER: str = field_from_dict()
    PAUSE: str = field_from_dict()
    OVERLAPMARKER_CURR_START: str = field_from_dict()
    OVERLAPMARKER_CURR_END: str = field_from_dict()
    OVERLAPMARKER_NEXT_START: str = field_from_dict()
    OVERLAPMARKER_NEXT_END: str = field_from_dict()


@dataclass
class ALL_LABELS(DataclassFromDict):
    DEFAULT: LABEL = field_from_dict()
    TXT: LABEL = field_from_dict()
    XML: LABEL = field_from_dict()
    CSV: LABEL = field_from_dict()
    CHAT: LABEL = field_from_dict()


@dataclass
class PLUGIN_NAME:
    WordTree = "WordTreePlugin"
    ConvModel = "ConversationModelPlugin"
    ConvMap = "ConversationMapPlugin"
    UttMap = "UtteranceMapPlugin"
    SpeakerMap = "SpeakerMapPlugin"
    ConvMap = "ConversationMapPlugin"
    Overlap = "OverlapPlugin"
    Pause = "PausePlugin"
    Gap = "GapPlugin"
    SyllableRate = "SyllableRatePlugin"
    Chat = "ChatPlugin"
    Text = "TextPlugin"
    CSV = "CSVPlugin"
    XML = "XMLPlugin"


@dataclass
class OUTPUT_FILE:
    CHAT = "conversation.cha"
    NATIVE_XML = "conversation.gailbot.xml"
    TB_XML = "conversation.talkbank.xml"
    WORD_CSV = "words.csv"
    UTT_CSV = "conversation.csv"
    CON_TXT = "conversation.txt"


def load_label():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return ALL_LABELS.from_dict(d["LABEL"])


def load_threshold():
    d = toml.load(os.path.join(os.path.dirname(__file__), "configData.toml"))
    return THRESHOLD.from_dict(d["THRESHOLD"])
