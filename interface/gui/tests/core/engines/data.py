import os 
from dataclasses import dataclass
AUDIOROOT = "/Users/yike/Desktop/input"
OUTPUTROOT = "/Users/yike/Desktop/gbout"


@dataclass
class AudioPath:
    OPUS_AUDIO              = os.path.join(AUDIOROOT, "all/test.opus")
    WATSON_OUT_PATH         = os.path.join(OUTPUTROOT, "watson")
    GOOGLE_OUT_PATH         = os.path.join(OUTPUTROOT, "google")
    WHISPER_OUT_PATH        = os.path.join(OUTPUTROOT, "whisper")
    RESULT_OUTPUT           = os.path.join(OUTPUTROOT, "result")
    SMALL_AUDIO_MP3         = os.path.join(AUDIOROOT, "all/test.mp3")
    CHUNK_60                = os.path.join(AUDIOROOT, "all/60sec.mp3")
    MEDIUM_AUDIO_MP3        = os.path.join(AUDIOROOT, "all/mediumtest.mp3")
    LARGE_AUDIO_MP3         = os.path.join(AUDIOROOT, "all/largetest.mp3")
    FORTY_MIN               = os.path.join(AUDIOROOT, "long/forty.mp3")
    
    ##### the below test will be run for controller ###
    SMALL_AUDIO_WAV         = os.path.join(AUDIOROOT, "all/shorttest.wav")
    MEDIUM_AUDIO            = os.path.join(AUDIOROOT, "all/mediumtest.wav")
    LONG_PHONE_CALL         = os.path.join(AUDIOROOT, "all/long_phone_call.wav")
    SHORT_PHONE_CALL        = os.path.join(AUDIOROOT, "all/short_phone_call.wav")
    LARGE_AUDIO_WAV         = os.path.join(AUDIOROOT, "all/largetest.wav" )
    CONVERSATION_DIR        = os.path.join(AUDIOROOT, "small_dir")
    TRANSCRIBED_DIR         = os.path.join(AUDIOROOT, "medium_transcribed")
    SHORT_AUDIO             = os.path.join(AUDIOROOT, "small_dir/test1.wav")
    SMALL_CONVERSATION_DIR  = os.path.join(AUDIOROOT, "small_dir")
    MEDIUM_CONVERSATION_DIR = os.path.join(AUDIOROOT, "medium_dir")
    LARGE_CONVERSATION_DIR  = os.path.join(AUDIOROOT, "all")
    MANY_FILES_DIR          = os.path.join(AUDIOROOT, "many_files_dir")
    AUDIO_INPUT             = [SMALL_AUDIO_MP3, SMALL_AUDIO_WAV, MEDIUM_AUDIO, OPUS_AUDIO]
