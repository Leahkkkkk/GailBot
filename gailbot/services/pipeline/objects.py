# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:22:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 15:16:18

import logging
from datetime import date, time
from typing import Dict, List, Any, Dict
from dataclasses import dataclass
from ..organizer.objects import Source, Settings

@dataclass
class Utterance:
    speaker : str
    text : str
    start_time : float
    end_time : float

@dataclass
class ProcessingStats:
    date: date = date.today().strftime("%m/%d/%y")
    start_time: time = None
    end_time: time = None
    elapsed_time_sec: float = None


@dataclass
class TranscriptionResults:
    utterances = Dict[str, List[Utterance]] = dict()
    stats = ProcessingStats()

@dataclass
class AnalysisResults:
    stats = ProcessingStats()

@dataclass
class FormatResults:
    stats = ProcessingStats()


@dataclass
class Payload:
    source: Source
    transcription_res : TranscriptionResults = TranscriptionResults()
    analysis_res: AnalysisResults = AnalysisResults()
    format_res : FormatResults = FormatResults()


class PayloadOutputWriter:

    @staticmethod
    def write_output(self, payload : Payload) -> bool:
        pass

    @staticmethod
    def is_payload_output(self, dir_path : str) -> bool:
        pass

    @staticmethod
    def read_payload_output(self, dir_path) -> Source:
        pass