# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:22:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 09:43:45

import logging
from datetime import date, time
from typing import Dict
from dataclasses import dataclass
from ..organizer.objects import Source, Settings


# @dataclass
# class SourceAddons:
#     @dataclass
#     class Stats:
#         process_date: date = date.today().strftime("%m/%d/%y")
#         process_start_time: time = None
#         process_end_time: time = None
#         elapsed_time_sec: float = None
#         transcription_time_sec: float = None
#         plugin_application_time_sec: float = None
#         output_time_sec: float = None

#     utterances_map: Dict[str, Utt]
#     data_file_paths: Dict[str, Dict]
#     logger: logging.Logger
#     stats: Stats = Stats()


@dataclass
class Payload:
    source: Source
    settings : Settings