import os 
from dataclasses import dataclass

@dataclass
class AudioPath:
    SMALL_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.mp3")
    SMALL_AUDIO_WAV = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.wav")
    CHUNK_60 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/60sec.mp3")
    MEDIUM_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/mediumtest.wav")
    MEDIUM_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/mediumtest.mp3")
    LARGE_AUDIO_WAV = os.path.join(os.getcwd(), "data/test_file/audio_file_input/largetest.wav")
    LARGE_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/largetest.mp3")
    OPUS_AUDIO = os.path.join(os.getcwd(), "data/test_file/compressed/longtest.opus")
    WATSON_OUT_PATH =  os.path.join(os.getcwd(), "data/watson_output")
    GOOGLE_OUT_PATH =  os.path.join(os.getcwd(), "data/google_output")
    AUDIO_INPUT = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIUM_AUDIO, OPUS_AUDIO]
   