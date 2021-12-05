# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:32:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 14:25:03

from typing import Dict, List
from dataclasses import dataclass, field
from collections import defaultdict
from ..shared_models import Source, Utt, DataFile


@dataclass
class SourceAddons:
    utterances_map: Dict[str, Utt]
    data_file_paths: Dict[str, Dict]


@dataclass
class Payload:
    source: Source
    source_addons: SourceAddons
