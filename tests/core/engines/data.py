import os 
from dataclasses import dataclass

@dataclass
class AudioPath:
    SMALL_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.mp3")
    SMALL_AUDIO_WAV = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.wav")
    MEDIA_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/longtest.wav")
    OPUS_AUDIO = os.path.join(os.getcwd(), "data/test_file/compressed/longtest.opus")
    WATSON_OUT_PATH =  os.path.join(os.getcwd(), "data/watson_output")
    GOOGLE_OUT_PATH =  os.path.join(os.getcwd(), "data/google_output")
    AUDIO_INPUT = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIA_AUDIO, OPUS_AUDIO]