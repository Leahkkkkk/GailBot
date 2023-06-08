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
from gailbot.core.engines import exception as ERR
from ibm_watson.speech_to_text_v1 import CustomWord

from gailbot.configs import watson_config_loader
from gailbot.core.utils.media import MediaHandler

import logging
logger = logging.getLogger(__name__)

from .codes import WatsonReturnCodes

WATSON_CONFIG = watson_config_loader()

class WatsonAMInterface:
    """
    Responsible for interacting with the IBM Watson STT service and providing
    methods for interacting with acoustic models.
    """
    def __init__(self, apikey : str, region : str):

        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()
        self.connected_to_service = False
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
            raise ERR.ConnectionError("ERROR: Failed to connect to the Watson STT")
        else:
            self.connected_to_service  = True
    
    def get_custom_model(
        self,
        customization_id: str
    ) -> Union[Dict[str, Any], None]:
        """
        Obtain information regarding a specific custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (Union[Dict[str,Any],None]):
                Mapping from the following keys to their values:
                customization_id, CREATED, updated,language, dialect,
                versions, owner, name, description, base_model_name, status,
                progress
                None if unsuccessful.
        """
        _, resp = self._execute_watson_method(
            self.stt.get_acoustic_model, [WatsonReturnCodes.OK],
            [customization_id])
        return resp

    def get_custom_models(self) -> Dict[str, str]:
        """
        Obtain all custom acoustic models

        Returns:
            (Dict[str,str]):
                Mapping from custom acoustic model to the customization id.
        """
        custom_models = dict()
        response = self._execute_watson_method(
            self.stt.list_acoustic_models, [WatsonReturnCodes.OK])
        if response:
            for model in response["customizations"]:
                custom_models[model["name"]] = model["customization_id"]
        return custom_models

    def create_custom_model(
        self,
        name : str,
        base_model_name : str,
        description : str
    ) -> bool:
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
        response = self._execute_watson_method(
            self.stt.create_acoustic_model, [WatsonReturnCodes.CREATED],
            [name, base_model_name], {"description": description})
        return response

    def delete_custom_model(self, customization_id: str) -> bool:
        """
        Delete an existing custom acoustic model.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response= self._execute_watson_method(
            self.stt.delete_acoustic_model, [WatsonReturnCodes.OK],
            [customization_id])
        return response

    def train_custom_model(self, customization_id: str) -> bool:
        """
        Train a custom acoustic model with a previously added resource.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.train_acoustic_model, [WatsonReturnCodes.OK],
            [customization_id])
        return response

    def reset_custom_model(self, customization_id: str) -> bool:
        """
        Reset a custom acoustic model to remove all loaded resources.

        Args:
            customization_id (str): Unique ID of the custom acoustic model.

        Returns:
            (bool): True if successful. False otherwise.
        """
        response = self._execute_watson_method(
            self.stt.reset_acoustic_model, [WatsonReturnCodes.OK],
            [customization_id])
        return response

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
        response = self._execute_watson_method(
            self.stt.upgrade_acoustic_model,
            [customization_id, custom_language_model_id])
        return response

    
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
        response = self._execute_watson_method(
            self.stt.list_audio, [customization_id])
        if response:
            return response["audio"]

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
            response = self._execute_watson_method(
                self.stt.get_audio, [WatsonReturnCodes.OK],
                [customization_id, audio_name])
            if response:
                return response

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
            response = self._execute_watson_method(
                self.stt.add_audio, [WatsonReturnCodes.CREATED],
                [customization_id, audio_name, audio_resource, content_type])
            return response

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
        response = self._execute_watson_method(
            self.stt.delete_audio, [WatsonReturnCodes.OK],
            [customization_id, audio_name])
        return response
    
    ## PRIVATE ##
    
    def _is_api_key_valid(self, apikey: str, url: str) -> bool:
        try:
            stt = self._initialize_stt_service(apikey)
            stt.set_service_url(url)
            stt.list_models()
            return True
        except:
            return False

    def _initialize_stt_service(self, apikey: str) -> SpeechToTextV1:
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        return stt
    
    def _execute_watson_method(self, 
                               method: Callable,
                               expected_response_codes: List[WatsonReturnCodes], 
                               args: List = [],
                               kwargs: Dict = {}) -> Union[bool, Any]:
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
            raise ERR.ConnectionError
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