# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-02-17 15:00:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-29 15:55:39

from typing import Dict
from typing import Dict, Any
from gailbot.core import GailBotController, GailBotSettings
from ..vardefs import *
from ..utils import *

# ---- GLOBALS # TODO: Separate into another file later.


def init_gb(ws_dir_path: str) -> GailBotController:
    controller = GailBotController(ws_dir_path)
    # Create a profile based on given data
    controller.create_new_settings_profile(
        SETTINGS_PROFILE_NAME, get_settings_dict())
    return controller


########################## TEST DEFINITIONS ##################################

def run():

    gb = init_gb(TRANSCRIPTION_WORKSPACE)
    assert gb.add_source("test_audio_transcription_short",
                         MP3_SAMPLE1_FILE, TRANSCRIPTION_RESULT)
    assert gb.apply_settings_profile_to_source(
        "test_audio_transcription_short", SETTINGS_PROFILE_NAME)
    assert gb.is_source_ready_to_transcribe("test_audio_transcription_short")
    gb.transcribe()


if __name__ == "__main__":
    run()
