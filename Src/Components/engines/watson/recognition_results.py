# Standard library imports
from typing import Dict, Any, List
# Local imports 
# Third party imports 

class Alternative:

    def __init__(self, data : Dict) -> None:
        self.items = {
            "transcript" : None,
            "confidence" : None,
            "timestamps" : None,
            "word_confidence" : None}
        self.configured =  self._parse_data(data)

    def is_configured(self) -> bool:
        return self.configured 

    def get(self, key : str) -> Any:
        return self.items[key]

    def _parse_data(self, data : Dict) -> bool:
        keys = ["timestamps","word_confidence","transcript","confidence"]
        for key in keys:
            if key in data:
                self.items[key] = data[key]
        return all([k in data for k in keys])

class SpeakerLabel:

    def __init__(self, data : Dict) -> None:
        self.items = {
            "from" : None,
            "to" : None,
            "speaker" : None,
            "confidence" : None}
        self.configured =  self._parse_data(data)

    def is_configured(self) -> bool:
        return self.configured 

    def get(self, key : str) -> Any:
        return self.items[key]

    def _parse_data(self, data : Dict) -> bool:
        for key in self.items.keys():
            if key in data:
                self.items[key] = data[key]
        return all([k in data for k in self.items.keys()])

class Result:

    def __init__(self, data : Dict) -> None:
        self.items = {
            "keywords_result" : list(),
            "word_alternatives" : list(),
            "alternatives" : list() ,
            "final" : None}
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        return self.configured

    def get(self, key : str) -> Any:
        return self.items[key]

    def _parse_data(self, data : Dict) -> bool:
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
    
    def __init__(self, watson_data : Dict) -> None:
        self.items = {
            "result_index" : None,
            "results" : None,
            "speaker_labels" : None}
        self.configured = self._parse_data(watson_data)

    def is_configured(self) -> bool:
        return self.configured 

    ############################### PUBLIC METHODS ###########################

    def get_result_index(self) -> int:
        return self.items["result_index"] 

    def num_speaker_labels(self) -> int:
        return len(self.items["speaker_labels"]) 

    def num_results(self) -> int:
        return len(self.items["results"]) 

    def get_speaker_labels(self) -> List[Dict[str,str]]:
        labels = list()
        for label in self.items["speaker_labels"]:
            labels.append({
                "start_time" : label.get("from"),
                "end_time" : label.get("to"),
                "speaker" : label.get("speaker"),
                "label_confidence" : label.get("confidence")})
        return labels

    def get_keywords_results(self, only_final : bool = True) -> List:
        return self._aggregate(
            self.items["results"],"keywords_result",only_final)

    def get_word_alternatives(self, only_final : bool = True) -> Any:
        return self._aggregate(
            self.items["results"],"word_alternatives",only_final)

    def get_transcript_from_alternatives(self, only_final : bool = True ) \
            -> List:
        alternatives = self._aggregate(
            self.items["results"],"alternatives",only_final)[0]
        return [alternative.get("transcript") for alternative in alternatives]

    def get_transcript_confidences_from_alternatives(self, 
            only_final : bool = True)  -> List:
        alternatives = self._aggregate(
            self.items["results"],"alternatives",only_final)[0]

        return [alternative.get("confidence") for alternative in alternatives]

    def get_timestamps_from_alternatives(self, only_final : bool = True) \
            -> List:
        alternatives = self._aggregate(
            self.items["results"],"alternatives",only_final)[0]
        return [alternative.get("timestamps") for alternative in alternatives]

    def get_word_confidences_from_alternatives(self, only_final : bool = True) \
            -> List:
        alternatives = self._aggregate(
            self.items["results"],"alternatives",only_final)[0]
        return [alternative.get("word_confidence") \
            for alternative in alternatives]

    ############################### PRIVATE METHODS ##########################

    def _parse_data(self, watson_data : Dict) -> bool:
        ## Level 1 
        if "result_index" in watson_data.keys():
            self.items["result_index"] = watson_data["result_index"]
        if "speaker_labels" in watson_data.keys():
            labels = list()
            for label in watson_data["speaker_labels"]:
                labels.append(SpeakerLabel(label))
            self.items["speaker_labels"] = labels
        ## Level 2 (In results)
        if "results" in watson_data.keys():
            results_array = list()
            for results in watson_data["results"]:
                results_array.append(Result({"results" : results}))
            self.items["results"] = results_array
        return True

    def _aggregate(self, results : List[Result], aggregation_key : str, 
            only_final : bool ) -> List[Any]:
        response = list()
        for item in results:
            if only_final:
                if item.get("final"):
                    response.append(item.get(aggregation_key))
            else:
                response.append(item.get(aggregation_key))
        return response








