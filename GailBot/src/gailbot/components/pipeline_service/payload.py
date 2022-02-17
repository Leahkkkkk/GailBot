# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:32:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-02-17 09:46:51

import logging
from datetime import date, time
from typing import Dict
from dataclasses import dataclass
from ..shared_models import Source, Utt


@dataclass
class SourceAddons:
    @dataclass
    class Stats:
        process_date: date = date.today().strftime("%m/%d/%y")
        process_start_time: time = None
        process_end_time: time = None
        elapsed_time_sec: float = None
        transcription_time_sec: float = None
        plugin_application_time_sec: float = None
        output_time_sec: float = None

    utterances_map: Dict[str, Utt]
    data_file_paths: Dict[str, Dict]
    logger: logging.Logger
    stats: Stats = Stats()


@dataclass
class Payload:
    source: Source
    source_addons: SourceAddons
