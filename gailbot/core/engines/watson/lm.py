# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:30:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:39:44

# Standard library imports
from typing import Any, BinaryIO, List, TextIO, Tuple, Dict, Callable, Union
from enum import IntEnum
# Local imports

# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import CustomWord

# TODO: Should aldo directly get access to config files
class WatsonLMInterface:

    def __init__(self, apikey : str, region : str):
        pass

    def get_base_models(self) -> List[str]:
        """
        Obtain a list of the names of base language models that are supported.
        """
        pass

    def get_base_model(self, model_name : str) -> Dict:
        pass

    def get_custom_model(
        self,
        customization_id: str
    ) -> Dict:
        pass

    def get_custom_models(self) -> Dict[str, str]:
        pass

    def create_custom_model(
        self,
        base_model_name : str,
        description : str
    ):
        pass

    def delete_custom_model(self, customization_id: str) -> bool:
        pass

    def train_custom_model(self, customization_id: str) -> bool:
        pass

    def reset_custom_model(self, customization_id: str) -> bool:
        pass

    def upgrade_custom_model(self, customization_id: str) -> bool:
        pass

    def get_corpora(self, customization_id: str) -> Dict:
        pass

    def add_corpus(
        self,
        customization_id: str,
        corpus_name: str,
        corpus_file: BinaryIO
    ) -> bool:
        pass

    def delete_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> bool:
        pass

    def get_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> Dict:
        pass

    def get_custom_works(
        self,
        customization_id : str
    ) -> List[Dict]:
        pass

    def add_custom_works(
        self,
        customization_id : str,
        words : List[str]
    ) -> bool:
        pass

    def delete_custom_words(
        self,
        customization_id : str,
        word : str
    ) -> bool:
        pass

    def get_custom_grammars(
        self,
        customization_id : str
    ) -> List[Dict]:
        pass

    def get_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> Dict:
        pass

    def add_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str,
        grammar_file: TextIO,
        content_type: str
    ) -> bool:
        pass

    def delete_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> bool:
        """
        Delete the specific grammar from a custom language model.
        """
        pass

    # Others
