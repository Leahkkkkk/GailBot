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
    watson_core = Watson(WATSON_API_KEY, WATSON_REGION)
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
        
@pytest.mark.parametrize("inpath", [AudioPath.MEDIUM_AUDIO])
def test_convert_to_opus(inpath):
    watson = WatsonCore(WATSON_API_KEY, WATSON_REGION)
    assert watson._convert_to_opus(inpath)

def watson_test(inpath):
    watson = Watson(WATSON_API_KEY, WATSON_REGION)
    assert watson.supported_formats == MediaHandler().supported_formats
    for format in  watson.supported_formats:  
        assert watson.is_file_supported(f"test.{format}")
    assert not watson.was_transcription_successful()
    utterance = watson.transcribe(inpath, 
                      WATSON_BASE_LANG_MODEL, 
                      WATSON_LANG_CUSTOM_ID)
    logger.info(utterance)
    assert watson.was_transcription_successful() 

@pytest.mark.parametrize(
    "inpath", [AudioPath.SMALL_AUDIO_MP3, AudioPath.SMALL_AUDIO_WAV])
def test_watson_small(inpath):
    logger.info("test watson small audio")
    watson_test(inpath)

@pytest.mark.parametrize("inpath", [AudioPath.MEDIUM_AUDIO])
def test_watson_media(inpath):
    watson_test(inpath)
    
@pytest.mark.parametrize(
    "inpath", [AudioPath.LARGE_AUDIO_MP3])
def test_watson_large(inpath):
    watson_test(inpath)
    
@pytest.mark.parametrize(
    "inpath", [AudioPath.LARGE_AUDIO_WAV])
def test_watson_large_wav(inpath):
    watson_test(inpath)

@pytest.mark.parametrize(
    "inpath", [AudioPath.CHUNK_60])
def test_watson_60(inpath):
    watson_test(inpath)



