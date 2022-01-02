# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 14:14:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-01-01 18:24:14

from dataclasses import dataclass


@dataclass
class Utt:
    """
    Object representing a single conversation unit in different contexts.
    """
    speaker_label: str
    start_time_seconds: float
    end_time_seconds: float
    text: str
