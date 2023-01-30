# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:58:57
import os 
from typing import Dict, Any, List
from itertools import chain

from .recognition_results import RecognitionResult
from .recognize_callback import CustomWatsonCallbacks
from .core import WatsonCore
from .lm import WatsonLMInterface
from .am import WatsonAMInterface
from ..engine import Engine
from gailbot.core.engines import exception as Err
from gailbot.core.utils.general import write_json
class Watson(Engine):
    """ 
    An Engine that connect to IBM Watson STT, provide function to transcribe 
    audio file with IBM Watson STT

    Inheritance:
        Engine 
    """
    ENGINE_NAME = "watson"

    def __init__(
        self,
        apikey : str,
        region : str
    ):
        """ constructor for IBM Watson STT engine 

        Args:
            apikey (str): User API key to Watson STT service. 
            region (str): User API region. Must be in supported regions.
        """
        self.apikey = apikey
        self.region = region
        # NOTE: Exception raised if not connected to the service.
        self.core = WatsonCore(apikey, region)
        self.lm = WatsonLMInterface(apikey ,region)
        self.am = WatsonAMInterface(apikey, region)
        self.recognize_callbacks = CustomWatsonCallbacks()
        
        self.is_transcribe_success = False

    def __str__(self):
        return self.ENGINE_NAME

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        return (
            f"Watson engine with "
            f"api_key: {self.apikey}, " \
            f"region: {self.region}"
        )

    @property
    def supported_formats(self) -> List[str]:
        """ 
        a list of supported format that can be transcribe with the STT engine 
        """
        return self.core.supported_formats

    @property
    def regions(self) -> Dict:
        """
        a dictionary of the supported regions and the regions url  
        """
        return self.core.regions

    @property
    def defaults(self) -> Dict:
        """
        a dictionary that contains the default settings that will be 
        applied to the IBM Watson STT engine
        """
        return self.core.defaults

    def transcribe(
        self,
        audio_path : str,
        output_directory : str,
        base_model : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> str:
        """Use the engine to transcribe an item
        
        Args: 
        audio_path: str 
            a path to the audio file that will be transcribed 
        output_directory: str 
            a path where the output file will be stored 
        base_model: str 
            a string that define the base model 
        language_customization_id: str (optional): 
            ID of the custom language model.
        acoustic_customization_id: str (optional): 
            ID of the custom acoustic model.
        """
        # try:
        utterances = self.core.transcribe(
            audio_path, output_directory, base_model,
            language_customization_id, acoustic_customization_id)
        self.is_transcribe_success = True
        return utterances
        # except:
            # raise Err.ThranscriptionError

    def language_customization_interface(self) -> WatsonLMInterface:
        """ return the watson customized language model interface """
        return self.lm

    def acoustic_customization_interface(self) -> WatsonAMInterface:
        """ return the watson customized acoustic model interface """
        return self.am
    
    def get_engine_name(self) -> str:
        """ return  the name of the watson engine"""
        return self.ENGINE_NAME 

    def get_supported_formats(self) -> List[str]:
        """ 
        return a list of supported format that can be 
        transcribe with the STT engine 
        """
        self.core.supported_formats
    
    def is_file_supported(self, file_path: str) -> bool:
        """ 
        given a file path, return true if the file format is supported by 
        the Watson STT engine 
        """
        return self.core.is_file_supported(file_path)
    
    def was_transcription_successful(self) -> bool:
        """ 
        return true if the transcription is finished and successful, 
        false otherwise 
        """
        return self.is_transcribe_success
  