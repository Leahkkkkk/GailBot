# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 21:22:35
'''
    The classes in this script model the RecognitionResult object as per
    the documentation for IBM Watson STT service:
    https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-basic-response
'''
# Standard library imports
from typing import Dict, Any, List
import itertools
# Local imports
# Third party imports


class Alternative:
    """
    Models the smallest unit of a transcription result.
    """

    def __init__(self, data: Dict) -> None:
        self.items = {
            "transcript": None,
            "confidence": None,
            "timestamps": None,
            "word_confidence": None}
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Return True if the data was successfully parsed. False otherwise.
        """
        return self.configured

    def get(self, key: str) -> Any:
        """
        Obtain the value associated with the specified key.
        None if key not found.
        """
        try:
            return self.items[key]
        except:
            pass

    def _parse_data(self, data: Dict) -> bool:
        """
        Parse the input data dictionary.

        Args:
            data (Dict)

        Returns:
            (bool): True if parsed successfully. False otherwise.
        """
        keys = ["timestamps", "word_confidence", "transcript", "confidence"]
        for key in keys:
            if key in data:
                self.items[key] = data[key]
        return all([k in data for k in keys])


class SpeakerLabel:
    """
    Models a SpeakerLabel data item returned from the IBM Watson STT service.
    """

    def __init__(self, data: Dict) -> None:
        self.items = {
            "from": None,
            "to": None,
            "speaker": None,
            "confidence": None}
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Return True if the data was successfully parsed. False otherwise.
        """
        return self.configured

    def get(self, key: str) -> Any:
        """
        Obtain the value associated with the specified key.
        None if key not found.
        """
        try:
            return self.items[key]
        except:
            pass

    def _parse_data(self, data: Dict) -> bool:
        """
        Parse the input data dictionary.

        Args:
            data (Dict)

        Returns:
            (bool): True if parsed successfully. False otherwise.
        """
        for key in self.items.keys():
            if key in data:
                self.items[key] = data[key]
        return all([k in data for k in self.items.keys()])


class Result:
    """
    Models a 'Result' object that is returned from the IBM STT service.
    """

    def __init__(self, data: Dict) -> None:
        self.items = {
            "keywords_result": list(),
            "word_alternatives": list(),
            "alternatives": list(),
            "final": None}
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Return True if the data was successfully parsed. False otherwise.
        """
        return self.configured

    def get(self, key: str) -> Any:
        """
        Obtain the value associated with the specified key.
        None if key not found.
        """
        return self.items[key]

    def _parse_data(self, data: Dict) -> bool:
        """
        Parse the input data dictionary.

        Args:
            data (Dict)

        Returns:
            (bool): True if parsed successfully. False otherwise.
        """
        results = data["results"]
        if "final" in results:
            self.items["final"] = results["final"]
        if "keywords_result" in results.keys():
            self.items["keywords_result"] = results["keywords_result"]
        if "word_alternatives" in results.keys():
            self.items["word_alternatives"] = results["word_alternatives"]
        if "alternatives" in results.keys():
            self.items["alternatives"] = \
                [Alternative(alt) for alt in results["alternatives"]]


class RecognitionResult:
    """
    Main class that models an entire RecognitionResult object that is returned
    from the IBM Watson STT service.
    """

    def __init__(self, watson_data: Dict) -> None:
        self.items = {
            "result_index": None,
            "results": None,
            "speaker_labels": None}
        self.configured = self._parse_data(watson_data)

    def is_configured(self) -> bool:
        """
        Return True if the data was successfully parsed. False otherwise.
        """
        return self.configured

    ############################### PUBLIC METHODS ###########################

    def get_result_index(self) -> int:
        """
        Obtain the index / result number as returned by the IBM STT service.

        Returns:
            (int): Result index.
        """
        return self.items["result_index"]

    def num_speaker_labels(self) -> int:
        """
        Obtain the number of SpeakerLabel objects received by the service.
        Note that this does not relate to the number of speakers detected by
        the service.

        Returns:
            (int): Number of SpeakerLabel objects received.
        """
        return len(self.items["speaker_labels"])

    def num_results(self) -> int:
        """
        Obtain the number of individual results obtained by the IBM STT service.
        """
        return len(self.items["results"])

    def get_speaker_labels(self) -> List[Dict[str, str]]:
        """
        Obtain a list of dictionaries that model SpeakerLabel objects.

        Returns:
            (List[Dict[str,str]]):
                List of dictionaries modeling SpeakerLabel objects.
                Each dictionary has the keys: 'from', 'to', 'speaker',
                'confidence'.
        """
        labels = list()
        for label in self.items["speaker_labels"]:
            labels.append({
                "start_time": label.get("from"),
                "end_time": label.get("to"),
                "speaker": label.get("speaker"),
                "label_confidence": label.get("confidence")})
        return labels

    def get_keywords_results(self, only_final: bool = True) -> List[Any]:
        """
        Obtain a list of 'keyword_result' objects received from the IBM
        STT service.

        Args:
            only_final (bool):
                True to obtain 'keyword_result' only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[Any]): List of 'keyword_result' objects.
        """
        return self._aggregate(
            self.items["results"], "keywords_result", only_final)

    def get_word_alternatives(self, only_final: bool = True) -> Any:
        """
        Obtain a list of 'word_alternative' objects received from the IBM
        STT service.

        Args:
            only_final (bool):
                True to obtain 'word_alternative' only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[Any]): List of 'word_alternative' objects.
        """
        return self._aggregate(
            self.items["results"], "word_alternatives", only_final)

    def get_transcript_from_alternatives(self, only_final: bool = True) \
            -> List[str]:
        """
        Obtain a list containing all 'transcript' items from all Alternative
        received as part of the IBM STT result.

        Args:
            only_final (bool):
                True to obtain items only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[str]):
                List of 'transcript' items for all Alternative objects.
        """
        alternatives = self._aggregate(
            self.items["results"], "alternatives", only_final)[0]
        return [alternative.get("transcript") for alternative in alternatives]

    def get_transcript_confidences_from_alternatives(self,
                                                     only_final: bool = True) -> List[float]:
        """
        Obtain a list containing all 'transcript_confidence' objects from all
        Alternative received as part of the IBM STT result.

        Args:
            only_final (bool):
                True to obtain items only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[float]):
                List contianing confidence for each transcript obtained.
        """
        alternatives = self._aggregate(
            self.items["results"], "alternatives", only_final)[0]

        return [alternative.get("confidence") for alternative in alternatives]

    def get_timestamps_from_alternatives(self, only_final: bool = True) \
            -> List[List[List[Any]]]:
        """
        Obtain a list containing all 'timestamps' objects from all
        Alternative received as part of the IBM STT result.

        Args:
            only_final (bool):
                True to obtain items only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[List[List[Any]]]):
                One main list continaing lists, with each inner most list
                representing one result of the form:
                ['text', 'start time', 'end time']
        """
        alternatives = self._aggregate(
            self.items["results"], "alternatives", only_final)
        alternatives = list(itertools.chain(*alternatives))
        timestamps = [alternative.get("timestamps")
                      for alternative in alternatives]
        return [timestamp for timestamp in timestamps if timestamp != None]

    def get_word_confidences_from_alternatives(self, only_final: bool = True) \
            -> List:
        """
        Obtain a list containing all 'word_confidence' objects from all
        Alternative received as part of the IBM STT result.

        Args:
            only_final (bool):
                True to obtain items only from results that are
                considered final and not interim. False to include all results,
                both final and interim.

        Returns:
            (List[List[List[Any]]]):
                One main list continaing lists, with each inner most list
                representing one result of the form:
                ['text', 'confidence']
        """
        alternatives = self._aggregate(
            self.items["results"], "alternatives", only_final)[0]
        return [alternative.get("word_confidence")
                for alternative in alternatives]

    ############################### PRIVATE METHODS ##########################

    def _parse_data(self, watson_data: Dict) -> bool:
        """
        Parse a single RecognitionResult dictionary obtained from the IBM
        STT service.

        Args:
            (Dict): Dictionary representing a RecognitionResult

        Returns:
            (bool): True if p[arsed successfully. False otherwise.
        """
        # Level 1
        try:
            if "result_index" in watson_data.keys():
                self.items["result_index"] = watson_data["result_index"]
            if "speaker_labels" in watson_data.keys():
                labels = list()
                for label in watson_data["speaker_labels"]:
                    labels.append(SpeakerLabel(label))
                self.items["speaker_labels"] = labels
            # Level 2 (In results)
            if "results" in watson_data.keys():
                results_array = list()
                for results in watson_data["results"]:
                    results_array.append(Result({"results": results}))
                self.items["results"] = results_array
            return True
        except Exception as e:
            print("parsing excepion", e)

    def _aggregate(self, results: List[Result], aggregation_key: str,
                   only_final: bool) -> List[Any]:
        """
        Aggregate the results from a list of Result objects, based on the
        aggregation key. If only_final = True, only use the results of
        Result objects considered final.
        """
        response = list()
        for item in results:
            if only_final:
                if item.get("final"):
                    response.append(item.get(aggregation_key))
            else:
                response.append(item.get(aggregation_key))
        return response
