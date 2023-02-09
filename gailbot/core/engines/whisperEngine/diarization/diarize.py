# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-02-07 16:12:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 18:10:38

import sys
import os
from typing import Any
from huggingface_hub import hf_hub_url, cached_download
import joblib
from huggingface_hub import hf_hub_download
from pyannote.audio import Pipeline

from gailbot.core.utils.general import (
    make_dir,
    read_yaml,
    write_yaml,
    is_directory
)
from gailbot.core.utils.download import is_internet_connected
from gailbot.configs import  whisper_config_loader
from gailbot.core.utils.logger import makelogger

logger = makelogger("pyannote_diarization")


WHISPER_CONFIG = whisper_config_loader()

class PyannoteDiarizer:
    """
    Class containing the functionality for creating and managing the diarization 
        for WHISPER transcripts 
    """

    def __init__(
        self,
        cache_dir : str
    ):

        self.cache_dir = os.path.join(cache_dir,"pyannote")
        make_dir(self.cache_dir,overwrite=False)

        if not is_internet_connected():
            logger.warning("Internet connection not detected...")

        # Download the model
        model_path = hf_hub_download(
            repo_id = WHISPER_CONFIG.diarization_configs.HF_diarization_model_repo_id,
            filename = WHISPER_CONFIG.diarization_configs.model_filename,
            token = WHISPER_CONFIG.diarization_configs.HF_auth_token,
            cache_dir=self.cache_dir
        )
        logger.info(f"Using diarization model from path: {model_path}")

        config_path =  hf_hub_download(
            repo_id = WHISPER_CONFIG.diarization_configs.HF_diarization_config_repo_id,
            filename = WHISPER_CONFIG.diarization_configs.config_filename,
            token = WHISPER_CONFIG.diarization_configs.HF_auth_token,
            cache_dir=self.cache_dir
        )
        logger.info(f"Using diarizaton configuration from path: {config_path}")

        # Read the config and update the model path
        config = read_yaml(config_path)
        config["pipeline"]["params"]["segmentation"] = model_path
        write_yaml(config_path, config,overwrite=True)

        self.pipeline = Pipeline.from_pretrained(
            config_path
        )

    def __call__(
        self,
        audio_path : str,
    ) -> Any:
        """
        Get speaker diarization for the given audio.

        Args:
            audio_path = string containing the path to the audio for which 
                to get the speaker diarization.
        
        Returns:
            Pipeline containing the diarization for the given audio file.
        """
        return self.pipeline(audio_path)

