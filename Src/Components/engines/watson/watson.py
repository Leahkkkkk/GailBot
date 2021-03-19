# Standard library imports 
from typing import Dict, List, Any, Union
# Local imports 
from ...io import IO 
from ...network import Network
from ..engine import Engine
from ..utterance import Utterance
from .core import WatsonCore
from .recognition_results import RecognitionResult
from .language_model import WatsonLanguageModel
from .acoustic_model import WatsonAcousticModel
from .recognize_callback import customWatsonCallbacks
from ..utterance import Utterance
# Third party imports 

class WatsonEngine(Engine):
    """
    Engine that connects to the IBM Watson STT and provides methods to interact
    with it. 
    """
    def __init__(self, io : IO, network : Network) -> None:
        """
        Args:
            io (IO)
            network (Network)
        """
        self.engine_name = "watson"
        # Objects 
        self.io = io 
        self.network = network
        self.core = WatsonCore(io) 
        self.lm = WatsonLanguageModel()
        self.am = WatsonAcousticModel() 
        self.callback_closure = {
            "callback_status" : {
                "on_transcription" : False, 
                "on_connected" : False, 
                "on_error" : False, 
                "on_inactivity_timeout" : False, 
                "on_listening" : False, 
                "on_hypothesis" : False, 
                "on_data" : False, 
                "on_close" : False},
            "results" : {
                "error" : None,
                "transcript" : list(),
                "hypothesis" : list(),
                "data" : list()}}
        # State parameters 
        self.is_ready_for_transcription = False 
        

    ### Core 
    def configure(self, api_key : str, region : str, audio_path : str, 
            base_model_name : str, language_customization_id : str = "", 
            acoustic_customization_id : str = "") -> bool:
        """
        Configure core attributes for the engine.

        Args:
            api_key (str): User API key to Watson STT service. 
            region (str): User API region. Must be in supported regions.
            audio_path (str): Path to the audio file to transcribe.
            base_model_name (str): Name of the base language model to use. 
            language_customization_id (str): ID of the custom language model.
            acoustic_customization_id (str): ID of the custom acoustic model.

        Returns:
            (bool): True if successfully configured. False otherwise.
        """
        # Connecting to internal components

        if not self.lm.connect_to_service(api_key, region) or \
                not self.am.connect_to_service(api_key, region) or \
                not self.is_file_supported(audio_path) or \
                not base_model_name in self.lm.get_base_models():
            return False 

        if self.lm.get_custom_model(language_customization_id) != None:
            self.core.set_language_customization_id(
                language_customization_id)
        elif len(language_customization_id) > 0:
            return False 
        if self.am.get_custom_model(acoustic_customization_id) != None:
            self.core.set_acoustic_customization_id(
                acoustic_customization_id)
        elif len(acoustic_customization_id) > 0:
            return False 
            
        self._reset_callback_closure()
        recognize_cb = customWatsonCallbacks([self.callback_closure])
        recognize_cb.set_on_transcription_callback(
            self._on_transcription_callback)
        recognize_cb.set_on_connected_callback(
            self._on_connected_callback)
        recognize_cb.set_on_error_callback(
            self._on_error_callback)
        recognize_cb.set_on_inactivity_timeout(
            self._on_inactivity_timeout_callback)
        recognize_cb.set_on_listening_callback(
            self._on_listening_callback)
        recognize_cb.set_on_hypothesis_callback(
            self._on_hypothesis_callback)
        recognize_cb.set_on_data_callback(
            self._on_data_callback)
        recognize_cb.set_on_close_callback(
            self._on_close_callback)

        self.is_ready_for_transcription = \
            self.core.reset_configurations() and \
            self.core.set_api_key(api_key) and \
            self.core.set_service_region(region) and \
            self.core.set_audio_source_path(audio_path) and \
            self.core.set_recognize_callback(recognize_cb) and \
            self.core.set_base_language_model(base_model_name)
        return self.is_ready_for_transcription


    def get_configurations(self) -> Dict[str,Any]:
        """
        Obtain all core configurations of the engine/

        Returns:
            (Dict[str,Any]): Mapping from core configuration to the values.
        """
        return {
            "api_key" : self.core.get_api_key(), 
            "region" : self.core.get_service_region(),
            "audio_path" : self.core.get_audio_source_path(),
            "base_model_name" : self.core.get_selected_base_model(),
            "language_customization_id" : 
                self.core.get_language_customization_id(),
            "acoustic_customization_id" :
                self.core.get_acoustic_customization_id()}

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.
        """
        return self.engine_name

    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported. 

        Returns:
            (List[str]): Supported audio file formats.
        """
        return self.core.get_supported_audio_formats() 

    def is_file_supported(self, file_path : str) -> bool:
        """
        Determine if the given file is supported by the engine.

        Args:
            file_path (str)
        
        Returns:
            (bool): True if file is supported. False otherwise.
        """

        return self.io.is_file(file_path) and \
            self.io.get_file_extension(file_path)[1] \
                in self.core.get_supported_audio_formats()

    def transcribe(self) -> List[Utterance]:
        """
        Transcribe the audio file that can be added through the configure method

        Returns:
            (bool): True if transcribed successfully. False otherwise.
        """
        if not self.is_ready_for_transcription:
            return []
        self.core.recognize_using_websockets()
        utterances = self._prepare_utterance(self.callback_closure)
        self.is_ready_for_transcription = False 
        return utterances

    def get_supported_regions(self) -> List[str]:
        """
        Obtain supported regions for the IBM service.

        Returns:
            (List[str])
        """
        return self.core.get_supported_regions()
    
    def get_supported_audio_formats(self) -> List[str]:
        """
        Obtain audio file formats supported by the engine.

        Returns:
            (List[str]): Supported audio formats.
        """
        return self.core.get_supported_audio_formats()

    ## Language model methods
    def get_base_model(self, model_name : str) -> Union[Dict[str,Any],None]:
        """
        Obtain information about the given base model.

        Args:
            model_name (str): Name of the base language model.
        
        Returns:
            (Union[Dict[str,Any],None])
        """
        return self.lm.get_base_model(model_name)

    def get_base_models(self) -> List[str]:
        """
        Obtain a list of available base language models.

        Returns:
            (List[str])
        """
        return self.lm.get_base_models()

    def get_custom_language_model(self, customization_id : str) \
            -> Union[Dict[str,Any],None]:
        """
        Obtain information about the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 
        
        Returns:
            (Union[Dict[str,Any],None])
        """
        return self.lm.get_custom_model(customization_id)
    
    def create_custom_language_model(self, name : str, base_model_name : str, 
            description : str) -> bool:
        """
        Create a new custom language model.
        
        Args:
            name (str): Name of the custom language model.
            base_model_name (str): Name of the base model to use.
            description (str): Description of the custom language model.

        Returns:
            (bool): True if model created successfully. False otherwise.
        """
        return self.lm.create_custom_model(name, base_model_name, description)

    def delete_custom_language_model(self, customization_id : str) -> bool:
        """
        Delete the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 

        Returns:
            (bool): True if model deleted successfully. False otherwise.
        """
        return self.lm.delete_custom_model(customization_id)

    def train_custom_language_model(self, customization_id : str) -> bool:
        """
        Train a new custom language model with a loaded resource.

        Args:
            customization_id (str): ID of the custom language model to use. 

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.lm.train_custom_model(customization_id)
    
    def reset_custom_language_model(self, customization_id : str) -> bool: 
        """
        Reset the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.lm.create_custom_model(customization_id)

    def upgrade_custom_language_model(self, customization_id : str) -> bool:
        """
        Upgrade the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.lm.upgrade_custom_model(customization_id)

    def get_custom_language_model_corpora(self,customization_id : str) \
            -> Union[List[Dict],None]:
        """
        Get all the corpora used to train the custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 
        
        Returns:
            (Union[List[Dict],None])
        """
        return self.lm.get_corpora(customization_id)
    
    def add_corpus_custom_language_model(self, customization_id : str, 
            corpus_name : str, corpus_file : str) -> bool:
        """
        Add a corpus to the custom language model. 

        Args:
            customization_id (str): ID of the custom language model to use. 
            corpus_name (str): Name of the corpus
            corpus_file (str): Path to the corpus file.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.io.is_file(corpus_file):
            return False
        with open(corpus_file, 'rb') as f:
            return self.lm.add_corpus(customization_id,corpus_name,f)
        
    def delete_corpus_custom_language_model(self, customization_id : str, 
            corpus_name : str) -> bool:
        """
        Delete the specified corpus from the custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 
            corpus_name (str): Name of the corpus

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.lm.delete_corpus(customization_id, corpus_name)
    
    def get_corpus_custom_language_model(self, customization_id : str, 
            corpus_name : str) -> Union[Dict[str,Any],None]:
        """
        Obtain information about a specific corpus used to train the specified 
        custom language model.

        Args:
            customization_id (str): ID of the custom language model to use. 
            corpus_name (str): Name of the corpus

        Returns:
            (Union[Dict[str,Any],None])
        """
        return self.lm.get_corpus(customization_id, corpus_name)

    def get_custom_words_custom_language_model(self, customization_id : str) \
            -> Union[List[Dict], None]:
        """
        Obtain all custom words used to train the specified custom language 
        model.

        Args:
            customization_id (str): ID of the custom language model to use.
        
        Returns:
            (Union[List[Dict], None])
        """
        return self.lm.get_custom_words(customization_id)
    
    def add_words_custom_language_model(self, customization_id : str, 
            words : List[str]) -> bool:
        """
        Add custom words to the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use.
            words (List[str]): List of words to add

        Returns:
            (bool): True if successfully added. False otherwise.
        """
        return self.lm.add_custom_words(customization_id, words)
    
    def delete_word_custom_language_model(self, customization_id : str, 
            word : str) -> bool:
        """
        Delete the specified word from the specified custom language model.

        Args:
            customization_id (str): ID of the custom language model to use.
            words (str): Word to delete.
        
        Returns:
            (bool): True if successfully deleted. False otherwise.
        """
        return self.lm.delete_custom_word(customization_id, word)
    
    def get_grammars_custom_language_model(self, customization_id : str ) \
            -> Union[List[Dict], None]:
        """
        Get all the grammars from the custom language model.

        Args:
            customization_id (str): ID of the custom language model to use.
        
        Returns:
            (Union[List[Dict], None])
        """
        return self.lm.get_custom_grammars(customization_id)
    
    def get_grammar_custom_language_model(self, customization_id : str,
             grammar_name : str) -> Union[Dict, None]:
        """
        Obtain information about the specific grammar in the specified custom 
        language model.

        Args:
            customization_id (str): ID of the custom language model to use.
            grammar_name (str)
        
        Returns:
            (Union[Dict, None])
        """
        return self.lm.get_custom_grammar(customization_id, grammar_name)
    
    def add_grammar_custom_language_model(self, customization_id : str, 
            grammar_name : str, grammar_file : str) -> bool:
        """
        Add grammar to the specified language model.

        Args:
            customization_id (str): ID of the custom language model to use.
            grammar_name (str)
            grammar_file (str): Path to the grammar file.

        Returns:
            (bool): True if added successfully. False otherwise.
        """
        if not self.io.is_file(grammar_file):
            return False
        with open(grammar_file,'rb') as f:
            # TODO: Add content type / determine it somehow. 
            self.lm.add_custom_grammar(
                customization_id, grammar_name, f, "application/srgs")
        
    def delete_grammar_custom_language_model(self, customization_id : str, 
            grammar_name : str) -> bool:
        """
        Delete the specified grammar from the specific custom language model.

        Args:
            customization_id (str): ID of the custom language model to use.
            grammar_name (str)
        
        Returns:
            (bool): True if successfully deleted. False otherwise.
        """
        return self.lm.delete_custom_grammar(customization_id, grammar_name)

    ## Acoustic model methods 
    def get_acoustic_models(self) -> Dict[str,str]:
        """
        Obtain a list of available acoustic models.

        Returns:
            (Dict[str,str]): 
                Mapping from acoustic model name to the customization id.
        """
        return self.am.get_custom_models()
    
    def get_acoustic_model(self, customization_id : str) \
            -> Union[Dict[str,Any],None]:
        """
        Obtain information about a specific custom acoustic model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
        
        Returns:
            (Union[Dict[str,Any],None])
        """
        return self.am.get_custom_model(customization_id)

    def create_acoustic_model(self, name : str, base_model_name : str, 
            description : str) -> bool:
        """
        Create a new custom acoustic model.

        Args:
            name (str): Name of rhe custom acoustic model.
            base_model_name (str): Base language model to use.
            description (str): Description for the new model.

        Returns:
            (bool): True if successfully created. False otherwise.
        """
        if not base_model_name in self.lm.get_base_models():
            return False 
        return self.am.create_custom_model(name, base_model_name, description)
    
    def delete_acoustic_model(self, customization_id : str) -> bool:
        """
        Delete the specified custom acoustic model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
        
        Returns:
            (bool): True if successfully deleted. False otherwise.
        """
        return self.am.delete_custom_model(customization_id)

    def train_acoustic_model(self, customization_id : str) -> bool:
        """
        Train the specified acoustic model with loaded resources.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.am.train_custom_model(customization_id)
    
    def upgrade_acoustic_model(self, customization_id : str) -> bool:
        """
        Upgrade the specified custom acoustic model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.

        Returns:
            (bool): True if upgraded successfully. False otherwise.
        """
        return self.am.upgrade_custom_model(customization_id)

    def get_acoustic_model_audio_resource(self, customization_id : str, 
            audio_name : str) -> Union[Dict,None]:
        """
        Get information about the specified audio resource from the specified 
        custom acoustic model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
            audio_name (str): Name of the audio resource.

        Returns:
            (Union[Dict,None])
        """
        return self.am.get_custom_audio_resource(customization_id, audio_name)
    
    def add_acoustic_model_audio_resource(self, customization_id : str,
            audio_name : str, audio_path : str ) -> bool:
        """
        Add the specified audio resource to the custom audio model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
            audio_name (str): Name of the audio resource.
            audio_path (str): Path to the audio file.
        
        Returns:
            (bool): True if added successfully. False otherwise.
        """
        if not self.io.is_file(audio_path):
            return False 
        with open(audio_path, "rb") as f:
            # TODO: Determine a method to identify the content type. 
            return self.am.add_custom_audio_resource(
                customization_id, audio_name, f,"application/zip")
    
    def delete_acoustic_model_audio_resource(self, customization_id : str, 
            audio_name : str) -> bool:
        """
        Delete the specified audio resource from the custom acoustic model.

        Args:
            customization_id (str): ID of the custom acoustic model to use.
            audio_name (str): Name of the audio resource.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.am.delete_custom_audio_resource(
            customization_id, audio_name)

    ############################### PRIVATE METHODS ###########################

    def _on_transcription_callback(self,
            closure : List[Dict], transcript : List) -> None:
        closure[0]["callback_status"]["on_transcription"] = True 
        #closure[0]["results"]["transcript"].append(transcript)

    def _on_connected_callback(self, closure : List[Dict]) -> None:
        closure[0]["callback_status"]["on_connected"] = True 

    def _on_error_callback(self, closure : List[Dict], error : str) -> None:
        closure[0]["callback_status"]["on_error"] = True 
        closure[0]["results"]["error"] = error

    def _on_inactivity_timeout_callback(
                self, closure : List[Dict], error : str) -> None:
        closure[0]["callback_status"]["on_inactivity_timeout"] = True  
        closure[0]["results"]["error"] = error

    def _on_listening_callback(self, closure : List[Dict]) -> None:
        closure[0]["callback_status"]["on_listening"] = True 

    def _on_hypothesis_callback(self, 
            closure : List[Dict], hypothesis : str) -> None:
        closure[0]["callback_status"]["on_hypothesis"] = True 
        #closure[0]["results"]["hypothesis"].append(hypothesis)

    def _on_data_callback(self, closure : List[Dict], data : Dict) -> None:
        closure[0]["callback_status"]["on_data"] = True  
        closure[0]["results"]["data"].append(data) 

    def _on_close_callback(self, closure : List[Dict]) -> None:
        closure[0]["callback_status"]["on_close"] = True 

    def _prepare_utterance(self, closure : Dict[str, Any]) -> List[Utterance]:
        try:
            # Creating RecognitionResults objects
            recognition_results = list()
            for item in closure["results"]["data"]:
                recognition_result = RecognitionResult(item)
                print("Index")
                print(recognition_result.get_result_index())
                print("Num labels")
                print(recognition_result.num_speaker_labels())
                print("Num results")
                print(recognition_result.num_results())
                print("Labels")
                print(recognition_result.get_speaker_labels())
                print("keyword results")
                print(recognition_result.get_keywords_results())
                print("word alternatives")
                print(recognition_result.get_word_alternatives())
                print("transcript")
                print(recognition_result.get_transcript_from_alternatives())
                print("transcript_confidences")
                print(recognition_result.get_transcript_confidences_from_alternatives())
                print("timestamps")
                print(recognition_result.get_timestamps_from_alternatives())
                print("word_confidences")
                print(recognition_result.get_word_confidences_from_alternatives())
                recognition_results.append(RecognitionResult(item))


            
     


            # results = list()
            # additional_info = list()
            # utterances = list()
            # # Extracting relevant information.
            # for item in closure["results"]["data"]:
            #     if "results" in item and item["results"][0]["final"]:
            #         results.append(item["results"])
            #     if "speaker_labels" in item:
            #         additional_info .append(item["speaker_labels"])
            # # Creating standard mappings for timestamps and speaker labels.



            # # for i, result in enumerate(timestamps):
            # #     # Search to find an appropriate label for this specific start 
            # #     # and end time


            # # Preparing utterance objects 
            # for result , label_information in zip(
            #         timestamps, labels_information):
            #     data = {
            #         "speaker_label" : label_information["speaker"],
            #         "start_time" : result[1],
            #         "end_time" : result[2],
            #         "transcript" : result[0]}
            #     utt = Utterance(data)
            #     if utt.is_configured():
            #         utterances.append(utt)
            # return utterances
        except:
            return []

    def _reset_callback_closure(self) -> None:
        self.callback_closure = {
            "callback_status" : {
                "on_transcription" : False, 
                "on_connected" : False, 
                "on_error" : False, 
                "on_inactivity_timeout" : False, 
                "on_listening" : False, 
                "on_hypothesis" : False, 
                "on_data" : False, 
                "on_close" : False},
            "results" : {
                "error" : None,
                "transcript" : list(),
                "hypothesis" : list(),
                "data" : list()}}

