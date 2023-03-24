# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 08:33:21
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 10:32:06


from typing import List, Dict

def get_dependencies() -> List[Dict]:
    return [
        {
        "plugin_name": "overlaps",
        "plugin_dependencies": ["conv_model"],
        "plugin_file_path": "analysis/overlaps.py",
        "plugin_source_name": "overlaps",
        "plugin_class_name": "OverlapPlugin"
        },
        {
        "plugin_name": "pauses",
        "plugin_dependencies": ["conv_model"],
        "plugin_file_path": "analysis/pauses.py",
        "plugin_source_name": "pauses",
        "plugin_class_name": "PausePlugin"
        },
        {
        "plugin_name": "gaps",
        "plugin_dependencies": ["conv_model"],
        "plugin_file_path": "analysis/gaps.py",
        "plugin_source_name": "gaps",
        "plugin_class_name": "GapPlugin"
        },
        {
        "plugin_name": "syllable_rate",
        "plugin_dependencies": ["conv_model"],
        "plugin_file_path": "analysis/syllable_rate.py",
        "plugin_source_name": "syllable_rate",
        "plugin_class_name": "SyllableRatePlugin"
        },
    ]