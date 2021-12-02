# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:32:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:11:22

from typing import Dict
from dataclasses import dataclass
from ..shared_models import Source, Utt


@dataclass
class Payload:
    source: Source
    utterances_map: Dict[str, Utt] = None
