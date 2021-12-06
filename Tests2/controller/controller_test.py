# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:33:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 22:01:42

import pytest
from Tests2.controller.vardefs import *
from Src2.components.controller import GailBotController
from Src2.components.io import IO


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.clear_directory(RESULT_DIR_PATH)


def test():
    controller = GailBotController(WS_DIR_PATH)

    loaded = controller.add_source(
        "mp3_medium", MXF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()


# def test():
#     controller = GailBotController(WS_DIR_PATH)
#     for i in range(20):
#         loaded = controller.add_source(
#             "mp3_{}".format(i), MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
#     print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
#     controller.transcribe()
