# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 14:39:47
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:37:44

from gailbot.plugins import Methods
from typing import Dict

class GBPluginMethods(Methods):

    def __init__(self):
        pass

    @property
    def audios(self) -> Dict[str,str]:
        raise NotImplementedError()

    @property
    def utterances(self) -> Dict[str,Dict]:
        raise NotImplementedError()

    @property
    def save_dir(self) -> str:
        raise NotImplementedError()

