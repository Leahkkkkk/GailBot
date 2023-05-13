# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-03-15 12:01:39

from typing import Dict, Any, List
import torch
import multiprocessing
from ..engine import Engine
from .core import WhisperCore
from gailbot.core.utils.general import (
    get_extension
)
from gailbot.configs import  whisper_config_loader
from gailbot.core.utils.logger import makelogger
logger = makelogger("Whisper Engine")

WHISPER_CONFIG = whisper_config_loader()

class WhisperEngine(Engine):

    def __init__(self):
        self.core = WhisperCore()
        self._successful = False

    def __str__(self):
        """Returns the name of the function"""
        return WHISPER_CONFIG.engine_name

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        return self.core.__repr__()

    #### Engine API Methods

    def transcribe(
        self,
        audio_path : str,
        payload_workspace : str,
        language : str = None,
        detect_speakers : bool = False,
    ) -> List[Dict]:
        """Use the engine to transcribe an item"""
        results = self.core.transcribe(audio_path, language, detect_speakers)
        self._successful = True
        return results

    def was_transcription_successful(self) -> bool:
        return self._successful

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.
        """
        return WHISPER_CONFIG.engine_name

    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.
        """
        return self.core.get_supported_formats()

    def is_file_supported(self, filepath: str) -> bool:
        """
        Determine if the given file is supported by the engine.
        """
        return get_extension(filepath) in self.get_supported_formats()

    #### Additional methods

    def get_available_models(self) -> List[str]:
        """return the list of available model
        """
        return self.core.get_available_models()

    def get_supported_languages(self) -> List[str]:
        """ return the list of available languages 
        """
        return self.core.get_supported_languages()