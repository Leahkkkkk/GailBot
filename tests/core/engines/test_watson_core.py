import os 
from gailbot.core.engines.watson.core import WatsonCore
from gailbot.core.engines.watson.recognize_callback import CustomWatsonCallbacks
from gailbot.core.engines.watson.watson import Watson
from gailbot.core.utils.media import MediaHandler
from ibm_watson.websocket.recognize_listener import RecognizeListener
import pytest 

WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
SMALL_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.mp3")
MEDIA_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/longtest.wav")
OPUS_AUDIO = os.path.join(os.getcwd(), "data/test_file/audio_file_input/longtest.wav")

AUDIO_INPUT = [SMALL_AUDIO, MEDIA_AUDIO, OPUS_AUDIO]

OUT_PATH =  os.path.join(os.getcwd(), "data/watson_output")

def test_watson_core():
    watson_core = WatsonCore(WATSON_API_KEY, WATSON_REGION)
    assert MediaHandler().supported_formats == watson_core.supported_formats
    for format in  watson_core.supported_formats:  
        assert watson_core.is_file_supported(f"test.{format}")

def test_on_invalid_api():    
    with pytest.raises(Exception) as e:
        watson_core = WatsonCore(WATSON_API_KEY + "**", WATSON_REGION)
        assert e

def test_on_invalid_region():
    with pytest.raises(Exception) as e:
        watson_core = WatsonCore(WATSON_API_KEY, WATSON_REGION + "__")
        assert e 
        
@pytest.mark.parametrize("inpath, outpath", [(AUDIO_INPUT[1], OUT_PATH)])
def test_convert_to_opus(inpath, outpath):
    watson = WatsonCore(WATSON_API_KEY, WATSON_REGION)
    assert watson._convert_to_opus(inpath, outpath)

@pytest.mark.parametrize(
    "inpath, outpath", [
                        (AUDIO_INPUT[2], OUT_PATH)])
def test_watson(inpath, outpath):
    watson = Watson(WATSON_API_KEY, WATSON_REGION)
    assert watson.supported_formats == MediaHandler().supported_formats
    for format in  watson.supported_formats:  
        assert watson.is_file_supported(f"test.{format}")
    assert not watson.was_transcription_successful()
    watson.transcribe(inpath, 
                      outpath,
                      WATSON_BASE_LANG_MODEL, 
                      WATSON_LANG_CUSTOM_ID)

    

    
    