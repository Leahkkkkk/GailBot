import os 
from dataclasses import dataclass

@dataclass 
class PATH:
    USER_ROOT = "/Users/yike/Desktop"
    OUTPUT_ROOT = "/Users/yike/Desktop/gbout"
    AUDIOROOT = "/Users/yike/Desktop/input"
    INVALID_DATA_DIR = os.path.join(AUDIOROOT, "invalidFile")
    DUMMY_AUDIO = os.path.join(AUDIOROOT, "invalidaudio")
    TRANSCRIBED = os.path.join(AUDIOROOT, "medium_transcribed")
    GB_TEST_SUITE = os.path.join(AUDIOROOT, "medium_dir")
    INVALID_PATH = os.path.join(AUDIOROOT, "invalidFile")
    SMALL_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/test.mp3")
    SMALL_AUDIO_WAV = os.path.join(AUDIOROOT, "all/shorttest.wav")
    CHUNK_60 = os.path.join(AUDIOROOT, "all/60sec.mp3")
    MEDIUM_AUDIO = os.path.join(AUDIOROOT, "all/mediumtest.wav")
    MEDIUM_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/mediumtest.mp3")
    LONG_PHONE_CALL = os.path.join(AUDIOROOT, "all/long_phone_call.wav")
    SHORT_PHONE_CALL = os.path.join(AUDIOROOT, "all/short_phone_call.wav")
    LARGE_AUDIO_WAV = os.path.join(AUDIOROOT,"all/largetest.wav" )
    LARGE_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/largetest.mp3")
    OPUS_AUDIO = os.path.join(AUDIOROOT, "all/test.opus")
    WATSON_OUT_PATH =  os.path.join(OUTPUT_ROOT, "watson")
    GOOGLE_OUT_PATH =  os.path.join(OUTPUT_ROOT, "google")
    WHISPER_OUT_PATH =  os.path.join(OUTPUT_ROOT, "whisper")
    AUDIO_INPUT = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIUM_AUDIO, OPUS_AUDIO]
    RESULT_OUTPUT = os.path.join(OUTPUT_ROOT, "result")
    CONVERSATION_DIR = os.path.join(AUDIOROOT, "small_dir")
    TRANSCRIBED_DIR = os.path.join(AUDIOROOT, "medium_transcribed")
    FORTY_MIN = os.path.join(AUDIOROOT, "long/forty.mp3")
    SHORT_AUDIO = os.path.join(AUDIOROOT, "small_dir/test1.wav")



