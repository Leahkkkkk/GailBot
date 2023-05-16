# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:25:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:59:32

""" TODO:
1. keyword arguments : headers, customization weight are removed 
"""
import os 
from typing import List, Any, Dict, Union
from itertools import chain
from copy import deepcopy
# Third party imports
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource
from .recognize_callback import CustomWatsonCallbacks
from .recognition_results import RecognitionResult
from gailbot.core.utils.logger import makelogger
from gailbot.core.engines import exception as EXCEPTION
from gailbot.configs import watson_config_loader
from gailbot.core.utils.media import MediaHandler
from gailbot.core.utils.general import (
    get_extension,
    get_name,
    is_file,
    get_size,
    run_cmd, 
    get_cmd_status,
    CMD_STATUS
)

WATSON_CONFIG = watson_config_loader()
logger = makelogger("watson_core")
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
        self._format_to_content_types = WATSON_CONFIG.format_to_content 
        self._defaults = WATSON_CONFIG.defaults
        
        if not WatsonCore.valid_region_api(apikey, region):
            raise ApiException("invalid apikey and region")
       
    
    @staticmethod 
    def valid_region_api(apikey, region):
        """check if an api key is a valid api key under the region

        Args:
            apikey (str): a string that stores the api key
            region (str): the region 

        Returns:
            bool: true if the api key is valid, false otherwise
        """
        if not region in WATSON_CONFIG.regions_uris:
            logger.error("Region invalid")
            return False
        if not WatsonCore.is_api_valid(apikey, WATSON_CONFIG.regions_uris[region]):
            logger.error("API invalid")
            return False
        return True
          
    @property
    def supported_formats(self) -> List[str]:
        """
        Access the supported formats of an instance of object WatsonCore

        Returns:
            List[str] : list of supported formats
        """
        return ["wav"]

    @property
    def regions(self) -> Dict:
        """
        Access the regions of an instance of object WatsonCore

        Returns: 
            Dict representing the regions
        """
        return WATSON_CONFIG.regions_uris

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
    
    def transcribe( self, 
                    audio_path: str,
                    payload_workspace: str,  
                    base_model: str, 
                    language_customization_id: str, 
                    acoustic_customization_id: str):
        """
        Transcribes the provided audio stream using a websocket connections.
        And output the result to given output directory 

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            base_language_model (str) : 
                specifies the base_language_model 
            language_customization_id (str) : 
                ID of the custom acoustic model
            acoustic_customization_id (str) : 
                ID of the custom language model.
        """
        # compress the audio if it is too bog
        path_copy = audio_path
        logger.info("transcribe the audio file with watson STT")
        try:
            new_path = os.path.join(payload_workspace, os.path.basename(audio_path))
            audio_path = MediaHandler.convert_to_16bit_wav(audio_path, new_path)
        except Exception as e:
            logger.error(e, exc_info=e)
            audio_path = path_copy
        try:
            if get_size(audio_path) >= WATSON_CONFIG.max_file_size_bytes:
                audio_path = self._convert_to_opus(audio_path, payload_workspace)
                logger.info(f"the compressed auido_path is {audio_path}")
        except Exception as e: 
            logger.error("error in compressing the media file", exc_info=e)
            raise EXCEPTION.AudioFileError(EXCEPTION.ERROR.AUDIO_COMPRESSION_FAILED)
        
        recognize_callbacks = CustomWatsonCallbacks()
        try:
            self._websockets_recognize(
                audio_path,
                base_model, 
                recognize_callbacks,
                language_customization_id, 
                acoustic_customization_id)  
        except Exception as e:
            logger.error(e, exc_info=e)
            raise EXCEPTION.ConnectionError(EXCEPTION.ERROR.CONNECTION_ERROR)
        
        try:
            audio_name = get_name(audio_path)
            utterances = self._prepare_utterance(
                audio_name,
                recognize_callbacks.get_results())   
            return utterances   
        except Exception as e: 
            logger.error(e, exc_info=e)
            raise EXCEPTION.GetUttResultError()
    
###############
# PRIVATE
##############
    def _websockets_recognize(
        self,
        audio_path : str,
        base_model : str,
        recognize_callbacks: CustomWatsonCallbacks,
        language_customization_id : str = None,
        acoustic_customization_id : str = None
    ) -> Any:
        """
        Transcribes the provided audio stream using a websocket connections.
        All attributes MUST be set before using this method.

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            base_language_model (str) : 
                specifies the base_language_model 
            language_customization_id (str) : 
                ID of the custom acoustic model
            acoustic_customization_id (str) : 
                ID of the custom language model.
        """
        # reset the callbacks
        logger.info("sending audio file to watson")
        recognize_callbacks.reset()
        assert is_file(audio_path), f"Not a file {audio_path}"
    
        # Create the stt service and run
        try:
            authenticator = IAMAuthenticator(self.apikey)
            stt = SpeechToTextV1(authenticator=authenticator)
            stt.set_service_url(self.regions[self.region])
        except:
            raise EXCEPTION.APIKeyError()
        with open(audio_path, "rb") as f:
            # Prepare args
            source = AudioSource(f)
            content_type = self._format_to_content_types[get_extension(audio_path)]
            """ 
            :  confirm current set of key word arguments is okay, 
                       headers and customized weight does not work  """
            kwargs = deepcopy(self.defaults)
            kwargs.update({
                "inactivity_timeout": -1,
                "audio": source,
                "content_type" : content_type,
                "recognize_callback": recognize_callbacks,
                "model" : base_model,
                "customization_id": language_customization_id,
            })
            logger.info(kwargs)
            stt.recognize_using_websocket(**kwargs)
            
    def _prepare_utterance(self, audio_name: str,  closure: Dict[str, Any]) -> List:
        """ 
         output the response data from google STT, convert the raw data to 
        utterance data which is a list of dictionary in the format 
        {speaker: , start: , end: , text: }
        

        Args:
            closure (Dict[str, Any]): contains the result data from Watson

        Returns:
            List:  a list of dictionary that contains the output data
        """
        logger.info(f"prepare utterance for audio {audio_name}")
        utterances = list()
        # Mapping based on (start time, end time)
        data = dict()
        # Aggregated data from recognition results
        labels = list()
        timestamps = list()
        
        # from callback, check that the transcription is successful
        assert not closure["callback_status"]["on_error"]
    
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
                "start" : times[0],
                "end" : times[1],
                "text" : value["utterance"]
            }
            utterances.append(utt)
        return utterances
    
  
    @staticmethod
    def is_api_valid(apikey: str, url: str) -> bool:
        """
        Determines if given Watson API key is valid

        Args:
            apikey (str) : apikey of which to determine validity
            url (str) : URL to set service url of speech to text service
        """
        try:
            stt = WatsonCore._initialize_stt_service(apikey)
            stt.set_service_url(url)
            stt.list_models()
            return True
        except:
            return False

    @staticmethod
    def _initialize_stt_service(apikey: str) -> SpeechToTextV1:
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

    def _convert_to_opus(self, audio_path: str, workspace: str) -> Union[str, bool]:
        """
        Convert audio stream to .opus format 

        Args:
            audio_path (str) : path to the audio file for which to convert 
                to .opus format
            workspace (str) : Workspace of the output directory in which to put 
                the newly converted file

        Returns:
            String representing the path to the newly converted output file 
            if the file is compressed successfully, else return false 
        """
        logger.info("Converting file")
        out_path = "{}/{}.opus".format(workspace, get_name(audio_path))
        logger.info(f"Converting path{out_path}")
        pid = run_cmd(["ffmpeg", "-y", "-i", audio_path, "-strict", "-2", out_path])
        
        while True:
            match get_cmd_status(pid):
                case CMD_STATUS.STOPPED:
                    raise ChildProcessError(EXCEPTION.ERROR.CHILD_PROCESS_NOT_FOUND)
                case CMD_STATUS.FINISHED:
                    break 
                case CMD_STATUS.ERROR:
                    raise ChildProcessError(EXCEPTION.ERROR.CHILD_PROCESS_ERROR)
                case CMD_STATUS.NOTFOUND:
                    raise ProcessLookupError(EXCEPTION.ERROR.CHILD_PROCESS_NOT_FOUND)
        
        if get_cmd_status(pid) == CMD_STATUS.FINISHED:
            return out_path
        else: 
            return False
    
