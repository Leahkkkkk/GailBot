# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-22 12:33:51
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-22 12:46:39
# Standard library imports
from typing import BinaryIO, List, Any, Callable, Tuple, Dict, Union
from enum import IntEnum
# Local imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# Third party imports


class WatsonReturnCodes(IntEnum):
    """
    Return codes from Watson.
    """
    ok = 200
    created = 201
    notFound = 404
    notAcceptable = 406
    unsupported = 415


class WatsonAcousticModel:
    """
    Responsible for interacting with the IBM Watson STT service and providing
    methods for interacting with acoustic models.
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

    # Custom acoustic models

    def get_custom_models(self) -> Dict[str, str]:
        """
        Obtain all custom acoustic models

        Returns:
            (Dict[str,str]):
                Mapping from custom acoustic model to the customization id.
        """
        custom_models = dict()
        success, resp = self._execute_watson_method(
            self.stt.list_acoustic_models, [WatsonReturnCodes.ok])
        if success:
            for model in resp["customizations"]:
                custom_models[model["name"]] = model["customization_id"]
        return custom_models

    def get_custom_model(self, customization_id: str) \
            -> Union[Dict[str, Any], None]:
        """
        Obtain information regarding a specific custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (Union[Dict[str,Any],None]):
                Mapping from the following keys to their values:
                customization_id, created, updated,language, dialect,
                versions, owner, name, description, base_model_name, status,
                progress
                None if unsuccessful.
        """
        _, resp = self._execute_watson_method(
            self.stt.get_acoustic_model, [WatsonReturnCodes.ok],
            [customization_id])
        return resp

    def create_custom_model(self, name: str, base_model_name: str,
                            description: str) -> bool:
        """
        Create a new custom acoustic model.

        Args:
            name (str): Name of the model.
            base_model_name (str):
                Name of the base model. Must be a supported base model.
            description (str): Description of the model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.create_acoustic_model, [WatsonReturnCodes.created],
            [name, base_model_name, None, description])
        return success

    def delete_custom_model(self, customization_id: str) -> bool:
        """
        Delete an existing custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_acoustic_model, [WatsonReturnCodes.ok],
            [customization_id])
        return success

    def train_custom_model(self, customization_id: str) -> bool:
        """
        Train a custom acoustic model with a previously added resource.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.train_acoustic_model, [WatsonReturnCodes.ok],
            [customization_id])
        return success

    def reset_custom_model(self, customization_id: str) -> bool:
        """
        Reset a custom acoustic model to remove all loaded resources.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.reset_acoustic_model, [WatsonReturnCodes.ok],
            [customization_id])
        return success

    def upgrade_custom_model(self, customization_id: str,
                             custom_language_model_id: str = None) -> bool:
        """
        Upgrade the base model of the custom acoustic model to its latest
        version.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.
            custom_language_model_id (str):
                ID of the custom language model (if any) that this acoustic
                model was trained with a custom language model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.upgrade_acoustic_model,
            [customization_id, custom_language_model_id])
        return success

    # Custom Audio resources

    def get_custom_audio_resources(self, customization_id: str) \
            -> Union[List[Dict], None]:
        """
        List information about all audio resources of the specified custom
        acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (Union[List[Dict],None]):
                Each internal list contains the following keys:
                "duration","name","details","status"
                None if unsuccessful.
        """
        success, resp = self._execute_watson_method(
            self.stt.list_audio, [customization_id])
        if success:
            return resp["audio"]

    def get_custom_audio_resource(self, customization_id: str,
                                  audio_name: str) -> Union[Dict, None]:
        """
        Obtain information about a specific custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.
            audio_name (str): Name of the specific audio resource.

        Returns:
            (Dict): Contains the following keys:
                    "duration","name","details","status"
                    None if unsuccessful
        """
        success, resp = self._execute_watson_method(
            self.stt.get_audio, [WatsonReturnCodes.ok],
            [customization_id, audio_name])
        if success:
            return resp

    def add_custom_audio_resource(self, customization_id: str,
                                  audio_name: str, audio_resource: BinaryIO, content_type: str)\
            -> bool:
        """
        Add an audio resource to the specific custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.
            audio_name (str): Name of the specific audio resource.
            audio_resource (BinaryIO):
                Audio resources to be added to the custom model.
            content_type (str):
                Type of the audio resource. One of:
                [application/zip,application/gzip,audio/alaw,audio/basic,
                audio/flac,audio/g729,audio/l16,audio/mp3,audio/mpeg,
                audio/mulaw,audio/ogg,audio/ogg;codecs=opus,
                audio/ogg;codecs=vorbis,audio/wav,audio/webm,
                audio/webm;codecs=opus,audio/webm;codecs=vorbis]

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.add_audio, [WatsonReturnCodes.created],
            [customization_id, audio_name, audio_resource, content_type])
        return success

    def delete_custom_audio_resource(self, customization_id: str,
                                     audio_name: str) -> bool:
        """
        Delete the specified resource from the custom audio model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.
            audio_name (str): Name of the specific audio resource.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, _ = self._execute_watson_method(
            self.stt.delete_audio, [WatsonReturnCodes.ok],
            [customization_id, audio_name])
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
        except ApiException:
            return (False, None)
