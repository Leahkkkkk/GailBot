# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:41:12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 12:01:31

# Standard library imports
from typing import Any, BinaryIO, List, TextIO, Tuple, Dict, Callable, Union
from enum import IntEnum
# Local imports

# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import CustomWord

# from gailbot.configs.utils import get_engine_conf
from gailbot.core.utils.media import MediaHandler
from gailbot.core.utils.general import (
    make_dir,
    get_extension,
    get_name,
    is_file,
    get_size
)

import logging
logger = logging.getLogger(__name__)

from .codes import WatsonReturnCodes

# _ENGINE_CONF = get_engine_conf("watson")



class WatsonAMInterface:

    def __init__(self, apikey : str, region : str):

        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()

        # Parse confs
        self._regions = _ENGINE_CONF["watson"]["regions"]['"uris']
        self._format_to_content_types = _ENGINE_CONF["watson"]["format_to_content"]
        self._defaults = _ENGINE_CONF["watson"]["defaults"]
        self.max_size_bytes = _ENGINE_CONF["watson"]["max_file_size_bytes"]

        if not self._is_api_key_valid(apikey):
            raise Exception(f"Apikey {apikey} invalid")
        if not region in self._regions:
            raise Exception(
                f"Region {region} not in {list(self._regions.keys())}"
            )

        # Create the stt service and run
        authenticator = IAMAuthenticator(self.apikey)
        self.stt = SpeechToTextV1(authenticator=authenticator)
        self.stt.set_service_url(self.regions[self.region])

    def get_custom_models(self) -> Dict:
        raise NotImplementedError()

    def get_custom_model(
        self,
        customization_id: str
    ) -> Dict:
        raise NotImplementedError()

    def get_custom_models(self) -> Dict[str, str]:
        raise NotImplementedError()

    def create_custom_model(
        self,
        base_model_name : str,
        description : str
    ):
        raise NotImplementedError()

    def delete_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def train_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def reset_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def upgrade_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def get_custom_audio_resources(self, customization_id: str) -> List[Dict]:
        raise NotImplementedError()

    def get_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str
    ) -> Dict:
        raise NotImplementedError()

    def add_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str,
        audio_resource: BinaryIO,
        content_type: str
    ) -> bool:
        raise NotImplementedError()

    def delete_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str
    ) -> bool:
        raise NotImplementedError()
