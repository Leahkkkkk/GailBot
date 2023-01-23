from gailbot.core.utils import media 
from gailbot.core.utils import general
import shutil
import pytest 
import os

""" global file path for testing  """
INPUT_DIR = f"{os.getcwd()}/tests/test_file/audio_file_input"
STEREO_DIR = f"{os.getcwd()}/tests/test_file/stereo_file"
OUTPUT_DIR = f"{os.getcwd()}/tests/test_file/audio_file_output"
    
@pytest.fixture
def audio_handler () -> media.AudioHandler:
    audio_handler = media.AudioHandler()
    return audio_handler

def test_support_format(audio_handler):
    assert audio_handler.supported_formats == audio_handler._SUPPORTED_FORMATS 

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
   

def test_mono_stereo_convert(audio_handler: media.AudioHandler):
    files = general.filepaths_in_dir(INPUT_DIR)
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    for file in files:
        stream: media.AudioStream = audio_handler.read_file(file)
        stereo = audio_handler.mono_to_stereo(stream, stream )
        assert stereo
        mono_left, mono_right = audio_handler.stereo_to_mono(stereo)
        assert mono_left
        assert mono_right
        format = general.get_extension(file)
        audio_handler.write_stream(mono_left, OUTPUT_DIR, format = format)
        audio_handler.write_stream(mono_right, OUTPUT_DIR, format = format)
        audio_handler.write_stream(stereo, OUTPUT_DIR, format=format)
        
def test_stereo_mono_convert(audio_handler: media.AudioHandler):
    files = general.filepaths_in_dir(STEREO_DIR)
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    for file in files:
        stream: media.AudioStream = audio_handler.read_file(file)
        assert stream.segment.channels == 2
        mono_left, mono_right = audio_handler.stereo_to_mono(stream)
        assert mono_left, mono_right 
        assert mono_left.segment.channels == 1
        assert mono_right.segment.channels == 1
        stereo: media.AudioStream = audio_handler.mono_to_stereo(mono_left, mono_right)
        assert stereo 
        assert stereo.segment.channels == 2
        format = general.get_extension(file)
        audio_handler.write_stream(mono_right, OUTPUT_DIR, format = format)
        audio_handler.write_stream(mono_left, OUTPUT_DIR, format = format)
        audio_handler.write_stream(stereo, OUTPUT_DIR, format = format)


def test_concat(audio_handler: media.AudioHandler):
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    files = general.filepaths_in_dir(INPUT_DIR)
    for file in files:
        stream1 = audio_handler.read_file(file)
        stream2 = audio_handler.read_file(file)
        concated = audio_handler.concat([stream1, stream2])
        assert concated 
        format = general.get_extension(file)
        audio_handler.write_stream(concated, OUTPUT_DIR, format = format)


def test_overlay(audio_handler: media.AudioHandler):
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    audio_files = general.filepaths_in_dir(INPUT_DIR)
    music_files = general.filepaths_in_dir(STEREO_DIR)
    for audio, music in zip(audio_files, music_files):
        audio_stream = audio_handler.read_file(audio)
        music_stream = audio_handler.read_file(music)
        overlayed = audio_handler.overlay(audio_stream, music_stream)
        assert overlayed 
        audio_handler.write_stream(overlayed, OUTPUT_DIR, format = general.get_extension(audio))
     

def test_reverse(audio_handler: media.AudioHandler):
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    files = general.filepaths_in_dir(INPUT_DIR)
    for file in files:
        stream = audio_handler.read_file(file)
        reversed = audio_handler.reverse(stream)
        # assert reversed
        format = general.get_extension(file)
        audio_handler.write_stream(reversed, OUTPUT_DIR, format = format)

def test_chunck(audio_handler: media.AudioHandler):
    if general.is_directory(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    files = general.filepaths_in_dir(INPUT_DIR)
    
    for file in files:
        stream = audio_handler.read_file(file)
        assert stream.segment.duration_seconds > 2.0
        chunks = audio_handler.chunk(stream, 2.0)
        format = general.get_extension(file)
        for chunk in chunks:
            audio_handler.write_stream(chunk, OUTPUT_DIR, format=format)