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
        base_model : str,
        outdir : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> str:
        """Use the engine to transcribe an item
        
        Args: 
        audio_path: str 
            a path to the audio file that will be transcribed 
        base_model: str 
            a string that define the base model 
        outdir: str 
            a path where the output file will be stored 
        language_customization_id: str (optional): 
            ID of the custom language model.
        acoustic_customization_id: str (optional): 
            ID of the custom acoustic model.
        """
        try:
            self.recognize_callbacks.reset()
            self.core.websockets_recognize(
                audio_path,
                outdir,
                self.recognize_callbacks,
                base_model,
                language_customization_id,
                acoustic_customization_id
            )
            utterances = self._prepare_utterance(
                outdir, 
                self.recognize_callbacks.get_results())
            self.is_transcribe_success = True
            return utterances
        except:
            self.is_transcribe_success = False

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
        self.core.is_file_supported(file_path)
    
    def was_transcription_successful(self) -> bool:
        """ 
        return true if the transcription is finished and successful, 
        false otherwise 
        """
        return self.is_transcribe_success
     ############################### PRIVATE METHODS ###########################
    """ TODO: check output directory """
    def _prepare_utterance(self, outdir: str, closure: Dict[str, Any]) -> List:
        """ 
        Args:
            outdir: str 
                the output directory 
            closure (Dict[str, Any]): 


        Returns:
            List: a list of dictionary that stores a stream of utterance data 
                  in "speaker: , start time:  , end time:  , text:  ," format  
        """
        try:
            utterances = list()
            # Mapping based on (start time, end time)
            data = dict()
            # Aggregated data from recognition results
            labels = list()
            timestamps = list()
            """ TODO: check the parent file path for the json file output  """     
            write_json(os.path.join(outdir, "data.json"), 
                        closure["results"]["data"])
            write_json(os.path.join(outdir, "results.json"),
                        closure["results"]["data"])
            write_json(os.path.join(outdir, "closure.json"), closure)
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
    
