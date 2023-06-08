from dataclasses import dataclass 

@dataclass
class XML:
    META_DATAS  = [{'name': '@Languages', 'content': 'eng'}, 
                   {'name': '@Options', 'content': 'CA'}, 
                   {'name': '@Media', 'content': 'test, audio'}, 
                   {'name': '@Comment', 'content': 'absolute'}, 
                   {'name': '@Transcriber', 'content': 'Gailbot 0.3.0'}, 
                   {'name': '@Location', 'content': 'Hilab'}, 
                   {'name': '@Room', 'content': 'big'}, 
                   {'name': '@Situation', 'content': 'test'}]
    NAME = "name"
    CONTENT = "content"
    META = "meta"
    CONV_META_NAME = "@Conversation"
    LABEL = "label"
    UTT = "Utterance"
    GB_VERSION = 'Gailbot 0.3.0'
    TEST = "test"
    CONV = "Conversation"
    HIL = "HiLab"
    SLOWER = "slower"
    FASTER = "faster"
    VERSION_NUM = "ca-delimiter"
    TALK_BANK_LINK = "http://www.talkbank.org/ns/talkbank"
    EMPTY = "EMPTY"
    
@dataclass
class ATT_NAME:
    START_TIME = "startTime"
    END_TIME = "endTime"
    START = "start"
    END = "end"
    TIME_UNIT = "s"
    PARTS = "Participants"
    CHAT = "CHAT"
    VSN = "Version"
    LANG = "Lang"
    CORP = "Corpus"
    DATE = "Date"
    S_LABEL = "speakerlabel"
    LINK = "xmlns"
    TYPE     = 'type'
    LENGTH = "length"
    SYMBOL_LENTH = 'symbolic-length'

@dataclass
class ATT_VALUE:
    TIMMY   = 'timmy'
    VERSION = '2.16.0'
    LANG    = 'eng'
    YEAR    = '1996-02-29'
    END     = 'end'        
    BEGIN   = "begin"
    SIMPLE  = 'simple'
    TIME_UNIT = "s"

@dataclass
class TAG:
    WORD          = "Word"
    UTT           = "u"
    WORD_SUB      = "w"
    OVERLAP_SUB   = "g"
    OVERLAP       = "overlap"
    PAUSES        = "pauses"
    OVERLAP_PRE   = "overlap precedes"
    OVERLAP_POST  = "overlap follows"
    DELIM         = "ca-delimiter"
    TERM_SUB      = "t"
    TERM_SUB_TYPE = "p"
    MEDIA         = "media"
    HEAD          = "head"
    PARTICIPANT   = "participant"
    

@dataclass
class COMMENTS:
    HILAB    = "HI_LAB"
    COMMENT  = "comment"
    LOCATION = 'Location'

@dataclass
class UTT:
    WHO = 'who'
    ID  = 'uID'
    U   = "u"