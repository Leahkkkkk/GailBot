# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:13:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:59:48

from dataclasses import dataclass
from typing import List, Dict

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

###########################################################
# underlying speaker label
###########################################################

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

SLOWSPEECH_CHAT = u'\u2207'
FASTSPEECH_CHAT = u'\u2206'

SLOWSPEECH_START = "slowspeech_start"
SLOWSPEECH_END = "slowspeech_end"
FASTSPEECH_START = "fastspeech_start"
FASTSPEECH_END = "fastspeech_end"

INTERNAL_MARKER_SET = set()
INTERNAL_MARKER_SET.add(GAPS)
INTERNAL_MARKER_SET.add(OVERLAPS)
INTERNAL_MARKER_SET.add(PAUSES)
INTERNAL_MARKER_SET.add(MARKER1)
INTERNAL_MARKER_SET.add(MARKER2)
INTERNAL_MARKER_SET.add(MARKER3)
INTERNAL_MARKER_SET.add(MARKER4)
INTERNAL_MARKER_SET.add(SLOWSPEECH_START)
INTERNAL_MARKER_SET.add(SLOWSPEECH_END)
INTERNAL_MARKER_SET.add(FASTSPEECH_START)
INTERNAL_MARKER_SET.add(FASTSPEECH_END)

STRANGE_SYMBOL = set()
STRANGE_SYMBOL.add('.')
STRANGE_SYMBOL.add('%')

###########################################################
# surface marker text
###########################################################
#speaker label
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
