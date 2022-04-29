# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-29 15:22:38
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-29 15:22:51

from typing import Dict
from .vardefs import *


def get_settings_dict() -> Dict:
    return {
        "core": {},
        "plugins": {
            "plugins_to_apply": []
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


