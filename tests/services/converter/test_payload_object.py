from gailbot.services.converter.payload.audioPayload import AudioPayload, load_audio_payload
from gailbot.services.converter.payload.conversationDirectoryPayload import ConversationDirectoryPayload, load_conversation_dir_payload
from gailbot.services.converter.payload.transcribedDirPayload import TranscribedDirPayload, load_transcribed_dir_payload
from tests.core.engines.data import AudioPath
from gailbot.services.organizer.source import SourceObject, SourceManager
from gailbot.services.organizer.settings import SettingObject
from gailbot.services.converter.payload.payloadObject import PayLoadObject, PayLoadStatus
import pytest
from gailbot.core.utils.general import get_name
from gailbot.core.utils.logger import makelogger 


TEST_SETTING = SettingObject ({"engine_setting": {"engine":"whisper"},
                "plugin_setting": ["hilab"]}, "test_setting")
TEST_TRANSCRIBE_RESULT = { "test": [{"speaker": 1, "endtime": 1, "starttime": "2", "text": "hello"}]}
TEST_ANALYSIS_RESULT = {"test": [{"speaker-analysis": 1, "endtime-analysis": 1, "starttime-analysis": "2", "text-analysis": "hello"}]}
TEST_FORMAT_RESULT = {"test" : [{"speaker-format": 1, "endtime": 1, "starttime-format": "2", "text-format": "hello"}]}

logger = makelogger("audiopayload_test ")
    
# create Audio payload
audio_source = SourceObject(AudioPath.MEDIUM_AUDIO, get_name(AudioPath.MEDIUM_AUDIO), output=AudioPath.RESULT_OUTPUT)
audio_source.apply_setting(TEST_SETTING)
audio_payload: AudioPayload = load_audio_payload(audio_source)[0]

# create the directory payload 
dir_source = SourceObject(AudioPath.CONVERSATION_DIR, get_name(AudioPath.CONVERSATION_DIR), AudioPath.RESULT_OUTPUT)
dir_source.apply_setting(TEST_SETTING)
dir_payload: ConversationDirectoryPayload = load_conversation_dir_payload(dir_source)[0]


# transcribed directory output 
trans_dir_source = SourceObject(AudioPath.TRANSCRIBED_DIR, get_name(AudioPath.TRANSCRIBED_DIR),AudioPath.RESULT_OUTPUT)
trans_dir_source.apply_setting(TEST_SETTING)
trans_dir_payload: TranscribedDirPayload = load_transcribed_dir_payload(trans_dir_source)[0]


@pytest.mark.parametrize("test_payload", [audio_payload, dir_payload, trans_dir_payload])
def test_construct_payload(test_payload: PayLoadObject):
    assert test_payload
    logger.info(test_payload.supported_format)
    logger.info(test_payload.get_status()) 
    logger.info(test_payload.get_source())
    # assert not test_payload.transcribed
    assert not test_payload.analyzed
    assert not test_payload.formatted
    logger.info(test_payload.get_plugin_setting())
    logger.info(test_payload.get_engine_setting())
    logger.info(test_payload.get_status())
    assert test_payload.set_transcription_result(TEST_TRANSCRIBE_RESULT)
    assert test_payload.set_format_result(TEST_FORMAT_RESULT)
    assert test_payload.set_analysis_result(TEST_ANALYSIS_RESULT)
    logger.info(test_payload.get_analyze_result())
    logger.info(test_payload.get_format_result())
    logger.info(test_payload.get_transcription_result())
    test_payload.save()

@pytest.mark.parametrize("path_name", [AudioPath.SMALL_AUDIO_MP3, AudioPath.SMALL_AUDIO_WAV, AudioPath.OPUS_AUDIO])
def test_audio_is_supported(path_name):
    test_source_manager = SourceManager()
    test_source_manager.add_source(path_name, AudioPath.WATSON_OUT_PATH)
    source_name = get_name(path_name)

    test_payload = AudioPayload(test_source_manager.get_source(source_name))
    assert(test_payload.is_supported(path_name))

@pytest.mark.parametrize("path_name", [AudioPath.SMALL_AUDIO_MP3, AudioPath.SMALL_AUDIO_WAV, AudioPath.OPUS_AUDIO])
def test_audio_set_initial_status(path_name):
    test_source_manager = SourceManager()
    test_source_manager.add_source(path_name, AudioPath.WATSON_OUT_PATH)
    source_name = get_name(path_name)

    test_payload = AudioPayload(test_source_manager.get_source(source_name))
    test_payload._set_initial_status
    assert(test_payload.status == PayLoadStatus.INITIALIZED)

def test_audio_copy_file():
    pass

@pytest.mark.parametrize("path_name", [AudioPath.SMALL_AUDIO_MP3, AudioPath.SMALL_AUDIO_WAV, AudioPath.OPUS_AUDIO])
def test_audio_supported_format(path_name):
    test_source_manager = SourceManager()
    test_source_manager.add_source(path_name, AudioPath.WATSON_OUT_PATH)
    source_name = get_name(path_name)

    test_payload = AudioPayload(test_source_manager.get_source(source_name))
    assert(test_payload.supported_format == ["mp3", "wav", "opus"])

def test_dir_is_supported():
    assert(dir_payload.is_supported(AudioPath.CONVERSATION_DIR))

def test_dir_copy_file():
    pass

def test_dir_set_initial_status():
    dir_payload._set_initial_status
    assert(dir_payload.status == PayLoadStatus.INITIALIZED)