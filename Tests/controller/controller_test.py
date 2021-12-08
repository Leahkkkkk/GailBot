# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:33:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 18:18:03

import pytest
from typing import Dict
from Tests.controller.vardefs import *
from Src.components import GailBotController, GailBotSettings
from Src.components.io import IO


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.clear_directory(RESULT_DIR_PATH)


def settings_data() -> Dict:
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


# def test():

#     controller = GailBotController(WS_DIR_PATH)
#     data = settings_data()
#     controller.add_source(
#         "mp3", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
#     assert controller.create_new_settings_profile("test", data)
#     save_path = controller.save_settings_profile("test")
#     controller.apply_settings_profile_to_source("mp3", "test")
#     print(controller.get_source_names())
#     controller.remove_settings_profile("test")
#     print(controller.get_source_names())
#     # Part 2
#     controller.add_source(
#         "mp3", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
#     assert controller.create_new_settings_profile("test", data)
#     controller.apply_settings_profile_to_source("mp3", "test")
#     print(controller.get_source_names_using_settings_profile("test"))
#     controller.change_settings_profile_name("test", "test2")
#     print(controller.get_source_names_using_settings_profile("test"))
#     print(controller.get_source_names_using_settings_profile("test2"))
#     # Part 3
#     print("Part 3")
#     assert controller.save_source_settings_profile("mp3", "source_profile")
#     print(controller.get_settings_profile_names())
#     print(controller.get_source_names_using_settings_profile("test2"))
#     print(controller.get_source_names_using_settings_profile("source_profile"))
#     controller.change_settings_profile_name("source_profile", "apple")
#     print(controller.get_source_names_using_settings_profile("source_profile"))
#     print(controller.get_source_names_using_settings_profile("apple"))


# def test():
#     controller = GailBotController(WS_DIR_PATH)
#     data = settings_data()
#     assert controller.create_new_settings_profile("test", data)
#     save_path = controller.save_settings_profile("test")
#     print(save_path)
#     assert controller.remove_settings_profile("test")
#     print(controller.load_settings_profile(save_path))
#     settings: GailBotSettings = controller.get_settings_profile("test")
#     controller.save_settings_profile("test")
#     controller.add_source(
#         "mp3", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
#     controller.apply_settings_profile_to_source("mp3", "test")
#     controller.transcribe()


def test():
    controller = GailBotController(WS_DIR_PATH)
    controller.create_new_settings_profile(
        "settings", settings_data())
    controller.add_source(
        "mp3_medium",MXF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("mp3_medium", "settings")
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()


# def test():
#     controller = GailBotController(WS_DIR_PATH)
#     for i in range(20):
#         loaded = controller.add_source(
#             "mp3_{}".format(i), MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
#     print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
#     controller.transcribe()
