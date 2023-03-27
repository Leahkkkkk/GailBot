from dataclasses import dataclass

@dataclass 
class MARKER:
    GAPS = "gaps"
    OVERLAPS = "overlaps"
    PAUSES = "pauses"
    FTO = "fto"
    LATCH = "latch"
    MICROPAUSE = "micropause"

    # marker text
    MARKER_SEP = ":"
    MARKERTYPE = "markerType"
    KEYVALUE_SEP = "="
    MARKERINFO = "markerInfo"
    MARKERSPEAKER = "markerSpeaker"

    # Speaker label for underlying overlap markers
    MARKER1 = "overlap-firstStart"
    MARKER2 = "overlap-firstEnd"
    MARKER3 = "overlap-secondStart"
    MARKER4 = "overlap-secondEnd"
    SLOWSPEECH_DELIM = u'\u2207'
    FASTSPEECH_DELIM = u'\u2206'
    LATCH_DELIM = u'\u2248'
    SLOWSPEECH_START = "slowspeech_start"
    SLOWSPEECH_END = "slowspeech_end"
    FASTSPEECH_START = "fastspeech_start"
    FASTSPEECH_END = "fastspeech_end"
    INTERNAL_MARKER_SET = {GAPS, OVERLAPS, PAUSES, MARKER1, MARKER2, MARKER3, MARKER4,
                           SLOWSPEECH_START, SLOWSPEECH_END, SLOWSPEECH_START, SLOWSPEECH_END}
    STRANGE_SYMBOL = {".", "%"}

@dataclass 
class THRESHOLD:
    GAPS_LB = 0.3
    OVERLAP_MARKERLIMIT = 4
    LB_LATCH = 0.01
    UB_LATCH = 0.09
    LB_PAUSE = 0.2
    UB_PAUSE = 1.0
    LB_MICROPAUSE = 0.1
    UB_MICROPAUSE = 0.2
    LB_LARGE_PAUSE = 1.0
    # turn_end_threshold_secs from layer00 when constructing utterances
    TURN_END_THRESHOLD_SECS = 0.1

@dataclass 
class LABEL: 
    SPEAKERLABEL = "SP_"
    CSV_SPEAKERLABEL = "SP_"
    XML_SPEAKERLABEL = "SP"
    TXT_SPEAKERLABEL = "SP_"

    CHAT_GAPMARKER = "(gap chat)"
    CHAT_OVERLAPMARKER = "(my_overlap chat)"
    CHAT_PAUSE = "(my_pause chat)"

    CSV_GAPMARKER = "(gap csv)"
    CSV_OVERLAPMARKER = "(my_overlap csv)"
    CSV_PAUSE = "(my_pause csv)"

    TXT_GAPMARKER = "(gap txt)"
    TXT_OVERLAPMARKER = "(my_overlap txt)"
    TXT_PAUSE = "(my_pause txt)"

    XML_GAPMARKER = "(gap xml)"
    XML_OVERLAPMARKER = "(my_overlap xml)"

    OVERLAPMARKER_CURR_START = " < "
    OVERLAPMARKER_CURR_END   = " > [<]"
    OVERLAPMARKER_NEXT_START = " < "
    OVERLAPMARKER_NEXT_END   = " > [>]"

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
class CONVERSATION:
    map1 = "map1"
    map2 = "map2"
    map3 = "map3"