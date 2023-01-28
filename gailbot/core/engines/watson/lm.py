# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:30:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 12:00:25

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



# TODO: Should aldo directly get access to config files
class WatsonLMInterface:

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

    def get_base_model(self, model_name : str) -> Dict:
        """
        Obtain information regarding the given base language model.
        """
        resp = self._execute_watson_method(
            self.stt.get_model, [WatsonReturnCodes.OK], model_name
        )
        return resp


    def get_base_models(self) -> List[str]:
        """
        Obtain a list of the names of base language models that are supported.
        """
        resp = self._execute_watson_method(
            self.stt.list_models, [WatsonReturnCodes.OK]
        )
        return [model["name"] for model in resp["models"]] if resp != None else []

    def get_custom_model(
        self,
        customization_id: str
    ) -> Dict:
        """
        Obtain information regarding a custom language model.
        """
        resp = self._execute_watson_method(
            self.stt.get_language_model, [WatsonReturnCodes.OK], customization_id
        )
        return resp

    def get_custom_models(self) -> Dict[str, str]:
        """
        Get custom language models
        """
        custom_models = dict()
        resp = self._execute_watson_method(
            self.stt.list_language_models, [WatsonReturnCodes.OK]
        )
        if resp != None:
            for model in resp["customizations"]:
                custom_models[model["name"]] = model["customization_id"]
        return custom_models

    def create_custom_model(
        self,
        base_model_name : str,
        description : str
    ):
        """
        Create a new custom language model.
        Does NOT create a new model if one with the same name already exists.
        """
        raise NotImplementedError()

    def delete_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def train_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def reset_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def upgrade_custom_model(self, customization_id: str) -> bool:
        raise NotImplementedError()

    def get_corpora(self, customization_id: str) -> Dict:
        raise NotImplementedError()

    def add_corpus(
        self,
        customization_id: str,
        corpus_name: str,
        corpus_file: BinaryIO
    ) -> bool:
        raise NotImplementedError()

    def delete_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> bool:
        raise NotImplementedError()

    def get_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> Dict:
        raise NotImplementedError()

    def get_custom_works(
        self,
        customization_id : str
    ) -> List[Dict]:
        raise NotImplementedError()

    def add_custom_works(
        self,
        customization_id : str,
        words : List[str]
    ) -> bool:
        raise NotImplementedError()

    def delete_custom_words(
        self,
        customization_id : str,
        word : str
    ) -> bool:
        raise NotImplementedError()

    def get_custom_grammars(
        self,
        customization_id : str
    ) -> List[Dict]:
        raise NotImplementedError()

    def get_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> Dict:
        raise NotImplementedError()

    def add_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str,
        grammar_file: TextIO,
        content_type: str
    ) -> bool:
        raise NotImplementedError()

    def delete_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> bool:
        """
        Delete the specific grammar from a custom language model.
        """
        raise NotImplementedError()

    # Others

    def _execute_watson_method(
        self,
        method : Callable,
        expected_response_codes: List[WatsonReturnCodes],
        *args,
        **kwargs

    ) -> Any:
        try:
            resp = method(*args, **kwargs)
            if any([resp.get_status_code() == expected
                        for expected in expected_response_codes]):
                return resp.get_result()
        except ApiException as e:
            logger.log(f"Exception raised: {e}")
