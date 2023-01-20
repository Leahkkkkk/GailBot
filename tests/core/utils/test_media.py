from gailbot.core.utils import media 
from gailbot.core.utils import general
import shutil
import pytest 
import os

""" global file path for testing  """
INPUT_DIR = f"{os.getcwd()}/tests/test_file/audio_file_input"
OUTPUT_DIR = f"{os.getcwd()}/tests/test_file/audio_file_output"
    
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
    

def test_read_write_stream(audio_handler: media.AudioHandler):
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    files = general.filepaths_in_dir(INPUT_DIR)
    for file in files:
        stream: media.AudioStream = audio_handler.read_file(file)
        assert stream
        format = general.get_extension(file)
        audio_handler.write_stream(stream, OUTPUT_DIR, format=format)

""" NOTE: function unimplemented  """
def test_record():
    pass


def test_change_volume(audio_handler: media.AudioHandler):
    files = general.filepaths_in_dir(INPUT_DIR)
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    for file in files:
        stream: media.AudioStream = audio_handler.read_file(file)
        assert stream
        after_change: media.AudioStream = audio_handler.change_volume(stream, 20)
        format = general.get_extension(file)
        audio_handler.write_stream(after_change, OUTPUT_DIR, format = format)
   

""" TODO:  """
def fail_test_mono_stereo_convert(audio_handler: media.AudioHandler):
    files = general.filepaths_in_dir(INPUT_DIR)
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    for file in files:
        stream: media.AudioStream = audio_handler.read_file(file)
        mono_left, mono_right = audio_handler.stereo_to_mono(stream)
        assert mono_left
        assert mono_right
        format = general.get_extension(file)
        audio_handler.write_stream(mono_left, OUTPUT_DIR, format = format)
        audio_handler.write_stream(mono_right, OUTPUT_DIR, format = format)
        
        monoStream = audio_handler.mono_to_stereo(
            mono_left, mono_right)
        assert monoStream
        audio_handler.write_stream(monoStream, format=format)
        