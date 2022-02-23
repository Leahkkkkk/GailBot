# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-02-17 15:00:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-02-23 08:12:39

import sys
import os
from typing import Dict, Any
from gailbot.core import GailBotController, GailBotSettings

# ---- GLOBALS # TODO: Separate into another file later.

WORKSPACE_PATH = "./tests/ws"
RESULT_DIR_PATH = "./tests/results"
SETTINGS_PROFILE_EXTENSION = "json"
WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
WATSON_REGION = "dallas"
PROFILE_NAME = "afosr_settings"


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


def init_gb(ws_dir_path: str) -> Any:
    controller = GailBotController(ws_dir_path)
    # Create a profile based on given data
    controller.create_new_settings_profile(
        PROFILE_NAME, get_settings_dict())
    return controller


def run():
    print("Running main...")
    gb = init_gb(WORKSPACE_PATH)


if __name__ == "__main__":
    run()
