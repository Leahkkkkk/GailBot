class ConnectionError(Exception):
    def __str__(self) -> str:
        return "STT Connection Error"

class TranscriptionError(Exception):
    def __str__(self) -> str:
        return "Transcription error"

class APIKeyError(Exception):
    def __str__(self) -> str:
        return "API key error"

class AudioFileError(Exception):
    def __str__(self) -> str:
        return "Not a valid audio file"

class ModelCreateError(Exception):
    def __str__(self) -> str:
        return "Model creation error"

class WatsonMethodExecutionError(Exception):
    def __str__(self) -> str:
        return "Watson method execution error"

class OutPutError(Exception):
    def __str__(self) -> str:
        return "Error writing output"