# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-02-17 15:00:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 17:39:16

from typing import Dict
from typing import Dict, Any
from gailbot.core import GailBotController, GailBotSettings
from vardefs import *
# ---- GLOBALS # TODO: Separate into another file later.


PLUGINS_TO_APPLY = [
    "turn_construct",
    "combine_turns",
    "overlaps",
    "pauses",
    "fto",
    "gaps",
    "chat"
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


def init_gb(ws_dir_path: str) -> GailBotController:
    controller = GailBotController(ws_dir_path)
    # Create a profile based on given data
    controller.create_new_settings_profile(
        SETTINGS_PROFILE_NAME, get_settings_dict())
    return controller


########################## TEST DEFINITIONS ##################################

def run():

    gb = init_gb(TRANSCRIPTION_WORKSPACE)
    print(gb.register_plugins(
        "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot-0.3/Plugins/ca_pkg/src"))
    assert gb.add_source("test_audio_transcription_short",
                         MP3_SAMPLE1_FILE, TRANSCRIPTION_RESULT)
    assert gb.apply_settings_profile_to_source(
        "test_audio_transcription_short", SETTINGS_PROFILE_NAME)
    assert gb.is_source_ready_to_transcribe("test_audio_transcription_short")
    gb.transcribe()


if __name__ == "__main__":
    run()
