from gailbot.core.utils.logger import makelogger 
from gailbot.core.engines.google.google import Google
from gailbot.core.engines.google.core import GoogleCore
from .data import AudioPath
import pytest 


logger = makelogger("pytest_google_engine")
def test_init_google():
    google_engine = Google()
    assert not google_engine.transcribe_success
    google_engine.transcribe(AudioPath.SMALL_AUDIO_WAV, AudioPath.GOOGLE_OUT_PATH)

@pytest.mark.parametrize("audio_path", [AudioPath.SMALL_AUDIO_WAV, AudioPath.SMALL_AUDIO_MP3])
def test_core_run_engine(audio_path):
    core = GoogleCore()
    core.run_engine(audio_path)

@pytest.mark.parametrize("audio_path", [AudioPath.SMALL_AUDIO_WAV])
def test_core_transcribe(audio_path):
    core = GoogleCore()    
    core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    
@pytest.mark.parametrize("audio_path", [AudioPath.SMALL_AUDIO_MP3, AudioPath.SMALL_AUDIO_WAV])
def test_small_file(audio_path):
    core = Google()
    assert not core.transcribe_success
    core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    assert core.transcribe_success
    
@pytest.mark.parametrize("audio_path", [AudioPath.LARGE_AUDIO_MP3])
def test_chunking_large_audio(audio_path):
    core = GoogleCore()
    dir = core._chunk_audio(audio_path, core.workspace_directory)
    from gailbot.core.utils.general import paths_in_dir
    files = paths_in_dir(dir)
    files = sorted(files, key = lambda file: (len(file), file))
    for file in files:
        logger.info(file)

@pytest.mark.parametrize("audio_path", [AudioPath.LARGE_AUDIO_MP3])
def test_large_audio(audio_path):
    core = GoogleCore()
    assert not core.transcribe_success
    core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    assert core.transcribe_success
    
@pytest.mark.parametrize("audio_path", [AudioPath.MEDIUM_AUDIO_MP3])
def test_medium_audio(audio_path):
    core = GoogleCore()
    assert not core.transcribe_success
    res = core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    assert core.transcribe_success
    logger.info("the final result of the utterance")
    logger.info(res)
    
@pytest.mark.parametrize("audio_path", [AudioPath.CHUNK_60])
def test_60_sec_audio(audio_path):
    core = GoogleCore()
    assert not core.transcribe_success
    res = core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    assert core.transcribe_success
    logger.info("the final result of the utterance")
    logger.info(res)
