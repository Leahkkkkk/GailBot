from gailbot.core.utils import media 
import pytest 
import unittest

@pytest.fixture
def audio_handler () -> media.AudioHandler:
    audio_handler = media.AudioHandler()
    return audio_handler

def test_support_format(audio_handler):
    assert audio_handler.supported_formats == audio_handler._SUPPORTED_FORMATS 

""" TODO: failure in test """
def test_is_supported(audio_handler):
    basename = "test"
    for format in audio_handler.supported_formats:
        assert audio_handler.is_supported(audio_handler, f"{basename}.{format}")
        
    for format in audio_handler.supported_formats:
        assert not audio_handler.is_supported(audio_handler, f"{basename}.not{format}")
    
""" TODO: failure in test  """
def test_read_file(audio_handler):
    basename = "test"
    for format in audio_handler.supported_formats:
        audio_handler.read_file(f"[basename.invalid{format}")
        assert not audio_handler.is_supported(audio_handler, f"{basename}.invalid{format}")
        audio_handler.read_file(f"[basename.{format}")
        assert audio_handler.source == f"[basename.{format}"



def test_record():
    pass

def test_write_stream():
    pass

""" TODO:  """
def test_info():
    pass

def test_change_volume(audio_handler):
    audio_stream = media.AudioStream()
    first_vol = audio_stream.segment
    change = 4.0
    audio_handler.change_volume(audio_handler, change)
    assert audio_stream.segment == first_vol + change

""" TODO:  """
def test_mono_to_stereo():
    pass 
