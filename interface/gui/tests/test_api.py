# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 14:26:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:04:41
from gailbot import GailBot
from tests.services.test_data import PATH
from tests.services.test_data import SETTING_DATA
from gailbot.core.engines.watson import Watson
import logging

HIL_LAB = "/Users/yike/Documents/GitHub/GailBot/plugin_suite/gb_hilab_suite"
HIL_LAB_GITHUB = "https://github.com/YikeLi-Vivi/hillab/archive/refs/heads/main.zip"
HIL_LAB_AWS = "https://gailbot-plugin.s3.us-east-2.amazonaws.com/gb_hilab_suite.zip"


def transcribe(
    files,
    setting_name="test",
    setting_data=SETTING_DATA.WHISPER_PROFILE,
    output=PATH.BACKUP_ROOT,
    fail_test=False,
):
    gb = GailBot(output)
    # assert gb.reset_workspace()
    input = [(f, PATH.OUTPUT_ROOT) for f in files]

    gb.add_sources(input)

    assert gb.add_new_engine(
        SETTING_DATA.WHISPER_NAME, SETTING_DATA.WHISPER_SETTING, overwrite=True
    )
    assert gb.add_new_engine(
        SETTING_DATA.GOOGLE_NAME, SETTING_DATA.GOOGLE_SETTING, overwrite=True
    )
    assert gb.add_new_engine(
        SETTING_DATA.WATSON_NAME, SETTING_DATA.WATSON_SETTING, overwrite=True
    )
    assert gb.add_new_engine(
        SETTING_DATA.WHISPER_SP_NAME, SETTING_DATA.WHISPER_SPEAKER, overwrite=True
    )

    if not gb.is_setting(setting_name):
        assert gb.create_new_setting(setting_name, setting_data)
    assert gb.apply_setting_to_sources(files, setting_name)
    for file in files:
        assert gb.get_src_setting_name(file) == setting_name
        assert gb.is_source(file)
    fails, invalid = gb.transcribe()
    logging.info(fails)
    logging.info(invalid)
    if not fail_test:
        assert not (fails or invalid)
    return fails, invalid


def test_gailbot():
    gb = GailBot(PATH.BACKUP_ROOT)
    # assert gb.reset_workspace()


#####################  test for whisper #####################
def test_whisper():
    fails, invalid = transcribe([PATH.SMALL_AUDIO_WAV, PATH.SMALL_CONVERSATION_DIR])
    assert not fails
    assert not invalid
    assert invalid == []


def test_whisper_wav_suite():
    fails, invalid = transcribe(
        PATH.WAV_SUITE, "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE
    )


def test_whisper_hello():
    fails, invalid = transcribe(
        [PATH.HELLO_1, PATH.HELLO_2], "whisper", SETTING_DATA.WHISPER_PROFILE
    )


def test_whisper_wav_dir():
    fails, invalid = transcribe([PATH.WAV_DIR], "whisper", SETTING_DATA.WHISPER_PROFILE)


def test_whisper_one():
    fails, invalid = transcribe([PATH.HELLO_1], "whisper", SETTING_DATA.WHISPER_PROFILE)


def test_whisper_dir():
    fails, invalid = transcribe(
        [
            PATH.MANY_FILES_DIR,
            PATH.SMALL_CONVERSATION_DIR,
            PATH.TRANSCRIBED_DIR,
            PATH.MANY_SMALL_FILES_DIR,
        ]
    )


def test_with_speaker_one_file():
    fails, invalid = transcribe(
        [PATH.LONG_LIB_RECORD], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE
    )


def test_with_speaker_empty():
    fails, invalid = transcribe(
        [PATH.SineWaveMinus16], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE
    )


def test_with_speaker_seven():
    fails, invalid = transcribe(
        [PATH.assassination1], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE
    )


def test_with_speaker_short():
    fails, invalid = transcribe(
        [PATH.SHORT_AUDIO], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE
    )


def test_with_speaker_dir():
    fails, invalid = transcribe(
        [PATH.SMALL_CONVERSATION_DIR, PATH.MANY_SMALL_FILES_DIR],
        "speaker",
        SETTING_DATA.WHISPER_SPEAKER_PROFILE,
        output=PATH.BACKUP_ROOT,
    )


def test_invalid():
    fails, invalid = transcribe(
        [PATH.INVALID_DATA_DIR, PATH.DUMMY_AUDIO, PATH.EMPTY, PATH.MIX], fail_test=True
    )
    assert invalid


###########################  test for watson #####################################
def test_watson():
    fails, invalid = transcribe([PATH.HELLO_1], "watson", SETTING_DATA.WATSON_PROFILE)


def test_watson_large():
    fails, invalid = transcribe(
        [PATH.LONG_PHONE_CALL], "watson", SETTING_DATA.WATSON_PROFILE
    )


def test_watson_large_two():
    fails, invalid = transcribe(
        [PATH.LONG_LIB_RECORD], "watson", SETTING_DATA.WATSON_PROFILE
    )


def test_watson_dir():
    fails, invalid = transcribe(
        [PATH.MANY_SMALL_FILES_DIR], "watson", SETTING_DATA.WATSON_PROFILE
    )


def test_watson_many():
    fails, invalid = transcribe(
        [PATH.HELLO_1, PATH.HELLO_2, PATH.HELLO_3, PATH.HELLO_4],
        "watson",
        SETTING_DATA.WATSON_PROFILE,
    )


def test_watson_wav_suite():
    fails, invalid = transcribe(
        PATH.WAV_SUITE, "watson", SETTING_DATA.WATSON_PROFILE, fail_test=True
    )


def test_watson_wav_dir():
    fails, invalid = transcribe([PATH.WAV_DIR], "watson", SETTING_DATA.WATSON_PROFILE)


def test_watson_wav_test2a_fail():
    fails, invalid = transcribe([PATH.TEST_2a], "watson", SETTING_DATA.WATSON_PROFILE)


def test_watson_wav_test2a_succ():
    fails, invalid = transcribe(
        [PATH.TEST_2a_trim], "watson", SETTING_DATA.WATSON_PROFILE
    )


def test_watson_wav_test2b():
    fails, invalid = transcribe([PATH.TEST_2b], "watson", SETTING_DATA.WATSON_PROFILE)


def test_watson_icc():
    fails, invalid = transcribe([PATH.ICC_DIR], "watson", SETTING_DATA.WATSON_PROFILE)


def test_watson_long():
    fails, invalid = transcribe(
        [PATH.LONG_PHONE_CALL], "watson", SETTING_DATA.WATSON_PROFILE
    )


def test_watson_empty():
    fails, invalid = transcribe(
        [PATH.SineWaveMinus16], "watson", SETTING_DATA.WATSON_PROFILE
    )


################################### test for google ##################################
def test_google():
    fails, invalid = transcribe([PATH.HELLO_1], "google", SETTING_DATA.GOOGLE_PROFILE)


def test_google_many_hello():
    fails, invalid = transcribe(
        [PATH.HELLO_1, PATH.HELLO_2, PATH.HELLO_3, PATH.HELLO_4],
        "google",
        SETTING_DATA.GOOGLE_PROFILE,
    )


def test_google_two():
    fails, invalid = transcribe([PATH.TWO_MIN_9], "google", SETTING_DATA.GOOGLE_PROFILE)


def test_google_many_two():
    fails, invalid = transcribe(
        [PATH.TWO_MIN_10, PATH.TWO_MIN_7, PATH.TWO_MIN_9, PATH.TWO_MIN_8],
        "google",
        SETTING_DATA.GOOGLE_PROFILE,
    )


def test_google_dir():
    fails, invalid = transcribe(
        [PATH.MANY_FILES_DIR], "google", SETTING_DATA.GOOGLE_PROFILE
    )


def test_google_long():
    fails, invalid = transcribe(
        [PATH.LONG_PHONE_CALL], "google", SETTING_DATA.GOOGLE_PROFILE
    )

def test_google_wav_suite():
    fails, invalid = transcribe(PATH.WAV_SUITE, "google", SETTING_DATA.GOOGLE_PROFILE)

def test_google_icc():
    fails, invalid = transcribe([PATH.ICC_DIR], "google", SETTING_DATA.GOOGLE_PROFILE)

def test_google_40_dirs():
    fails, invalid = transcribe(
        [PATH.DIR_4092, PATH.DIR_4093, PATH.DIR_4112],
        "google",
        SETTING_DATA.GOOGLE_PROFILE,
    )


################################## test for plugin ###########################################
def test_github_url():
    gb = GailBot(PATH.USER_ROOT)
    gb.register_plugin_suite(HIL_LAB_GITHUB)


def test_auto_load():
    gb = GailBot(PATH.USER_ROOT)
    assert gb.is_plugin_suite("gb_hilab_suite")


def test_s3_url():
    gb = GailBot(PATH.USER_ROOT)
    gb.register_plugin_suite(HIL_LAB_AWS)


def test_s3_bucket():
    gb = GailBot(PATH.USER_ROOT)
    gb.register_plugin_suite("gailbot-plugin")


def test_plugin():
    gb = GailBot(PATH.USER_ROOT)
    plugin_suite = gb.register_plugin_suite(HIL_LAB)
    logging.warn(plugin_suite)
    all_plugin = gb.get_all_plugin_suites()
    logging.warn(all_plugin)


def test_delete_plugin():
    gb = GailBot(PATH.USER_ROOT)
    gb.delete_plugin_suite("gb_hilab_suite")


def test_plugin_small():
    fails, invalid = transcribe(
        [PATH.TWO_MIN_10], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_2ab():
    fails, invalid = transcribe([PATH.DIR_2ab], "plugin", SETTING_DATA.WATSON_PROFILE)


def test_plugin_dir():
    fails, invalid = transcribe(
        [PATH.DIR_2ab], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_hello():
    fails, invalid = transcribe(
        [PATH.HELLO_1], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_multiple_files():
    fails, invalid = transcribe(
        [PATH.HELLO_2, PATH.HELLO_1, PATH.HELLO_3],
        "plugin",
        SETTING_DATA.PROFILE_WITH_PLUGIN,
    )


def test_plugin_short_phone():
    fails, invalid = transcribe(
        [PATH.SHORT_PHONE_CALL], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_assasination():
    fails, invalid = transcribe(
        [PATH.assassination1], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_wav():
    fails, invalid = transcribe(
        PATH.WAV_SUITE, "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_empty():
    fails, invalid = transcribe(
        [PATH.SineWaveMinus16], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_wav_dir():
    fails, invalid = transcribe(
        [PATH.WAV_DIR], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN
    )


def test_plugin_multiple():
    fails, invalid = transcribe(
        [PATH.SHORT_AUDIO, PATH.SHORT_PHONE_CALL],
        "plugin",
        SETTING_DATA.PROFILE_WITH_PLUGIN,
    )


def test_plugin_lib():
    fails, invalid = transcribe(
        [PATH.LIB_RECORD_DIR], "plugin", SETTING_DATA.PROFILE_WITH_PLUGIN, invalid=True
    )


def test_plugin_with_spk():
    fails, invalid = transcribe(
        [PATH.SHORT_PHONE_CALL], "plugin", SETTING_DATA.WATSON_PROFILE
    )


##### test workspace ###
def test_reset_ws():
    gb = GailBot(PATH.USER_ROOT)
    assert gb.reset_workspace()
