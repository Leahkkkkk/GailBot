import os 
from dataclasses import dataclass

@dataclass
class AudioPath:
    SMALL_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.mp3")
    SMALL_AUDIO_WAV = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.wav")
    CHUNK_60 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/60sec.mp3")
    MEDIUM_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/mediumtest.wav")
    MEDIUM_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/mediumtest.mp3")
    LONG_PHONE_CALL = os.path.join(os.getcwd(), "data/test_file/audio_file_input/long_phone_call.wav")
    SHORT_PHONE_CALL = os.path.join(os.getcwd(), "data/test_file/audio_file_input/short_phone_call.wav")
    LARGE_AUDIO_WAV = os.path.join(os.getcwd(), "data/test_file/audio_file_input/largetest.wav")
    LARGE_AUDIO_MP3 = os.path.join(os.getcwd(), "data/test_file/audio_file_input/largetest.mp3")
    OPUS_AUDIO = os.path.join(os.getcwd(), "data/test_file/compressed/longtest.opus")
    WATSON_OUT_PATH =  os.path.join(os.getcwd(), "data/watson_output")
    GOOGLE_OUT_PATH =  os.path.join(os.getcwd(), "data/google_output")
    WHISPER_OUT_PATH =  os.path.join(os.getcwd(), "data/whisper_output")
    AUDIO_INPUT = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIUM_AUDIO, OPUS_AUDIO]
    RESULT_OUTPUT = os.path.join(os.getcwd(), "data/result_output")
    CONVERSATION_DIR = os.path.join(os.getcwd(), "data/test_file/conversation_dir/")
    TRANSCRIBED_DIR = os.path.join(os.getcwd(), "data/result_output/conversation_dir_gb_output")
    FOURTY_MIN = "/Users/yike/Desktop/input/long/testConvo2.mp3"
    SHORT_AUDIO = "/Users/yike/Desktop/input/short_test/shorttest.wav"