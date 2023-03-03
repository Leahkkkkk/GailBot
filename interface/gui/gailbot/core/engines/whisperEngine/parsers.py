# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 16:53:33
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 17:57:45

import sys
import os
import json
from typing import Dict, List, Any, Tuple
# from pyannote.core import Segment

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

# def parse_into_timestamped_text(asr_res : Dict) -> List[Tuple]:
#     """
#     Parse results from whisper timestamped in terms of Segment
#     """
#     timestamp_texts = []
#     for segment in asr_res['segments']:
#         word_list = segment["words"]
#         for item in word_list:
#             start = item['start']
#             end = item['end']
#             text = item['text']
#             timestamp_texts.append((Segment(start, end), text))
#     return timestamp_texts

# def parse_into_full_text(asr_res : Dict) -> str:
#     """
#     Parse the transcription output into a string.
#     """
#     return asr_res["text"]

# def add_speaker_info_to_text(asr_res : Dict, dir_res : Dict) -> Dict:
#     """
#     Add speaker information to transcription results using speaker
#     diarization results. Returns dictionaries
#     """
#     spk_text = []
#     timestamp_texts = parse_into_timestamped_text(asr_res)
#     for seg, text in timestamp_texts:
#         spk = dir_res.crop(seg).argmax()
#         spk_text.append({
#             "start" : seg.start,
#             "end" : seg.end,
#             "speaker" : spk,
#             "text" : text
#         })
#     return spk_text
