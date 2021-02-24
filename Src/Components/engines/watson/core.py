# Standard library imports 
from typing import List, Any, Tuple
# Local imports 
from ...network import Network
# Third party imports 
from ibm_watson import SpeechToTextV1 , ApiException, DetailedResponse
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
        "dallas" : "https://api.us-south.speech-to-text.watson.cloud.ibm.com",
        "washington" : "https://api.us-east.speech-to-text.watson.cloud.ibm.com", 
        "frankfurt" : "https://api.eu-de.speech-to-text.watson.cloud.ibm.com",
        "sydney" : "https://api.au-syd.speech-to-text.watson.cloud.ibm.com",
        "tokyo" : "https://api.jp-tok.speech-to-text.watson.cloud.ibm.com", 
        "london" : "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com",
        "seoul" : "https://api.kr-seo.speech-to-text.watson.cloud.ibm.com"}

    content_types = (
        "application/octet-stream", "audio/alaw", "audio/basic", "audio/flac", 
        "audio/g729", "audio/l16", "audio/mp3", "audio/mpeg", "audio/mulaw",
        "audio/ogg", "audio/ogg;codecs=opus", "audio/ogg;codecs=vorbis",
        "audio/wav, audio/webm", "audio/webm;codecs=opus", 
        "audio/webm;codecs=vorbis")
    
    def __init__(self, network : Network) -> None:
        # Default parameters 
        self.watson_defaults = {
            "ssl_verification" : True,
            "headers" : {
                "x-watson-learning-opt-out" : True },
            "customization_weight" : 0.3,
            "inactivity_timeout" : 30, 
            "interim_results" : False, 
            "keyword_threshold" : 0.8,
            "max_alternatives" : 1,
            "word_confidence" : True,
            "timestamps" : True, 
            "profanity_filer" : False, 
            "smart_formatting" : True, 
            "speaker_labels" : True, 
            "redaction" : False, 
            "processing_metrics" : False, 
            "audio_metrics" : False, 
            "end_of_phrase_silence_time" : 0.8,
            "split_transcript_at_phrase_end" : True, 
            "speech_detector_sensitivity" : 0.7, 
            "background_audio_supression" : 0.3}
        self.inputs = {
            "api_key" : None,
            "region" : None,
            "audio_source" : None,
            "audio" : None,
            "content_type" : None,
            "recognize_callback" : None,
            "model" : None,
            "language_customization_id" : None,
            "acoustic_customization_id" : None}
        # State parameters 
        self.network = network
        self.authenticator = None

    ### SETTERS

    def set_api_key(self, api_key : str) -> bool:
        """
        Set the api key for the STT service.

        Args:
            apikey (str): Valid API key for the watson STT service.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        success, authenticator = self._initialize_authenticator(api_key)
        if not success:
            return False
        self.authenticator = authenticator 
        self.inputs["api_key"] = api_key
        return True  

    def set_service_region(self, region : str) -> bool:
        """
        Set the region associated with the api key for the STT service.

        Args:
            region (str): 
                Region for the STT service. Must be a supported regions.
        """
        if not region in self.regions.keys():
            return False 
        self.inputs["region"] = region
        return True

    def set_ssl_verification(self, verify : bool) -> bool:
        pass 

    def set_content_type(self, content_type : str) -> bool:
        pass 

    def set_recognize_callback(self, recognize_callback : RecognizeCallback)\
             -> bool:
        pass 

    def set_audio_source(self, audio_source : str) -> bool:
        pass 
    
    def set_base_language_model(self, base_model_name : str) -> bool:
        pass 

    def set_language_customization_id(self, customization_id : str) -> bool:
        pass 

    def set_acoustic_customization_id(self, customization_id : str) -> bool:
        pass 

    def set_customization_weight(self, weight : float) -> bool:
        pass 

    ### GETTERS

    def get_api_key(self) -> str:
        pass 

    def get_service_region(self) -> str:
        pass 

    def is_ssl_verified(self) -> bool:
        pass 

    def get_audio_source(self) -> str:
        pass 

    def get_selected_base_model(self) -> str:
        pass 

    def get_language_customization_id(self) -> str:
        pass 

    def get_customization_weight(self) -> float:
        pass 

    def get_supported_regions(self) -> List[str]:
        pass

    ### Others 

    ############################ PRIVATE METHODS ###########################

    def _determine_audio_type(self) -> str:
        pass 

    def _determine_content_type(self) -> str:
        pass 

    def _is_service_ready(self) -> bool:
        pass 

    def _initialize_authenticator(self, apikey : str) \
            -> Tuple[bool, IAMAuthenticator]:
        """
        Initialize an authenticator object after ensuring that the api key is 
        valid.

        Args:
            apikey (str): API key for the watson STT service. 

        Returns:
            (Tuple[bool, IAMAuthenticator]):
                True + authenticator object if valid.
                False + None otherwise.
        """
        try:
            authenticator = IAMAuthenticator(apikey)
            stt = SpeechToTextV1(authenticator=authenticator)
            stt.list_models()
            return (True, authenticator)
        except:
            return (False, None)
        


    