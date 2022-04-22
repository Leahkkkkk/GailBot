# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:58:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-22 12:48:08
# Standard library imports
from typing import List, Any, Dict
import time
# Local imports
from ...io import IO
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource


class WatsonCore:
    """
    Responsible for knowing how to interact with the IBM Watson STT service
    to perform transcription through a websocket connection for a
    single audio source.
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

    # Mappings from audio format to the watson content types for that format.
    format_to_content_types = {
        # "alaw" : "audio/alaw",
        # "basic" : "audio/basic",
        "flac": "audio/flac",
        "ogg": "audio/ogg",
        # "l16" : "audio/l16",
        "mp3": "audio/mp3",
        "mpeg": "audio/mpeg",
        # "mulaw" : "audio/mulaw",
        "wav": "audio/wav",
        "webm": "audio/webm",
        "ogg": "audio/ogg;codecs=opus",
        "opus": "audio/ogg;codecs=opus"}

    def __init__(self, io: IO) -> None:
        """
        Args:
            network (Network): Instantiated network object.
            io (IO): Instantiated IO object.
        """
        # Vars.
        self.max_file_size_bytes = 7e7
        # Default parameters for watson
        self.watson_defaults = {
            "ssl_verification": True,
            "headers": {
                "x-watson-learning-opt-out": True},
            "customization_weight": 0.3,
            "base_model_version": None,
            "inactivity_timeout": 1000,
            "interim_results": False,
            "keywords": None,
            "keyword_threshold": 0.8,
            "max_alternatives": 1,
            "word_alternatives_threshold": None,
            "word_confidence": True,
            "timestamps": False,
            "profanity_filter": False,
            "smart_formatting": False,
            "speaker_labels": True,
            "http_proxy_host": None,
            "http_proxy_port": None,
            "grammar_name": None,
            "redaction": False,
            "processing_metrics": False,
            "processing_metrics_interval": 1.0,
            "audio_metrics": False,
            "end_of_phrase_silence_time": 0.8,
            "split_transcript_at_phrase_end": False,
            "speech_detector_sensitivity": 0.5,
            "background_audio_supression": 0.0}
        # User inputs.
        self.inputs = {
            "api_key": None,
            "region": None,
            "audio_path": None,
            "recognize_callback": None,
            "base_model_name": None,
            "language_customization_id": None,
            "acoustic_customization_id": None,
            "workspace_directory_path": None}
        # Objects
        self.io = io

    # SETTERS

    def set_api_key(self, api_key: str) -> bool:
        """
        Set the api key for the STT service.

        Args:
            apikey (str): Valid API key for the watson STT service.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        # success = self._is_api_key_valid(api_key)
        # if not success:
        #     return False
        self.inputs["api_key"] = api_key
        return True

    def set_service_region(self, region: str) -> bool:
        """
        Set the region associated with the api key for the STT service.

        Args:
            region (str):
                Region for the STT service. Must be a supported regions.
        """
        region = region.lower()
        if not region in self.regions.keys():
            return False
        self.inputs["region"] = region
        return True

    def set_recognize_callback(self, recognize_callback: RecognizeCallback)\
            -> bool:
        """
        Initialized object that handles callbacks during the websocket lifecycle.
        Inherits from and implements ibm_watson.websocket.RecognizeCallback.

        Args:
            recognize_callback (RecognizeCallback)

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.inputs["recognize_callback"] = recognize_callback
        return True

    def set_audio_source_path(self, audio_source_path: str) -> bool:
        """
        Set the path to the audio file that is to be transcribed. This
        audio file format MUST be supported and the path MUST be a valid path.

        Args:
            audio_source_path (str): Validated path to the audio file.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        if not self.io.is_file(audio_source_path) and \
                not self._is_supported_audio_file(audio_source_path):
            return False
        self.inputs["audio_path"] = audio_source_path
        return True

    def set_base_language_model(self, base_model_name: str) -> bool:
        """
        Set the base language model to use for transcription.
        MUST be a supported model name.

        Args:
            base_model_name (str): Name of the base audio model.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.inputs["base_model_name"] = base_model_name
        return True

    def set_language_customization_id(self, customization_id: str) -> bool:
        """
        Set the language customization id for a custom language model.
        The base model should be the same as the base model used for the
        custom ID.
        The ID should be validated beforehand.

        Args:
            customization_id (str): ID of the custom language model to use.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.inputs["language_customization_id"] = customization_id
        return True

    def set_acoustic_customization_id(self, customization_id: str) -> bool:
        """
        Set the acoustic customization id for a custom acoustic model.
        The ID should be validated beforehand.

        Args:
            customization_id (str): ID of the custom acoustic model to use.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.inputs["acoustic_customization_id"] = customization_id
        return True

    def set_workspace_directory_path(self, workspace_dir_path: str) -> bool:
        if not self.io.is_directory(workspace_dir_path):
            return False
        self.engine_workspace_dir = "{}/watson_engine_ws".format(
            workspace_dir_path)
        self.inputs["workspace_directory_path"] = self.engine_workspace_dir
        return True

    # GETTERS

    def get_api_key(self) -> str:
        """
        Obtain the API key.

        Returns:
            (str): Api key is it has been set. None otherwise.
        """
        return self.inputs["api_key"]

    def get_service_region(self) -> str:
        """
        Obtain the region associated with the api key

        Returns:
            (str): Region if it has been set. None otherwise.
        """
        return self.inputs["region"]

    def get_audio_source_path(self) -> str:
        """
        Obtain the path to the audio source.

        Returns:
            (str): Path if it has been set. None otherwise.
        """
        return self.inputs["audio_path"]

    def get_selected_base_model(self) -> str:
        """
        Obtain the name of the base model being used for transcription.

        Returns:
            (str): Base model name if set. None otherwise.
        """
        return self.inputs["base_model_name"]

    def get_language_customization_id(self) -> str:
        """
        Obtain the ID of the custom language model being used.

        Returns:
            (str): Custom model ID if it has been set. None otherwise.
        """
        return self.inputs["language_customization_id"]

    def get_acoustic_customization_id(self) -> str:
        """
        Obtain the ID of the custom acoustic model being used.

        Returns:
            (str): Custom model ID if it has been set. None otherwise.
        """
        return self.inputs["acoustic_customization_id"]

    def get_supported_regions(self) -> List[str]:
        """
        Obtain a list of the transcription regions available in the service.

        Returns:
            (List[str]): List of regions.
        """
        return list(self.regions.keys())

    def get_supported_audio_formats(self) -> List[str]:
        """
        Get the audio formats that are supported by the transcription service.

        Returns:
            (str): Supported audio formats.
        """
        return list(self.format_to_content_types.keys())

    def get_workspace_directory_path(self) -> str:
        return self.inputs["workspace_directory_path"]

    # Others

    def reset_configurations(self) -> bool:
        """
        Reset all the configurations/inputs.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        for k in self.inputs.keys():
            self.inputs[k] = None
        return True

    # TODO:Needs to work for session timeout errors and large files.
    def recognize_using_websockets(self) -> bool:
        """
        Transcribes the provided audio stream using a websocket connections.
        All attributes MUST be set before using this method.

        Returns:
            (bool): True if successfully transcribed. False otherwise.
        """
        if not self._is_ready_to_connect():
            return False
        # Create ws dir
        self.io.create_directory(self.engine_workspace_dir)
        audio_path = self.inputs["audio_path"]
        workspace_dir_path = self.inputs["workspace_directory_path"]
        # If the audio file is larger than the max supported size, it needs to
        # convert to opus
        try:
            # TODO: Eventually add chunking logic instead of opus
            # TODO: Does not work yet
            size_bytes = self.io.get_size(audio_path)
            if size_bytes >= self.max_file_size_bytes:
                # Convert to opus and run
                out_path = "{}/{}.opus".format(
                    workspace_dir_path, self.io.get_name(audio_path)
                )
                _, identifier = self.io.run_shell_command(
                    "ffmpeg -y -i {} -strict -2  {}".format(
                        audio_path, out_path), None, None)
                while True:
                    if self.io.get_shell_process_status(identifier) == "finished":
                        break
                    if self.io.get_shell_process_status(identifier) == "error":
                        break
                    if self.io.get_shell_process_status(identifier) == "":
                        break
                audio_path = out_path
            # Creating STT object.
            # NOTE: This should be done right at the end to prevent a
            # session timeout.
            stt = self._initialize_stt_service(self.inputs["api_key"])
            stt.set_service_url(self.regions[self.inputs["region"]])
            with open(audio_path, "rb") as audio_file:
                stt.recognize_using_websocket(
                    **self._prepare_websocket_args(audio_path, audio_file))
            # Remove the workspace directory
            self.io.delete(self.engine_workspace_dir)
            return True
        except Exception as e:
            print(e)
            return False

    ############################ PRIVATE METHODS ###########################

    def _determine_content_type(self, file_path: str) -> str:
        """
        Given the path to an audio file, determines the watson content type.

        Args:
            file_path (str): Path to the audio file.

        Returns:
            (str): Watson content type for that file.
        """
        extension = self.io.get_file_extension(file_path)
        if extension in self.format_to_content_types.keys():
            return self.format_to_content_types[extension]

    def _is_supported_audio_file(self, file_path: str) -> bool:
        """
        Determine if the audio file at the given path is supported.

        Args:
            file_path (str): Path to the audio file.

        Returns:
            (bool): True if the file is supported. False otherwise.
        """
        _, extension = self.io.get_file_extension(file_path)
        return extension in self.format_to_content_types.keys()

    def _is_ready_to_connect(self) -> bool:
        """
        Determine if all the parameters required to send a request to the
        service have been set.

        Returns:
            (bool): True if ready to connect to service. False otherwise.
        """
        return self.inputs["api_key"] != None and \
            self.inputs["audio_path"] != None and \
            self.inputs["recognize_callback"] != None and \
            self.inputs["region"] != None

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

    def _prepare_websocket_args(self, audio_path, audio_file: Any) \
            -> Dict[str, Any]:
        """
        Prepare the final parameter dictionary for
        SpeechToTextV1.recognize_using_websocket.

        Args:
            audio_file (Any): Opened file stream for the audio file to be sent.

        Returns:
            (Dict[str,Any]): Mapping from watson parameter to its value.
        """
        source = AudioSource(audio_file)
        return {
            "audio": source,
            "content_type": self._determine_content_type(
                audio_path),
            "recognize_callback": self.inputs["recognize_callback"],
            "model": self.inputs["base_model_name"],
            "language_customization_id": self.inputs["language_customization_id"],
            "acoustic_customization_id": self.inputs["acoustic_customization_id"],
            "customization_weight":
            self.watson_defaults["customization_weight"] if
            self.inputs["language_customization_id"] else None,
            "base_model_version": None,
            "inactivity_timeout": self.watson_defaults["inactivity_timeout"],
            "interim_results": self.watson_defaults["interim_results"],
            "keywords": self.watson_defaults["keywords"],
            "keywords_threshold": self.watson_defaults["keyword_threshold"] if
            self.watson_defaults["keywords"] else None,
            "max_alternatives": self.watson_defaults["max_alternatives"],
            "word_alternatives_threshold":
            self.watson_defaults["word_alternatives_threshold"],
            "word_confidence": self.watson_defaults["word_confidence"],
            "timestamps": self.watson_defaults["timestamps"],
            "profanity_filter": self.watson_defaults["profanity_filter"],
            "smart_formatting": self.watson_defaults["smart_formatting"],
            "speaker_labels": self.watson_defaults["speaker_labels"],
            "http_proxy_host": self.watson_defaults["http_proxy_host"],
            "http_proxy_port": self.watson_defaults["http_proxy_port"],
            "grammar_name": self.watson_defaults["grammar_name"],
            "redaction": self.watson_defaults["redaction"],
            "processing_metrics": self.watson_defaults["processing_metrics"],
            "processing_metrics_interval": None,
            "audio_metrics": self.watson_defaults["audio_metrics"],
            "end_of_phrase_silence_time":
            self.watson_defaults["end_of_phrase_silence_time"],
            "split_transcript_at_phrase_end":
            self.watson_defaults["split_transcript_at_phrase_end"],
            "speech_detector_sensitivity":
            self.watson_defaults["speech_detector_sensitivity"],
            "background_audio_suppression":
            self.watson_defaults["background_audio_supression"]}
