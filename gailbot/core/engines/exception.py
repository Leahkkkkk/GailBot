class ConnectionError(Exception):
    def __str__(self) -> str:
        return "STT Connection Error"

class ThranscriptionError(Exception):
    def __str__(self) -> str:
        return "Transcription error"

class APIKeyError(Exception):
    def __str__(self) -> str:
        return "API key error"

class AudioFileError(Exception):
    def __str__(self) -> str:
        return "Not a valid audio file"
    
    