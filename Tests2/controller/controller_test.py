# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:33:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:01:17

from Tests2.controller.vardefs import *
from Src2.components.controller import GailBotController


def test():
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()
