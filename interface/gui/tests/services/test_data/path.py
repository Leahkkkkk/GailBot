import os
from dataclasses import dataclass


@dataclass
class PATH:
    SETTING_ROOT = (
        "/Users/yike/GailBot/Backend/gailbot_workspace/gailbot_data/setting_source"
    )
    USER_ROOT = "/Users/yike/Desktop/GailBot/Backend"
    BACKUP_ROOT = "/Users/yike/Desktop/GailBotTestDir2/Backend"
    OUTPUT_ROOT = "/Users/yike/Desktop/gbout"
    GOOLE_OUT = os.path.join(OUTPUT_ROOT, "google")
    WATSON_OUT = os.path.join(OUTPUT_ROOT, "watson")
    WHISPER_OUT = os.path.join(OUTPUT_ROOT, "whisper")
    AUDIOROOT = "/Users/yike/Desktop/input"

    # invalid dirtocy
    INVALID_DATA_DIR = os.path.join(AUDIOROOT, "invalidFile")
    DUMMY_AUDIO = os.path.join(AUDIOROOT, "invalidaudio")
    EMPTY = os.path.join(AUDIOROOT, "empty")
    MIX = os.path.join(AUDIOROOT, "mix")
    TRANSCRIBED = os.path.join(AUDIOROOT, "medium_transcribed")
    GB_TEST_SUITE = os.path.join(AUDIOROOT, "medium_dir")
    SMALL_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/test.mp3")
    CHUNK_60 = os.path.join(AUDIOROOT, "all/60sec.mp3")
    MEDIUM_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/mediumtest.mp3")
    SHORT_PHONE_CALL = os.path.join(AUDIOROOT, "all/short_phone_call.wav")
    LARGE_AUDIO_WAV = os.path.join(AUDIOROOT, "all/largetest.wav")
    LARGE_AUDIO_MP3 = os.path.join(AUDIOROOT, "all/largetest.mp3")
    OPUS_AUDIO = os.path.join(AUDIOROOT, "all/test.opus")
    WATSON_OUT_PATH = os.path.join(OUTPUT_ROOT, "Watson")
    GOOGLE_OUT_PATH = os.path.join(OUTPUT_ROOT, "Google")
    WHISPER_OUT_PATH = os.path.join(OUTPUT_ROOT, "Whisper")
    RESULT_OUTPUT = os.path.join(OUTPUT_ROOT, "result")
    CONVERSATION_DIR = os.path.join(AUDIOROOT, "small_dir")
    TRANSCRIBED_DIR = os.path.join(AUDIOROOT, "medium_transcribed")
    FORTY_MIN = os.path.join(AUDIOROOT, "long/forty.mp3")
    SHORT_AUDIO = os.path.join(AUDIOROOT, "small_dir/test1.wav")
    SMALL_AUDIO_WAV = os.path.join(AUDIOROOT, "all/shorttest.wav")
    MEDIUM_AUDIO = os.path.join(AUDIOROOT, "all/mediumtest.wav")
    LONG_PHONE_CALL = os.path.join(AUDIOROOT, "all/long_phone_call.wav")
    SMALL_CONVERSATION_DIR = os.path.join(AUDIOROOT, "small_dir")
    MEDIUM_CONVERSATION_DIR = os.path.join(AUDIOROOT, "medium_dir")
    LIB_RECORD_DIR = os.path.join(AUDIOROOT, "librecord")
    LONG_LIB_RECORD = os.path.join(AUDIOROOT, "3speakersLibrecord.wav")
    LARGE_CONVERSATION_DIR = os.path.join(AUDIOROOT, "all")
    MANY_FILES_DIR = os.path.join(AUDIOROOT, "many_files_dir")
    MANY_SMALL_FILES_DIR = os.path.join(AUDIOROOT, "many_small_files_dir")
    HELLO_1 = os.path.join(AUDIOROOT, "small_test/hello1.wav")
    HELLO_2 = os.path.join(AUDIOROOT, "small_test/hello2.wav")
    HELLO_3 = os.path.join(AUDIOROOT, "small_test/hello3.wav")
    HELLO_4 = os.path.join(AUDIOROOT, "small_test/hello4.wav")
    MANY_HELLO = os.path.join(AUDIOROOT, "small_test")
    TWO_MIN_10 = os.path.join(AUDIOROOT, "many_small_files_dir/test10.wav")
    TWO_MIN_9 = os.path.join(AUDIOROOT, "many_small_files_dir/test9.wav")
    TWO_MIN_8 = os.path.join(AUDIOROOT, "many_small_files_dir/test8.wav")
    TWO_MIN_7 = os.path.join(AUDIOROOT, "many_small_files_dir/test7.wav")
    TEST_2b = os.path.join(AUDIOROOT, "wav/test2b.wav")
    TEST_2a = os.path.join(AUDIOROOT, "wav/test2a.wav")
    TEST_2a_trim = os.path.join(AUDIOROOT, "wav/test2a_trim.wav")
    TEST_2aa = os.path.join(AUDIOROOT, "wav/test2aa.wav")
    TEST__ = os.path.join(AUDIOROOT, "wav/test.wav")
    TEST_OUTPUT_AUDIO = os.path.join(AUDIOROOT, "wav/test_output.wav")
    SineWaveMinus16 = os.path.join(AUDIOROOT, "wav/SineWaveMinus16.wav")
    assassination1 = os.path.join(AUDIOROOT, "wav/07assassination1.wav")
    WAV_DIR = os.path.join(AUDIOROOT, "wav")
    ICC_DIR = os.path.join(AUDIOROOT, "ICC")
    DIR_4157 = os.path.join(AUDIOROOT, "4157")
    DIR_4156 = os.path.join(AUDIOROOT, "4156")
    DIR_4145 = os.path.join(AUDIOROOT, "4145")
    DIR_4112 = os.path.join(AUDIOROOT, "4112")
    DIR_4104 = os.path.join(AUDIOROOT, "4104")
    DIR_4093 = os.path.join(AUDIOROOT, "4093")
    DIR_4092 = os.path.join(AUDIOROOT, "4092")
    DIR_2ab = os.path.join(AUDIOROOT, "test2ab")
    WAV_SUITE = [
        TEST_OUTPUT_AUDIO,
        TEST__,
        TEST_2a,
        TEST_2b,
        assassination1,
        SineWaveMinus16,
    ]
    DEMO1 = os.path.join(AUDIOROOT, "demo-folder/demo1")
    DEMO2 = os.path.join(AUDIOROOT, "demo-folder/demo2")
    DEMO3 = os.path.join(AUDIOROOT, "demo-folder/demo3")