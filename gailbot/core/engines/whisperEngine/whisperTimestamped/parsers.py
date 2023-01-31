# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 16:53:33
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 17:02:01

import sys
import os
import json
from typing import Dict, List, Any


_DEFAULT_SPEAKER = 0


def parse_into_word_dicts(transcription : Dict) -> List[Dict]:
    """
    Parse the results of the transcription into a list of dictionaries
    containing the speaker, start time, end time, and text.

    Format of the transcription is detailed here: https://github.com/linto-ai/whisper-timestamped
    """
    parsed = list()
    segments = transcription["segments"]
    for segment in segments:
        word_list = segment["words"]
        for item in word_list:
            parsed.append({
                "start" : item["start"],
                "end" : item["end"],
                "text" : item["text"],
                # NOTE: Whisper does not generate speaker but I can
                # potentially add that in too.
                "speaker" : str(_DEFAULT_SPEAKER)
            })
    return parsed


def parse_into_full_text(transcription : Dict) -> str:
    """
    Parse the transcription output into a string.
    """
    return transcription["text"]
