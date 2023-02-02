from gailbot.core.utils.logger import makelogger 
from gailbot.core.engines.google.google import Google
from gailbot.core.engines.google.core import GoogleCore
from .data import AudioPath
import pytest 


test_logger = makelogger("pytest_google_engine")
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
def test_google_engine(audio_path):
    core = Google()
    assert not core.transcribe_success
    core.transcribe(audio_path, AudioPath.GOOGLE_OUT_PATH)
    assert core.transcribe_success