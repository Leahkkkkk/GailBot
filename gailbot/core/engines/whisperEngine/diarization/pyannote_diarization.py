# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 17:35:21
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 18:56:41


from typing import List, Dict, Any
import re

import itertools
import operator

from pyannote.audio import Pipeline

from gailbot.core.utils.general import (
    is_file,
    get_extension
)

import logging
logger = logging.getLogger()

# TODO: This should be added to the config file.
# Instructions for pyannote setup: https://github.com/pyannote/pyannote-audio
# NOTE: Needed for huggingface: https://huggingface.co/settings/tokens
_HF_AUTH_TOKEN = "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"
_PYANNOTE_PIPELINE_NAME = "pyannote/speaker-diarization"
_SUPPORTED_FORMATS = ("wav", )


# TODO: Move the config and model into the config dir. probably. Doesn't make
# sense to keep it locally
# TODO: Change the paths on the config file to make sure it works on
# other machines too - do NOT hard code the local path.

_PIPELINE_CONFIG_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/gailbot/core/engines/whisperEngine/diarization/config.yaml"


# TODO: Local models not working rn - using remote.

###### UTILITY METHODS ########

def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s


class DiarizationPipeline:

    def __init__(self):
        self.pipeline = Pipeline.from_pretrained( _PIPELINE_CONFIG_PATH)
        # self.pipeline = Pipeline.from_pretrained(
        #     _PYANNOTE_PIPELINE_NAME, use_auth_token= _HF_AUTH_TOKEN
        # )

    def identity_speaker_chunks(
        self,
        audio_path : str,
        chunk_audio_by_groups : bool = True
    ):

        assert is_file(audio_path) and \
            get_extension(audio_path) in _SUPPORTED_FORMATS

        # Apply the diarization pipeline on the audio
        diarization = self.pipeline(audio_path)
        grouped_map = self._group_dz_by_speaker(diarization)
        print(grouped_map)


    def get_supported_formats(self) -> List[str]:
        return list(_SUPPORTED_FORMATS)

    def _group_dz_by_speaker(self, diarization):
        diarization = list(diarization.itertracks(yield_label = True))
        diarization = sorted(diarization, key=operator.itemgetter(2))
        grouped = dict()
        for i, g in itertools.groupby(diarization, key=operator.itemgetter(2)):
            segments = [g[0] for g in g]
            times = [(s.start, s.end) for s in segments]
            grouped[i] = times
        return grouped





