# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:30:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 12:00:25

""" TODO:
1. only function to create and delete model are tested 
   function to train the model are not tested 
"""
# Standard library imports
from typing import Any, BinaryIO, List, TextIO, Tuple, Dict, Callable, Union
from enum import IntEnum
# Local imports

# Third party imports
from gailbot.configs import watson_config_loader
from gailbot.core.engines import exception as ERR
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import CustomWord

from gailbot.core.utils.media import MediaHandler

import logging
logger = logging.getLogger(__name__)

from .codes import WatsonReturnCodes

WATSON_CONFIG = watson_config_loader()
class WatsonLMInterface:
    def __init__(self, apikey : str, region : str):
        self.connected_to_service = False
        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()

        # Parse confs
        self._regions = WATSON_CONFIG.regions_uris
        self._format_to_content_types = WATSON_CONFIG.format_to_content
        self._defaults = WATSON_CONFIG.defaults
        self.max_size_bytes = WATSON_CONFIG.max_file_size_bytes

        if not self._is_api_key_valid(apikey, self._regions[region]):
            raise Exception(f"Apikey {apikey} invalid")
        if not region in self._regions:
            raise Exception(
                f"Region {region} not in {list(self._regions.keys())}"
            )

        try:
            # Create the stt service and run
            authenticator = IAMAuthenticator(self.apikey)
            self.stt = SpeechToTextV1(authenticator=authenticator)
            self.stt.set_service_url(self._regions[self.region])
        except:
            raise Exception("Connect to STT failed")
        else:
            self.connected_to_service = True 
        
    def get_base_model(self, model_name : str) -> Dict:
        """
        Obtain information regarding the given base language model.

        Args:
            model_name (str): Name of the language model.

        Returns:
            (Union[Dict[str,Any],None]):
                Dictionary with keys: name, language, rate, url,
                supported_features, description if successful.
                None if unsuccessful.
        """
        if not self.connected_to_service: return {}
        resp = self._execute_watson_method(
            self.stt.get_model, [WatsonReturnCodes.OK], model_name
        )
        return resp

    def get_base_models(self) -> List[str]:
        """
        Obtain a list of the names of base language models that are supported.

        Returns:
            (List[str]): Names of the base language models.
        """
        if not self.connected_to_service: return []
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

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (Union[Dict[str,Any],None]):
                Mapping from the following keys to their values:
                customization_id, CREATED, updated,language, dialect,
                versions, owner, name, description, base_model_name, status,
                progress
                None if unsuccessful.
        """
        if not self.connected_to_service: return []
        resp = self._execute_watson_method(
            self.stt.get_language_model, [WatsonReturnCodes.OK], customization_id
        )
        return resp

    def get_custom_models(self) -> Dict[str, str]:
        """
        Get custom language models

        Returns:
            (Dict[str,str]):
                 Mapping from custom model name to the customization id.
        """
        if not self.connected_to_service: return {}
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
        name: str, 
        base_model_name : str,
        description : str
    ):
        """
        Create a new custom language model.
        Does NOT create a new model if one with the same name already exists.

        Args:
            name (str): Name of the model.
            base_model_name (str):
                Name of the base model. Must be a supported base model.
            description (str): Description of the model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.connected_to_service or name in self.get_custom_models().keys():
            return False
        response = self._execute_watson_method(
            self.stt.create_language_model, [WatsonReturnCodes.CREATED],
            [name, base_model_name], {"description": description})
        return response

    def delete_custom_model(self, customization_id: str) -> bool:
        """
        Delete an existing custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success = self._execute_watson_method(
            self.stt.delete_language_model, [WatsonReturnCodes.OK],
            [customization_id])
        return success

    def train_custom_model(self, customization_id: str) -> bool:
        """
        Train a custom language model with a previously added resource.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success = self._execute_watson_method(
            self.stt.train_language_model, [WatsonReturnCodes.OK],
            [customization_id])
        return success
   
    def reset_custom_model(self, customization_id: str) -> bool:
        """
        Reset a custom language model to remove all loaded resources.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.reset_language_model, [WatsonReturnCodes.OK],
            [customization_id])
        return response
    
    def upgrade_custom_model(self, customization_id: str) -> bool:
        """
        Upgrade the base model of the custom language model to its latest
        version.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.upgrade_language_model, [WatsonReturnCodes.OK],
            [customization_id])
        return response
    
    def get_corpora(self, customization_id: str) -> Dict:
        """
        Obtain the corpora used to train this custom model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (Union[List[Dict],None]):
                Each internal dict contains the keys: name,
                out_of_vocabulary_words,total_words, status.
                None if unsuccessful.
        """
        response = self._execute_watson_method(
            self.stt.list_corpora, [WatsonReturnCodes.OK], [customization_id])
        if response:
            return response["corpora"]

    def add_corpus(
        self,
        customization_id: str,
        corpus_name: str,
        corpus_file: BinaryIO
    ) -> bool:
        """
        Add a corpus to the specified custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            corpus_name (str): Name of the corpus
            corpus_file (BinaryIO): utf-8 encoded plain text file.
        """
        response = self._execute_watson_method(
            self.stt.add_corpus, [WatsonReturnCodes.CREATED],
            [customization_id, corpus_name, corpus_file, True])
        return response

    def delete_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> bool:
        """
        Delete a corpus from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            corpus_name (str): Name of the corpus to delete.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.delete_corpus, 
            [WatsonReturnCodes.OK], 
            [customization_id, corpus_name])
        return response

    def get_corpus(
        self,
        customization_id: str,
        corpus_name: str
    ) -> Dict:
        """
        Obtain information about a specific custom corpus used to train the
        custom model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            corpus_name (str): Name of the corpus.

        Returns:
            (Union[Dict[str,Any],None]): Contains the keys: "name",
            "out_of_vocabulary_words", "total_words","status"
            None if unsuccessful.
        """
        response = self._execute_watson_method(
            self.stt.get_corpus, [WatsonReturnCodes.OK],
            [customization_id, corpus_name])
        return response
    
    def get_custom_works(
        self,
        customization_id : str
    ) -> List[Dict]:
        """
        Obtain all the custom words used to train a custom model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (Union[List[Dict], None]):
                Each dictionary contains the keys: "word","sounds_like",
                "display_as","count","source"
                None if unsuccessful.
        """
        response = self._execute_watson_method(
            self.stt.list_words, [WatsonReturnCodes.OK],
            [customization_id])
        if response:
            return response["words"]

    def add_custom_works(
        self,
        customization_id : str,
        words : List[str]
    ) -> bool:
        """
        Add one or more custom words to the specified custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            words (List[str]): List of words to add to the model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        custom_words = list()
        for word in words:
            custom_words.append(CustomWord(word=word))
        response = self._execute_watson_method(
            self.stt.add_words, [WatsonReturnCodes.CREATED],
            [customization_id, custom_words])
        return response
    
    def delete_custom_words(
        self,
        customization_id : str,
        word : str
    ) -> bool:
        """
        Delete a word from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            word (str): Word to delete.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.delete_word, [WatsonReturnCodes.OK],
            [customization_id, word])
        return response

    def get_custom_grammars(
        self,
        customization_id : str
    ) -> List[Dict]:
        """
        Obtain a list of the grammars of a custom model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (Union[List[Dict], None]):
                Internal dictionaries contain the keys:
                out_of_vocabulary_words","name","status"
                None of unsuccessful.
        """
        response = self._execute_watson_method(
            self.stt.list_grammars, [customization_id])
        if response:
            return response["grammars"]
        
    def get_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> Dict:
        """
        Obtain information about a specific grammar in a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            grammar_name (str): Name of the custom grammar.

        Returns:
            (Union[Dict, None]):
                Contains the keys: "out_of_vocabulary_words","name","status"
                None of unsuccessful.
        """
        response = self._execute_watson_method(
            self.stt.get_grammar, [WatsonReturnCodes.OK],
            [customization_id, grammar_name])
        return response

    def add_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str,
        grammar_file: TextIO,
        content_type: str
    ) -> bool:
        """
        Add a grammar to the custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            grammar_name (str): Name of the custom grammar.
            grammar_file (TextIO): Plain text file containing grammar.
            content_type (str):
                Format of the grammar. one of:
                    application/srgs, application/srgs+xml

        Returns:
            (bool): True if successfully added. False otherwise.
        """
        response  = self._execute_watson_method(
            self.stt.add_grammar, [WatsonReturnCodes.CREATED],
            [customization_id, grammar_name, grammar_file, content_type, True])
        return response

    def delete_custom_grammar(
        self,
        customization_id: str,
        grammar_name: str
    ) -> bool:
        """
        Delete the specific grammar from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            grammar_name (str): Name of the custom grammar.

        Returns:
            (bool): True if successfully added. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.delete_grammar, [WatsonReturnCodes.OK],
            [customization_id, grammar_name])
        return response

    # Others
    def _execute_watson_method(
        self,
        method : Callable,
        expected_response_codes: List[WatsonReturnCodes],
        args: List = [],
        kwargs: Dict = {}
    ) -> Union[bool, Any]:
        """
        Execute a watson method only if connected to watson.

        Args:
            method (Callable): Method to execute.
            expected_response_codes (List[WatsonReturnCodes]):
                Watson codes that are expected for a successful response.
            args (List): Arguments to pass to the method.
            kwargs (Dict): Keyword arguments to method

        Returns:
            (Union[bool,Any]):
                result from watson if successful. 
                False otherwise.
        """
        if not self.connected_to_service:
            raise ERR.ConnectionError("Error raised: connection error")
        try:
            resp = method(*args, **kwargs)
            if any([resp.get_status_code() == expected
                        for expected in expected_response_codes]):
                return resp.get_result()
            raise ERR.WatsonMethodExecutionError
        except ApiException as e:
            logger.info(f"Exception raised: {e}", exc_info=e)
            return False
        except ERR.WatsonMethodExecutionError as e:
            logger.info(f"Exception raised: {e}", exc_info=e)
            return False
        
    def _is_api_key_valid(self, apikey: str, url: str) -> bool:
        """
        Determine if the given apikey is valid.

        Args:
            apikey (str): API key for the watson STT service.

        Returns:
            (bool): True if the key is valid. False otherwise.
        """
        try:
            stt = self._initialize_stt_service(apikey)
            stt.set_service_url(url)
            stt.list_models()
            return True
        except:
            return False

    def _initialize_stt_service(self, apikey: str) -> SpeechToTextV1:
        """
        Initialize a SpeechToTextV1 object given an apikey.

        Args:
            apikey (str): Valid API key for the watson STT service.

        Returns:
            (SpeechToTextV1)
        """
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        return stt