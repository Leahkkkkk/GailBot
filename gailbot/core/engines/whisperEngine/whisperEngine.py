# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 16:31:47

from typing import Dict, Any, List
import torch

from ..engine import Engine

from .core import WhisperCore

from gailbot.core.utils.general import (
    get_extension
)



class WhisperEngine(Engine):

    ENGINE_NAME = "whisper"

    # TODO: Move most of these to the config file, since almost none
    # of them should come from the user in our use case.
    # TODO: These configs should be loaded directly by core.
    def __init__(
        self,
        model : str,
        model_cache_dir : str,
        punctuations_with_words : bool = True,
        compute_confidence : bool = True,
        sampling_temperature : float = 0.0,
        best_of : int = None,
        beam_size : int = None,
        beam_decoding_patience : float = None,
        length_penalty : float = None,
        suppress_tokens : str = "-1",
        condition_on_previous_text : bool = True,
        fp16  = None,
        temperature_increment_on_fallback : float = 0.0,
        compression_ratio_threshold : float = 2.4,
        logprob_threshold : float = -1,
        no_speech_threshold : float = 0.6,
        num_threads : int = 0,
        verbose = True
    ):


        self.core = WhisperCore(
            model,
            model_cache_dir,
            punctuations_with_words,
            compute_confidence,
            sampling_temperature,
            best_of,
            beam_size,
            beam_decoding_patience,
            length_penalty,
            suppress_tokens,
            condition_on_previous_text,
            fp16,
            temperature_increment_on_fallback,
            compression_ratio_threshold,
            logprob_threshold,
            no_speech_threshold,
            num_threads,
            verbose
        )
        self._successful = False

    def __str__(self):
        """Returns the name of the function"""
        return self.ENGINE_NAME

    # TODO: Make this more informative.
    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        return f"Whisper engine using backend: {self.model} "

    #### Engine API Methods

    def transcribe(
        self,
        audio_path : str,
        outdir : str,
        language : str = None
    ) -> List[Dict]:
        """Use the engine to transcribe an item"""
        results = self.core.transcribe(audio_path, outdir, language)
        self._successful = True
        return results

    def was_transcription_successful(self) -> bool:
        return self._successful

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.
        """
        return self.ENGINE_NAME

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