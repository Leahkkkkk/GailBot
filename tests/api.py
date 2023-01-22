# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 14:26:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:04:41


from gailbot import GailBot


########
WORKSPACE_DIR = "./output/ws"

AUDIO_PATH = "./data/dev_test_data/media/audio/wav/SineWaveMinus16.wav"
########


def test():
    gb = GailBot(WORKSPACE_DIR)