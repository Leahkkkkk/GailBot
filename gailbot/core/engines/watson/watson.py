# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:58:57

from typing import Dict, Any, List
from itertools import chain

from .recognition_results import RecognitionResult
from .recognize_callback import CustomWatsonCallbacks
from .core import WatsonCore
from .lm import WatsonLMInterface
from .am import WatsonAMInterface
from ..engine import Engine


# TODO: Need to give the engine direct access to the config file.
class Watson(Engine):

    ENGINE_NAME = "watson"

    def __init__(
        self,
        apikey : str,
        region : str
    ):
        self.apikey = apikey
        self.region = region
        # NOTE: Exception raised if not connected to the service.
        self.core = WatsonCore(apikey, region)
        self.lm = WatsonLMInterface(apikey ,region)
        self.am = WatsonAMInterface(apikey, region)
        self.recognize_callbacks = CustomWatsonCallbacks()

    def __str__(self):
        return self.ENGINE_NAME

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        return (
            f"Watson engine with "
            f"api_key: {self.api_key}, " \
            f"region: {self.region}"
        )


    @property
    def supported_formats(self) -> List[str]:
        return self.core.supported_formats

    @property
    def regions(self) -> Dict:
        return self.core.regions

    @property
    def defaults(self) -> Dict:
        return self.core.defaults

    def transcribe(
        self,
        audio_path : str,
        base_model : str,
        outdir : str,
        language_customization_id : str = "",
        acoustic_customization_id : str = ""
    ) -> str:
        """Use the engine to transcribe an item"""

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
            self.recognize_callbacks.get_results())
        return utterances

    def language_customization_interface(self) -> WatsonLMInterface:
        return self.lm

    def acoustic_customization_interface(self) -> WatsonAMInterface:
        return self.am

     ############################### PRIVATE METHODS ###########################

    def _prepare_utterance(self, closure: Dict[str, Any]) -> List:
        try:
            utterances = list()
            # Mapping based on (start time, end time)
            data = dict()
            # Aggregated data from recognition results
            labels = list()
            timestamps = list()
            import json
            self.io.write(
                "./data.json", json.dumps(closure["results"]["data"]), False)
            self.io.write("./results.json",
                          json.dumps(closure["results"]["data"]), False)
            self.io.write("./closure.json", json.dumps(closure), False)
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
                # utt = Utt(
                #     value["speaker"], times[0], times[1],  value["utterance"]
                # )
                utterances.append(utt)
            return utterances
        except Exception as e:
            return []