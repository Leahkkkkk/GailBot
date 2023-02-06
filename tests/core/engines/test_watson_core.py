import os 
from gailbot.core.engines.watson.core import WatsonCore
from gailbot.core.engines.watson.watson import Watson
from gailbot.core.utils.media import MediaHandler
from .data import AudioPath
from gailbot.core.utils.logger import makelogger
import pytest 

logger = makelogger("watsone_engine")
WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"

from .data import AudioPath

def test_watson_core():
    watson_core = WatsonCore(WATSON_API_KEY, WATSON_REGION)
    assert MediaHandler().supported_formats == watson_core.supported_formats
    for format in  watson_core.supported_formats:  
        assert watson_core.is_file_supported(f"test.{format}")

def test_on_invalid_api():    
    with pytest.raises(Exception) as e:
        watson_core = WatsonCore(WATSON_API_KEY + "**", WATSON_REGION)
        logger.info(e)
        assert e

def test_on_invalid_region():
    with pytest.raises(Exception) as e:
        watson_core = WatsonCore(WATSON_API_KEY, WATSON_REGION + "__")
        logger.info(e)
        assert e 
        
@pytest.mark.parametrize("inpath, outpath", [(AudioPath.MEDIUM_AUDIO, AudioPath.WATSON_OUT_PATH)])
def test_convert_to_opus(inpath, outpath):
    watson = WatsonCore(WATSON_API_KEY, WATSON_REGION)
    assert watson._convert_to_opus(inpath, outpath)

def watson_test(inpath, outpath):
    watson = Watson(WATSON_API_KEY, WATSON_REGION)
    assert watson.supported_formats == MediaHandler().supported_formats
    for format in  watson.supported_formats:  
        assert watson.is_file_supported(f"test.{format}")
    assert not watson.was_transcription_successful()
    utterance = watson.transcribe(inpath, 
                      outpath,
                      WATSON_BASE_LANG_MODEL, 
                      WATSON_LANG_CUSTOM_ID)
    logger.info(utterance)
    assert watson.was_transcription_successful() 


@pytest.mark.parametrize(
    "inpath, outpath", [(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH), 
                        (AudioPath.SMALL_AUDIO_WAV, AudioPath.WATSON_OUT_PATH)])
def test_watson_small(inpath, outpath):
    watson_test(inpath, outpath)

@pytest.mark.parametrize(
    "inpath, outpath", [(AudioPath.MEDIUM_AUDIO, AudioPath.WATSON_OUT_PATH)])
def test_watson_media(inpath, outpath):
    watson_test(inpath, outpath)
    
@pytest.mark.parametrize(
    "inpath, outpath", [(AudioPath.LARGE_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)])
def test_watson_large(inpath, outpath):
    watson_test(inpath, outpath)
    
@pytest.mark.parametrize(
    "inpath, outpath", [(AudioPath.LARGE_AUDIO_WAV, AudioPath.WATSON_OUT_PATH)])
def test_watson_large_wav(inpath, outpath):
    watson_test(inpath, outpath)

@pytest.mark.parametrize(
    "inpath, outpath", [(AudioPath.CHUNK_60, AudioPath.WATSON_OUT_PATH)])
def test_watson_60(inpath, outpath):
    watson_test(inpath, outpath)



