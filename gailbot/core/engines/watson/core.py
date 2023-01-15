# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:25:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 16:07:48


from typing import List, Any, Dict
import time
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource

from gailbot.configs.utils import get_engine_conf

ENGINE_CONF = get_engine_conf("watson")

class WatsonCore:

    # TODO: This needs to load the configs somehow

    def __init__(self, apikey : str, region : str,):
        pass

    @property
    def supported_formats(self) -> List[str]:
        pass

    @property
    def regions(self) -> Dict:
        pass

    @property
    def defaults(self) -> Dict:
        pass

    def websockets_recognize(
        self,
        audio_path : str,
        out_dir : str,
        recognize_callback : RecognizeCallback,
        base_language_model : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> Any:
        pass
