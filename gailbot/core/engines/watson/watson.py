# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:45:46

from typing import Dict, Any, List

from .core import WatsonCore
from .lm import WatsonLMInterface
from .am import WatsonAMInterface
from ..engine import Engine

# TODO: Need to give the engine direct access to the config file.
class Watson(Engine):

    ENGINE_NAME = "watson"

    def __init__(
        self,
        apikey : str,
        region : str
    ):
        self.apikey = apikey
        self.region = region
        self.core = WatsonCore(apikey, region)
        self.lm = WatsonLMInterface(apikey ,region)

    def __str__(self):
        return self.ENGINE_NAME

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        return (
            f"api_key: {self.api_key}" \
            f"region: {self.region}"
        )


    @property
    def supported_formats(self) -> List[str]:
        pass

    @property
    def regions(self) -> Dict:
        pass

    @property
    def defaults(self) -> Dict:
        pass

    def transcribe(
        self,
        audio_path : str,
        base_model : str,
        out_dir : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> str:
        """Use the engine to transcribe an item"""
        pass

    def language_customization_interface(self) -> WatsonLMInterface:
        return self.lm

    def acoustic_customization_interface(self) -> WatsonAMInterface:
        return self.am