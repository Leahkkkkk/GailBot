'''
File: test_media.py
Project: GailBot GUI
File Created: Saturday, 21st January 2023 11:01:59 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 25th January 2023 6:47:31 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from gailbot.core.utils import media 
from gailbot.core.utils import general
import shutil
import pytest 
import os
import json

""" global file path for testing  """
INPUT_DIR = f"{os.getcwd()}/data/test_file/audio_file_input"
STEREO_DIR = f"{os.getcwd()}/data/test_file/stereo_file"
OUTPUT_DIR = f"{os.getcwd()}/data/test_file/audio_file_output"
    
@pytest.fixture
def handlers () -> media.AudioHandler:
    audio_handler = media.AudioHandler()
    media_handler = media.MediaHandler()
    return [audio_handler, media_handler]

def test_support_format(handlers):
    for handler in handlers:
        assert handler.supported_formats == handler._SUPPORTED_FORMATS 

def test_is_supported(handlers):
    for handler in handlers:
        basename = "test"
        for format in handler.supported_formats:
            assert handler.is_supported(handler, f"{basename}.{format}")
            
        for format in handler.supported_formats:
            assert not handler.is_supported(handler, f"{basename}.not{format}")
    

def test_read_write_stream(handlers):
    output = f"{OUTPUT_DIR}/write_stream"
    if general.is_directory(output):
        shutil.rmtree(output)
    os.mkdir(output)
    for handler in handlers:
        files = general.filepaths_in_dir(INPUT_DIR)
        for file in files:
            stream: media.AudioStream = handler.read_file(file)
            assert stream
            format = general.get_extension(file)
            handler.write_stream(stream, output, format=format)

""" NOTE: function unimplemented  """
def test_record():
    pass

def test_get_info(handlers):
    output = f"{OUTPUT_DIR}/info"
    if general.is_directory(output):
        shutil.rmtree(output)
    os.mkdir(output)
    for handler in handlers:
        files = general.filepaths_in_dir(INPUT_DIR)
        for file in files:
            stream : media.AudioStream = handler.read_file(file)
            info = handler.info(stream)
            with open(f'{output}/{stream.name}' , "w+") as f:
                f.write(json.dumps(info))

def test_change_volume(handlers):
    for handler in handlers:
        files = general.filepaths_in_dir(INPUT_DIR)
        output = f"{OUTPUT_DIR}/volume"
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        for file in files:
            stream: media.AudioStream = handler.read_file(file)
            assert stream
            after_change: media.AudioStream = handler.change_volume(stream, 10)
            format = general.get_extension(file)
            handler.write_stream(after_change, output, format = format)
    

def test_mono_stereo_convert(handlers):
    for handler in handlers:
        files = general.filepaths_in_dir(INPUT_DIR)
        output = f"{OUTPUT_DIR}/mono_stereo"
        
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        for file in files:
            stream: media.AudioStream = handler.read_file(file)
            stereo = handler.mono_to_stereo(stream, stream )
            assert stereo
            mono_left, mono_right = handler.stereo_to_mono(stereo)
            assert mono_left
            assert mono_right
            format = general.get_extension(file)
            handler.write_stream(mono_left, output, format = format)
            handler.write_stream(mono_right, output, format = format)
            handler.write_stream(stereo, output, format=format)
        
def test_stereo_mono_convert(handlers):
    for handler in handlers:
        files = general.filepaths_in_dir(STEREO_DIR)
        output = f"{OUTPUT_DIR}/mono_stereo"
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        for file in files:
            stream: media.AudioStream = handler.read_file(file)
            assert stream.segment.channels == 2
            mono_left, mono_right = handler.stereo_to_mono(stream)
            assert mono_left, mono_right 
            assert mono_left.segment.channels == 1
            assert mono_right.segment.channels == 1
            stereo: media.AudioStream = handler.mono_to_stereo(mono_left, mono_right)
            assert stereo 
            assert stereo.segment.channels == 2
            format = general.get_extension(file)
            handler.write_stream(mono_right, output, format = format)
            handler.write_stream(mono_left, output, format = format)
            handler.write_stream(stereo, output, format = format)


def test_concat(handlers):
    for handler in handlers:
        output = f"{OUTPUT_DIR}/concat"
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        files = general.filepaths_in_dir(INPUT_DIR)
        for file in files:
            stream1 = handler.read_file(file)
            stream2 = handler.read_file(file)
            concated = handler.concat([stream1, stream2])
            assert concated 
            format = general.get_extension(file)
            handler.write_stream(concated, output, format = format)


def test_overlay(handlers):
    for handler in handlers:
        output = f"{OUTPUT_DIR}/overlay"
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        audio_files = general.filepaths_in_dir(INPUT_DIR)
        music_files = general.filepaths_in_dir(STEREO_DIR)
        for audio, music in zip(audio_files, music_files):
            audio_stream = handler.read_file(audio)
            music_stream = handler.read_file(music)
            overlayed = handler.overlay(audio_stream, music_stream)
            assert overlayed 
            handler.write_stream(overlayed, output, format = general.get_extension(audio))
        

def test_reverse(handlers):
    output = f"{OUTPUT_DIR}/reverse"
    for handler in handlers:
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        files = general.filepaths_in_dir(INPUT_DIR)
        for file in files:
            stream = handler.read_file(file)
            reversed = handler.reverse(stream)
            # assert reversed
            format = general.get_extension(file)
            handler.write_stream(reversed, output, format = format)


def test_chunck(handlers):
    output = f"{OUTPUT_DIR}/chunck"
    for handler in handlers:
        if general.is_directory(output):
            shutil.rmtree(output)
        os.mkdir(output)
        files = general.filepaths_in_dir(INPUT_DIR)
        
        for file in files:
            stream = handler.read_file(file)
            assert stream.segment.duration_seconds > 2.0
            chunks = handler.chunk(stream, 2.0)
            format = general.get_extension(file)
            for chunk in chunks:
                handler.write_stream(chunk, output, format=format)