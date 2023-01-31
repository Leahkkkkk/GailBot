from google.cloud import speech_v1p1beta1 as speech


class GoogleCore: 
    
    def __init__(self) -> None:
        raise NotImplementedError
    
    
    def transcribe(self) -> None:
        raise NotImplementedError
    
    
    def prepare_utterance(self) -> None:
        raise NotImplementedError