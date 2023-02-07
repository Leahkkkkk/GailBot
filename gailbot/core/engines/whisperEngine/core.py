# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:09:26
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-01 12:36:57

import sys
import os
import json
from typing import List, Dict, Any

import torch

import gailbot.core.engines.whisperEngine.whisperTimestamped as whisper

from gailbot.core.engines.whisperEngine.whisperTimestamped.utils import (
    force_cudnn_initialization
)

from .diarization.pyannote_diarization import DiarizationPipeline


from gailbot.core.utils.general import (
    is_file,
    is_directory,
    make_dir
)


# TODO: All of the vars here should be moved to a config file.
_WORKSPACE = "whisper_workspace"
# TODO: Just adding this because we have not tested other formats.
# However, the load audio method will most likely support other formats
# as well.
_FORMATS = ("wav",)

class WhisperCore:
    """
    We are using this class as an adapter for the engine so that we can use
    multiple different instances of the underlying whisper package is required.
    """

    def __init__(
        self,
        model_name : str,
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
        self.model_name = model_name



        self.model_cache_dir = model_cache_dir

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        #  This is where the model outputs are saved but we might not need this

        self.punctuations_with_words = punctuations_with_words
        self.compute_confidence = compute_confidence
        self.sampling_temperature = sampling_temperature
        self.best_of = best_of
        self.beam_size = beam_size
        self.beam_decoding_patience = beam_decoding_patience
        self.length_penalty = length_penalty
        self.suppress_tokens = suppress_tokens
        self.condition_on_previous_text = condition_on_previous_text
        self.fp16  = fp16,
        self.fp16temperature_increment_on_fallback = temperature_increment_on_fallback
        self.compression_ratio_threshold = compression_ratio_threshold
        self.logprob_threshold = logprob_threshold
        self.no_speech_threshold = no_speech_threshold
        self.num_threads = num_threads
        # If True, print out all debug messages etc.
        self.verbose = verbose

        if self.device.lower().startswith("cuda"):
            force_cudnn_initialization(self.device)

        self.model = whisper.load_model(self.model_name,device=self.device)

        self.diarization_pipeline = DiarizationPipeline()

    def transcribe(
        self,
        audio_path : str,
        outdir : str,
        language : str = None
    ):
        assert is_file(audio_path), \
            f"Not a file: {audio_path}"

        outdir = os.path.join(_WORKSPACE, outdir)
        make_dir(outdir, overwrite=True)

        if language != None and not language in self.get_supported_languages():
            raise Exception(
                f"Unsupported language, must be one of: {language}"
            )

        # Identify the speaker chunks
        speaker_timing_map = \
            self.diarization_pipeline.identity_speaker_chunks(audio_path)

        # Load the audio and models, transcribe, and return the parsed result
        audio = whisper.load_audio(audio_path)
        result = whisper.transcribe(self.model, audio, language=language)

        word_dicts : List[Dict] = whisper.parse_into_word_dicts(result)

        # TODO: Add speaker diarization capability once that is fixed.
        return word_dicts

        # print(word_dicts)
        # print(speaker_timing_map)

        # # Merge the result of the speaker map and the whisper results
        # # TODO: This can def. be made more efficient.
        # for word_dict in word_dicts:
        #     assigned = False
        #     # Figure out if there is a speaker label.
        #     for label, timings in speaker_timing_map.items():
        #         for (start, end) in timings:
        #             if word_dict["start"] >= start and word_dict["end"] <= end:
        #                 word_dict["speaker"] = label
        #                 assigned = True
        #                 break
        #         if assigned:
        #             break
        # return word_dicts



        # print(json.dumps(whisper.parse_into_full_text(result), indent = 2, ensure_ascii = False))
        # return whisper.parse_into_word_dicts(result)

    def get_supported_formats(self) -> List[str]:
        return list(_FORMATS)

    def get_available_models(self) -> List[str]:
        return whisper.available_models()

    def get_supported_languages(self) -> List[str]:
        return whisper.supported_languages()


    ################ PRIVATE METHODS




