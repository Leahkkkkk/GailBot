# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 17:53:15

from typing import Dict, Any, List
import torch
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

    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
        self.core = WhisperCore(workspace_dir)
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
        language : str = None,
        detect_speakers : bool = False
    ) -> List[Dict]:
        """Use the engine to transcribe an item"""
        logger.info(f"get transcribe request audio_path: {audio_path}, language: {language}, detect_speakers: {detect_speakers}")
        results = self.core.transcribe(audio_path,language, detect_speakers)
        self._successful = True
        logger.info(f"transcription result {results}")
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
        return self.core.get_available_models()

    def get_supported_languages(self) -> List[str]:
        return self.core.get_supported_languages()