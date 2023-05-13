class ConnectionError(Exception):
    def __str__(self) -> str:
        return "ERROR 404: STT Connection Error"

class TranscriptionError(Exception):
    def __init__(self, error: str = None) -> None:
        super().__init__(error)
        self.error = error
    def __str__(self) -> str:
        return f"ERROR 500: Transcription error: {self.error}"

class APIKeyError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def __str__(self) -> str:
        return "ERROR 508: API key error"

class AudioFileError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "ERROR 510: Not a valid audio file"

class ModelCreateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def __str__(self) -> str:
        return "ERROR 511: Model creation error"

class WatsonMethodExecutionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def __str__(self) -> str:
        return "ERROR 512: Watson method execution error"

class OutPutError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def __str__(self) -> str:
        return "ERROR 520: Error writing output"


class GetUttResultError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
    def __str__(self) -> str:
        return "ERROR 521: Failed to get utterance result"




from dataclasses import dataclass 

@dataclass 
class ERROR: 
    CONNECTION_ERROR = "ERROR 404: No internet connection"
    GOOGLE_TRANSCRIPTION_FAILED = "ERROR 501: Google STT transcription failed"
    WATSON_TRANSCRIPTION_FAILED = "ERROR 502: Watson STT transcription failed"
    WHISPER_TRANSCRIPTION_FAILED = "ERROR 503: Whisper STT transcription failed"
    AUDIO_COMPRESSION_FAILED = "ERROR 505: Failed to compress large audio file to opus format"
    CHILD_PROCESS_STOPPED = "ERROR 531: Child process stopped"
    CHILD_PROCESS_ERROR = "ERROR 532: Child process error"
    CHILD_PROCESS_NOT_FOUND = "ERROR 533: Child process not found"
    