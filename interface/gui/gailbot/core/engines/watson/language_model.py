# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 15:20:18
# Standard library imports
from typing import Any, BinaryIO, List, TextIO, Tuple, Dict, Callable, Union
from enum import IntEnum
# Local imports

# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import CustomWord


class WatsonReturnCodes(IntEnum):
    """
    Return codes from Watson.
    """
    ok = 200
    created = 201
    notFound = 404
    notAcceptable = 406
    unsupported = 415


class WatsonLanguageModel:
    """
    Responsible for interacting with the IBM Watson STT service and providing
    methods for interacting with language models.
    """
    # Mappings from region to the region url.
    regions = {
        "dallas": "https://api.us-south.speech-to-text.watson.cloud.ibm.com",
        "washington": "https://api.us-east.speech-to-text.watson.cloud.ibm.com",
        "frankfurt": "https://api.eu-de.speech-to-text.watson.cloud.ibm.com",
        "sydney": "https://api.au-syd.speech-to-text.watson.cloud.ibm.com",
        "tokyo": "https://api.jp-tok.speech-to-text.watson.cloud.ibm.com",
        "london": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com",
        "seoul": "https://api.kr-seo.speech-to-text.watson.cloud.ibm.com"}

    def __init__(self) -> None:
        self.stt = None
        self.connected_to_service = False

    # base model methods

    def get_base_model(self, model_name: str) -> Union[Dict[str, Any], None]:
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
        if not self.connected_to_service:
            return
        _, resp = self._execute_watson_method(
            self.stt.get_model, [WatsonReturnCodes.ok], [model_name], {})
        return resp

    def get_base_models(self) -> List[str]:
        """
        Obtain a list of the names of base language models that are supported.

        Returns:
            (List[str]): Names of the base language models.
        """
        if not self.connected_to_service:
            return []
        names = list()
        success, resp = self._execute_watson_method(
            self.stt.list_models, [WatsonReturnCodes.ok])
        if success:
            for model in resp["models"]:
                names.append(model["name"])
        return names

    # Custom model methods

    def get_custom_model(self, customization_id: str) \
            -> Union[Dict[str, Any], None]:
        """
        Obtain information regarding a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (Union[Dict[str,Any],None]):
                Mapping from the following keys to their values:
                customization_id, created, updated,language, dialect,
                versions, owner, name, description, base_model_name, status,
                progress
                None if unsuccessful.
        """
        if not self.connected_to_service:
            return
        success, resp = self._execute_watson_method(
            self.stt.get_language_model, [WatsonReturnCodes.ok],
            [customization_id])
        return resp if success else None

    def get_custom_models(self) -> Dict[str, str]:
        """
        Obtain all custom language models.

        Returns:
            (Dict[str,str]):
                 Mapping from custom model name to the customization id.
        """
        if not self.connected_to_service:
            return {}
        custom_models = dict()
        success, resp = self._execute_watson_method(
            self.stt.list_language_models, [WatsonReturnCodes.ok])
        if success:
            for model in resp["customizations"]:
                custom_models[model["name"]] = model["customization_id"]
        return custom_models

    def create_custom_model(self, name: str, base_model_name: str,
                            description: str) -> bool:
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
        if not self.connected_to_service or \
                name in self.get_custom_models().keys():
            return False
        success, _ = self._execute_watson_method(
            self.stt.create_language_model, [WatsonReturnCodes.created],
            [name, base_model_name], {"description": description})
        return success

    def delete_custom_model(self, customization_id: str) -> bool:
        """
        Delete an existing custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_language_model, [WatsonReturnCodes.ok],
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
        success, resp = self._execute_watson_method(
            self.stt.train_language_model, [WatsonReturnCodes.ok],
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
        success, _ = self._execute_watson_method(
            self.stt.reset_language_model, [WatsonReturnCodes.ok],
            [customization_id])
        return success

    def upgrade_custom_model(self, customization_id: str) -> bool:
        """
        Upgrade the base model of the custom language model to its latest
        version.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.upgrade_language_model, [WatsonReturnCodes.ok],
            [customization_id])
        return success

    # Custom corpora methods

    def get_corpora(self, customization_id: str) -> Union[List[Dict], None]:
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
        success, resp = self._execute_watson_method(
            self.stt.list_corpora, [WatsonReturnCodes.ok], [customization_id])
        if success:
            return resp["corpora"]

    def add_corpus(self, customization_id: str, corpus_name: str,
                   corpus_file: BinaryIO) -> bool:
        """
        Add a corpus to the specified custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            corpus_name (str): Name of the corpus
            corpus_file (BinaryIO): utf-8 encoded plain text file.
        """
        success, _ = self._execute_watson_method(
            self.stt.add_corpus, [WatsonReturnCodes.created],
            [customization_id, corpus_name, corpus_file, True])
        return success

    def delete_corpus(
            self, customization_id: str, corpus_name: str) -> bool:
        """
        Delete a corpus from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            corpus_name (str): Name of the corpus to delete.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_corpus, [WatsonReturnCodes.ok]
            [customization_id, corpus_name])
        return success

    def get_corpus(
        self, customization_id: str, corpus_name: str) \
            -> Union[Dict[str, Any], None]:
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
        _, resp = self._execute_watson_method(
            self.stt.get_corpus, [WatsonReturnCodes.ok],
            [customization_id, corpus_name])
        return resp

    # Custom words methods

    def get_custom_words(
            self, customization_id: str) -> Union[List[Dict], None]:
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
        success, resp = self._execute_watson_method(
            self.stt.list_words, [WatsonReturnCodes.ok],
            [customization_id])
        if success:
            return resp["words"]

    def add_custom_words(
            self, customization_id: str, words: List[str]) -> bool:
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
        success, _ = self._execute_watson_method(
            self.stt.add_words, [WatsonReturnCodes.created],
            [customization_id, custom_words])
        return success

    def delete_custom_word(
            self, customization_id: str, word: str) -> bool:
        """
        Delete a word from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            word (str): Word to delete.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_word, [WatsonReturnCodes.ok],
            [customization_id, word])
        return success

    # Custom grammars methods

    def get_custom_grammars(self, customization_id: str) \
            -> Union[List[Dict], None]:
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
        success, resp = self._execute_watson_method(
            self.stt.list_grammars, [customization_id])
        if success:
            return resp["grammars"]

    def get_custom_grammar(
            self, customization_id: str, grammar_name: str) \
            -> Union[Dict, None]:
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
        _, resp = self._execute_watson_method(
            self.stt.get_grammar, [WatsonReturnCodes.ok],
            [customization_id, grammar_name])
        return resp

    def add_custom_grammar(self, customization_id: str,
                           grammar_name: str, grammar_file: TextIO,
                           content_type: str) -> bool:
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
        success, _ = self._execute_watson_method(
            self.stt.add_grammar, [WatsonReturnCodes.created],
            [customization_id, grammar_name, grammar_file, content_type, True])
        return success

    def delete_custom_grammar(
            self, customization_id: str, grammar_name: str) -> bool:
        """
        Delete the specific grammar from a custom language model.

        Args:
            customization_id (str): Unique ID of the custom language model.
            grammar_name (str): Name of the custom grammar.

        Returns:
            (bool): True if successfully added. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_grammar, [WatsonReturnCodes.ok],
            [customization_id, grammar_name])
        return success

    # Others

    def connect_to_service(self, api_key: str, region: str) -> bool:
        """
        Connect to the stt service using the given api key.
        Must be called before other methods can be used.

        Args:
            apikey (str): Valid API key for the watson STT service.

        Returns:
            (bool): True if connected successfully. False otherwise.
        """
        if not region in self.regions.keys() or \
                not self._is_api_key_valid(api_key, self.regions[region]):
            self.connected_to_service = False
            return False
        self.stt = self._initialize_stt_service(api_key)
        self.stt.set_service_url(self.regions[region])
        self.connected_to_service = True
        return True

    ############################# PRIVATE METHODS ############################

    def _is_api_key_valid(self, apikey: str, url : str) -> bool:
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

    def _execute_watson_method(self, method: Callable,
                               expected_response_codes: List[WatsonReturnCodes], args: List = [],
                               kwargs: Dict = {}) -> Tuple[bool, Any]:
        """
        Execute a watson method only if connected to watson.

        Args:
            method (Callable): Method to execute.
            expected_response_codes (List[WatsonReturnCodes]):
                Watson codes that are expected for a successful response.
            args (List): Arguments to pass to the method.
            kwargs (Dict): Keyword arguments to method

        Returns:
            (Tuple[bool,Any]):
                True + result if successful. False + None otherwise.
        """
        if not self.connected_to_service:
            return (False, None)
        try:
            resp = method(*args, **kwargs)
            if any([resp.get_status_code() == expected
                    for expected in expected_response_codes]):
                return (True, resp.get_result())
            return (False, None)
        except ApiException as e:
            return (False, e)
