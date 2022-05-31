# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-29 15:22:38
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-31 13:27:32

from typing import Dict
from .vardefs import *

PLUGINS_TO_APPLY = [
    "constructTree",
    "utteranceDict",
    "speakerDict",
    "conversationDict",
    "convModelPlugin",
    # "testLayer00"
    "overlaps",
    "pauses",
    "gaps",
    "syllRate",
    "layerPrint01",
    "plainPrint",
    "chat",
    "txt",
    "csvPlugin",
    "csvWordLevel",
    # "xmlPlugin",
    "XMLtoCSV",
    "xmlSchema"
]

def get_settings_dict() -> Dict:
    return {
        "core": {},
        "plugins": {
            "plugins_to_apply": PLUGINS_TO_APPLY
        },
        "engines": {
            "engine_type": "watson",
            "watson_engine": {
                "watson_api_key": WATSON_API_KEY,
                "watson_language_customization_id": WATSON_LANG_CUSTOM_ID,
                "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                "watson_region": WATSON_REGION,

            }
        }
    }
