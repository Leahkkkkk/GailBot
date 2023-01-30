# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:25:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:59:32
import os 
from typing import List, Any, Dict
from itertools import chain

import time
from copy import deepcopy
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource
from .recognize_callback import CustomWatsonCallbacks
from .recognition_results import RecognitionResult
from gailbot.core.engines import exception as Err
from gailbot.configs.utils import WATSON_DATA
from gailbot.core.utils.media import MediaHandler
from gailbot.core.utils.general import (
    make_dir,
    is_directory,
    get_extension,
    get_name,
    is_file,
    get_size,
    run_cmd, 
    get_cmd_status,
    delete,
    write_json,
    CMD_STATUS
)
WORK_SPACE = "watson_workspace"
class WatsonCore:
    """
    Implement core functionalities to transcribe an audio file through 
    watson STT engine
    """
    def __init__(self, apikey : str, region : str):
        self.apikey = apikey
        self.region = region
        self.media_h = MediaHandler()

        # Parse confs
        self._regions = WATSON_DATA.regions_uris
        self._format_to_content_types = WATSON_DATA.format_to_content 
        self._defaults = WATSON_DATA.defaults
        self.max_size_bytes = WATSON_DATA.max_file_size_bytes

        if not self._is_api_key_valid(apikey, self._regions[region]):
            raise Exception(f"Apikey {apikey} invalid")
        if not region in self._regions:
            raise Exception(
                f"Region {region} not in {list(self._regions.keys())}"
            )
        # create recognize callback 
        self.recognize_callbacks = CustomWatsonCallbacks()
        
    @property
    def supported_formats(self) -> List[str]:
        """
        Access the supported formats of an instance of object WatsonCore

        Returns:
            List[str] : list of supported formats
        """
        return self.media_h.supported_formats

    @property
    def regions(self) -> Dict:
        """
        Access the regions of an instance of object WatsonCore

        Returns: 
            Dict representing the regions
        """
        return self._regions

    @property
    def defaults(self) -> Dict:
        """
        Access the defaults of an instance of object WatsonCore

        Returns: 
            Dict representing the defaults
        """
        return self._defaults

    def is_file_supported(self, file:str) -> bool:
        """
        Determines if a given file is supported

        Args:
            file (str) : file name to check if supported

        Returns: True if the file is supported, false if not.
        """
        return get_extension(file) in self.supported_formats
    
    def transcribe(self, 
                  audio_path: str, 
                  output_directory: str, 
                  base_model: str, 
                  language_customization_id: str, 
                  acoustic_customization_id: str):
        """
        Transcribes the provided audio stream using a websocket connections.
        And output the result to given output directory 

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            output_directory (str) : 
                path to directory where the transcribed data will be stored
            base_language_model (str) : 
                specifies the base_language_model 
            language_customization_id (str) : 
                ID of the custom acoustic model
            acoustic_customization_id (str) : 
                ID of the custom language model.
        """
        try:
            self._websockets_recognize(
                audio_path, output_directory, base_model, 
                language_customization_id, acoustic_customization_id)  
        except:
           Err.ConnectionError
           
        utterances = self._prepare_utterance(
            output_directory, self.recognize_callbacks.get_results())   
        return utterances   
    
###############
# PRIVATE
##############
    def _websockets_recognize(
        self,
        audio_path : str,
        output_directory : str,
        base_model : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> Any:
        """
        Transcribes the provided audio stream using a websocket connections.
        All attributes MUST be set before using this method.

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            output_directory (str) : 
                path to directory where the transcribed data will be stored
            base_language_model (str) : 
                specifies the base_language_model 
            language_customization_id (str) : 
                ID of the custom acoustic model
            acoustic_customization_id (str) : 
                ID of the custom language model.
        """
        # reset the callbacks
        self.recognize_callbacks.reset()
        # Checks all the input data is valid
        assert is_file(audio_path), f"Not a file {audio_path}"
        work_space_directory = os.path.join(output_directory, WORK_SPACE)
        try: 
            if not is_directory(output_directory): 
                make_dir(output_directory, overwrite=True)
            make_dir(work_space_directory, overwrite=True)
            assert is_directory(output_directory)
            self.engine_workspace_dir = work_space_directory
        except:
            raise FileExistsError 
        
        try:
            if get_size(audio_path) >= self.max_size_bytes:
                audio_path = self._convert_to_opus(audio_path, work_space_directory)
        except: 
            raise Err.AudioFileError

        # Create the stt service and run
        try:
            authenticator = IAMAuthenticator(self.apikey)
            stt = SpeechToTextV1(authenticator=authenticator)
            stt.set_service_url(self.regions[self.region])
        except:
            raise Err.APIKeyError

        with open(audio_path, "rb") as f:
            # Prepare args
            source = AudioSource(f)
            content_type = self._format_to_content_types[get_extension(audio_path)]
            """ TODO:  no acoustic_customization id """
            # kwargs = deepcopy(self.defaults)
            kwargs = {
            "ssl_verification": True,
            # "headers": {
            #     "x-watson-learning-opt-out": False},
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
            "background_audio_suppression": 0.0}
            
            kwargs.update({
                "audio": source,
                "content_type" : content_type,
                "recognize_callback": self.recognize_callbacks,
                "model" : base_model,
                "customization_id": language_customization_id,
            })
            
            print(kwargs)
            stt.recognize_using_websocket(**kwargs)
            delete(self.engine_workspace_dir)
            
    def _prepare_utterance(self, output_directory, closure: Dict[str, Any]) -> List:
        try:
            utterances = list()
            # Mapping based on (start time, end time)
            data = dict()
            # Aggregated data from recognition results
            labels = list()
            timestamps = list()
            
            write_json(os.path.join(output_directory, "data.json"), 
                        closure["results"]["data"])
            write_json(os.path.join(output_directory, "results.json"),
                        closure["results"]["data"])
            write_json(os.path.join(output_directory, "closure.json"), closure)
            # Creating RecognitionResults objects
            for item in closure["results"]["data"]:
                recognition_result = RecognitionResult(item)
                if recognition_result.is_configured():
                    labels.extend(recognition_result.get_speaker_labels())
                    timestamps.extend(
                        recognition_result.get_timestamps_from_alternatives(
                            only_final=False))
            timestamps = list(chain(*timestamps))
            # Creating the mappings
            for label in labels:  # Label should be a dictionary
                key = (label["start_time"], label["end_time"])
                if not key in data:
                    data[key] = {"speaker": label["speaker"]}
                else:
                    data[key]["speaker"] = label["speaker"]
            for timestamp in timestamps:
                key = (timestamp[1], timestamp[2])
                if key not in data:
                    data[key] = {"utterance": timestamp[0]}
                else:
                    data[key]["utterance"] = timestamp[0]
            # Creating utterances
            for times, value in data.items():
                utt = {
                    "speaker" : value["speaker"],
                    "start_time" : times[0],
                    "end_time" : times[1],
                    "text" : value["utterance"]
                }
                utterances.append(utt)
            return utterances
        except Exception as e:
            return []
            
    def _is_api_key_valid(self, apikey: str, url: str) -> bool:
        """
        Determines if given Watson API key is valid

        Args:
            apikey (str) : apikey of which to determine validity
            url (str) : URL to set service url of speech to text service
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
        Initializes the speech to text services

        Args:
            apikey (str) : API key to pass into the IAMAuthenticator

        Returns:
            Newly initialized speech to text service
        """
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        return stt

    def _convert_to_opus(self, audio_path: str, workspace: str) -> str:
        """
        Convert audio stream to .opus format 

        Args:
            audio_path (str) : path to the audio file for which to convert 
                to .opus format
            workspace (str) : Workspace of the output directory in which to put 
                the newly converted file

        Returns:
            String representing the path to the newly converted output file
        """
        out_path = "{}/{}.opus".format(workspace, get_name(audio_path))
        cmd_str = "ffmpeg -y -i {} -strict -2  {}".format(audio_path, out_path)
        pid = run_cmd(["ffmpeg", "-y", "-i", audio_path, "-strict", "-2", out_path])
        
        while True:
            match get_cmd_status(pid):
                case CMD_STATUS.STOPPED:
                    raise ChildProcessError
                case CMD_STATUS.FINISHED:
                    break 
                case CMD_STATUS.ERROR:
                    raise ChildProcessError
                case CMD_STATUS.NOTFOUND:
                    raise ProcessLookupError
        
        return get_cmd_status(pid) == CMD_STATUS.FINISHED
    
