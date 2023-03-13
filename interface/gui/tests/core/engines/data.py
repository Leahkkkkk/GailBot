import os 
from dataclasses import dataclass
AUDIOROOT = "/Users/yike/Desktop/input"
OUTPUTROOT = "/Users/yike/Desktop/gbout"


@dataclass
class AudioPath:
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
    WATSON_OUT_PATH =  os.path.join(OUTPUTROOT, "watson")
    GOOGLE_OUT_PATH =  os.path.join(OUTPUTROOT, "google")
    WHISPER_OUT_PATH =  os.path.join(OUTPUTROOT, "whisper")
    AUDIO_INPUT = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIUM_AUDIO, OPUS_AUDIO]
    RESULT_OUTPUT = os.path.join(OUTPUTROOT, "result")
    CONVERSATION_DIR = os.path.join(AUDIOROOT, "small_dir")
    TRANSCRIBED_DIR = os.path.join(AUDIOROOT, "medium_transcribed")
    FORTY_MIN = os.path.join(AUDIOROOT, "long/forty.mp3")
    SHORT_AUDIO = os.path.join(AUDIOROOT, "small_dir/test1.wav")
