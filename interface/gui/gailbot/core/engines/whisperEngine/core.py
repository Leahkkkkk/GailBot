# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:09:26
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-03-15 11:43:23


import os
from threading import Lock
import json
from typing import List, Dict, Any
from dataclasses import asdict

import torch
import gailbot.core.engines.whisperEngine.whisperTimestamped as whisper
from gailbot.core.engines.whisperEngine.whisperTimestamped.utils import (
    force_cudnn_initialization
)

from .diarization.diarize import PyannoteDiarizer
from .parsers import (
    parse_into_full_text,
    parse_into_word_dicts,
    add_speaker_info_to_text
)

from .parsers import parse_into_word_dicts
from gailbot.configs import  whisper_config_loader, workspace_config_loader
from gailbot.core.utils.general import (
    is_file,
    make_dir
)
from gailbot.configs import whisper_config_loader
from gailbot.core.utils.logger import makelogger
logger = makelogger("whisper")

WHISPER_CONFIG = whisper_config_loader()
LOAD_MODEL_LOCK = Lock()

class WhisperCore:
    """
    We are using this class as an adapter for the engine so that we can use
    multiple different instances of the underlying whisper package is required.
    """

    # NOTE: Intentionally limiting the supported formats since we have
    # not tested other formats.
    # TODO: I'm not sure if this is the best place to define the supported
    # formats.
    _SUPPORTED_FORMATS = ("wav")

    def __init__(self):
        # initialize the workspace
        self.workspace_dir = workspace_config_loader().engine_ws.whisper
        logger.info(f"Whisper workspace path: {self.workspace_dir}")
        self.cache_dir = os.path.join(self.workspace_dir,"cache")
        self.models_dir = os.path.join(self.cache_dir,"models")
        self.loadModelLock = Lock()
        make_dir(self.workspace_dir,overwrite=False)
        make_dir(self.cache_dir,overwrite=False)
        make_dir(self.models_dir,overwrite=False)

        # Load a GPU is it is available
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        if self.device.lower().startswith("cuda"):
            force_cudnn_initialization(self.device)
        logger.info(f"Whisper core initialized with device: {self.device}")


    def __repr__(self) -> str:
        configs = json.dumps(
            asdict(WHISPER_CONFIG.transcribe_configs),
            indent = 2, ensure_ascii = False
        )
        return (
            f"Whisper model: {WHISPER_CONFIG.model_name}" \
            f"Transcribe configs:\n{configs}"
        )


    def transcribe(
        self,
        audio_path : str,
        language : str = None,
        detect_speaker : bool = False
    ) -> List[Dict]:
        assert is_file(audio_path), f"ERROR: Invalid file path: {audio_path}"
        
        # Load the model
        logger.info(f"start to load whisper model")
        
        global LOAD_MODEL_LOCK
        with LOAD_MODEL_LOCK:
            whisper_model = whisper.load_model(
                name=WHISPER_CONFIG.model_name,
                device=self.device,
                download_root=self.models_dir
            )
        logger.info(f"Whisper core using whisper model: {WHISPER_CONFIG.model_name}")

        # Load the diarization pipeline
        diarization_pipeline = PyannoteDiarizer(self.models_dir)
        logger.info("get the diarazation pipleine")
        logger.info(f"received setting language: {language}, detect speaker {detect_speaker} audio_path {audio_path}")
         
        if language != None and not language in self.get_supported_languages():
            raise Exception(
                f"Unsupported language, must be one of: {self.get_supported_languages()}"
            )

        if language == None:
            logger.info("No language specified - auto detecting language")

        # Load the audio and models, transcribe, and return the parsed result
        logger.info("prepare to load audio")
        audio = whisper.load_audio(audio_path)
        logger.info("audio loaded")

        asr_result = whisper.transcribe(
            whisper_model,
            audio,
            language=language,
            **asdict(WHISPER_CONFIG.transcribe_configs)
        )

        if WHISPER_CONFIG.transcribe_configs.verbose:
            logger.debug(parse_into_full_text(asr_result))

        # Apply speaker diarization
        if detect_speaker:
            if self.device == "cpu":
                logger.warning(
                    f"Performing speaker diarization on {self.device} may take upto 10x "\
                    f"the duration of the audio"
                )
            logger.info("Performing speaker diarization")
            
            try:
                dir_result = diarization_pipeline(audio_path)
                # Create and return results
                res = add_speaker_info_to_text(asr_result, dir_result)
                logger.info("get the result from parsed dict with speaker")
                return res 
            except ValueError as e:
                logger.warn(e, exc_info=e)
                return []
        else:
            res = parse_into_word_dicts(asr_result)
            logger.info("get the result from parse")
            return res  

    def get_supported_formats(self) -> List[str]:
        return list(self._SUPPORTED_FORMATS)

    def get_available_models(self) -> List[str]:
        return whisper.available_models()

    def get_supported_languages(self) -> List[str]:
        return whisper.supported_languages()


    ################ PRIVATE METHODS






