# Standard library imports
from typing import Any, Tuple, List
# Local imports
from Src.components.io import IO
from Src.components.engines import WatsonCore, customWatsonCallbacks
from Tests.engines.vardefs import *

############################### GLOBALS #####################################

################################# SETUP ######################################

# Custom callbacks for the websocket connection


def on_transcription(closure: List, transcript: Any) -> None:
    """
    Called after the service returns the final result for the transcription.
    """
    closure[0]["transcript"] = transcript
    closure[0]["on_transcription"] = True


def on_connected(closure: List) -> None:
    """
    Called when a Websocket connection was made
    """
    closure[0]["on_connected"] = True


def on_error(closure: List, error: Any) -> None:
    """
    Called when there is an error in the Websocket connection.
    """
    closure[0]["on_error_error"] = error
    closure[0]["on_error"] = True


def on_inactivity_timeout(closure: List, error: Any) -> None:
    """
    Called when there is an inactivity timeout.
    """
    closure[0]["on_inactivity_timeout_error"] = error
    closure[0]["on_inactivity_timeout"] = True


def on_listening(closure: List) -> None:
    """
    Called when the service is listening for audio.
    """
    closure[0]["on_listening"] = True


def on_hypothesis(closure: List, hypothesis: Any) -> None:
    """
    Called when an interim result is received.
    """
    closure[0]["hypothesis"] = hypothesis
    closure[0]["on_hypothesis"] = True


def on_data(closure: List, data: Any) -> None:
    """
    Called when the service returns results. The data is returned unparsed.
    """
    closure[0]["on_data"] = True
    closure[0]["data"] = data


def on_close(closure: List) -> None:
    """
    Called when the Websocket connection is closed
    """
    closure[0]["on_close"] = True


def create_custom_recognize_callbacks() -> Tuple[customWatsonCallbacks, List]:
    """
    Create a customRecognizeCallback object with the callbacks specified as
    well as the closure, which is a dictionary wrapped in a list.
    """
    closure = [{}]
    cb = customWatsonCallbacks(closure)
    cb.set_on_transcription_callback(on_transcription)
    cb.set_on_connected_callback(on_connected)
    cb.set_on_error_callback(on_error)
    cb.set_on_inactivity_timeout(on_inactivity_timeout)
    cb.set_on_listening_callback(on_listening)
    cb.set_on_hypothesis_callback(on_hypothesis)
    cb.set_on_data_callback(on_data)
    cb.set_on_close_callback(on_close)
    return (cb, closure)


########################## TEST DEFINITIONS ##################################


def test_watson_core_set_api_key_valid() -> None:
    """
    Tests:
        1. Set a valid api key
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_api_key(API_KEY)


def test_watson_core_set_api_key_invalid() -> None:
    """
    Tests:
        1. Set an invalid api key.
    """
    watson_core = WatsonCore(IO())
    assert not watson_core.set_api_key("invalid")


def test_watson_core_set_service_region_valid() -> None:
    """
    Tests:
        1. Set a valid service region.
        2. Set a valid service region in uppercase letters.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_service_region("dallas") and \
        watson_core.set_service_region("DALLAS") and \
        watson_core.set_service_region("seoul")


def test_watson_core_set_service_region_invalid() -> None:
    """
    Tests:
        1. Set an invalid service region.
    """
    watson_core = WatsonCore(IO())
    assert not watson_core.set_service_region("dalls") and \
        not watson_core.set_service_region("invalid")


def test_watson_core_set_recognize_callback() -> None:
    """
    Tests:
        1. Set a recognize callback object.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_recognize_callback(customWatsonCallbacks([{}]))


def test_watson_core_set_audio_source_path_valid() -> None:
    """
    Tests:
        1. Set a valid path to the source audio file.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_audio_source_path(WAV_FILE_PATH)


def test_watson_core_set_audio_source_path_invalid() -> None:
    """
    Tests:
        1. Set an invalid path for the source audio file.
    """
    watson_core = WatsonCore(IO())
    assert not watson_core.set_audio_source_path("invalid/")


def test_watson_core_set_base_language_model() -> None:
    """
    Tests:
        1. Set a supported base language model.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_base_language_model("en-US_BroadbandModel")


def test_watson_core_set_language_customization_id() -> None:
    """
    Tests:
        1. Set a language customization id.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_language_customization_id(LANG_CUSTOM_ID)


def test_watson_core_set_acoustic_customization_id() -> None:
    """
    Tests:
        1. Set an acoustic customization id.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)


def test_watson_core_get_api_key() -> None:
    """
    Tests:
        1. Obtain a valid api key that was set.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_api_key(API_KEY)
    assert watson_core.get_api_key() == API_KEY


def test_watson_core_get_service_region() -> None:
    """
    Tests:
        1. Obtain a valid service region that was set.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_service_region("dallas")
    assert watson_core.get_service_region() == "dallas"


def test_watson_core_get_audio_source_path() -> None:
    """
    Tests:
        1. Obtain the valid audio source that was set.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_audio_source_path(WAV_FILE_PATH)
    assert watson_core.get_audio_source_path() == WAV_FILE_PATH


def test_watson_core_get_selected_base_model() -> None:
    """
    Tests:
        1. Obtain the previously set base language model.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_base_language_model("en-US_BroadbandModel")
    assert watson_core.get_selected_base_model() == "en-US_BroadbandModel"


def test_watson_core_get_language_customization_id() -> None:
    """
    Tests:
        1. Obtain the previously set language customization id.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_language_customization_id(LANG_CUSTOM_ID)
    assert watson_core.get_language_customization_id() == LANG_CUSTOM_ID


def test_watson_core_get_acoustic_customization_id() -> None:
    """
    Tests:
        1. Obtain the previously set acoustic customization id.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)
    assert watson_core.get_acoustic_customization_id() == ACOUSTIC_CUSTOM_ID


def test_watson_core_get_supported_regions() -> None:
    """
    Tests:
        1. Obtain the list of supported regions.
    """
    watson_core = WatsonCore(IO())
    assert watson_core.get_supported_regions() == [
        "dallas", "washington", "frankfurt", "sydney", "tokyo", "london",
        "seoul"]


def test_watson_core_get_supported_audio_formats() -> None:
    """
    Tests:
        1. Obtain the list of supported audio formats.
    """
    watson_core = WatsonCore(IO())
    assert len(watson_core.get_supported_audio_formats()) > 0


def test_watson_core_reset_configurations() -> None:
    """
    Test:
        1. Reset the configurations of a  WatsonCore object that was previously
        configured and check to make sure that all attributes have been reset.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_api_key(API_KEY)
    watson_core.set_service_region("dallas")
    watson_core.set_recognize_callback(customWatsonCallbacks([{}]))
    watson_core.set_audio_source_path(WAV_FILE_PATH)
    watson_core.set_base_language_model("en-US_BroadbandModel")
    watson_core.set_language_customization_id(LANG_CUSTOM_ID)
    watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)
    watson_core.reset_configurations()
    assert watson_core.get_api_key() == None and \
        watson_core.get_service_region() == None and \
        watson_core.get_audio_source_path() == None and \
        watson_core.get_selected_base_model() == None and \
        watson_core.get_language_customization_id() == None and \
        watson_core.get_acoustic_customization_id() == None


def test_watson_core_recognize_using_websockets() -> None:
    """
    Tests:
        1. Transcribe a valid file using the websocket connection.
    """
    watson_core = WatsonCore(IO())
    watson_core.set_api_key(API_KEY)
    watson_core.set_service_region("dallas")
    rc, closure = create_custom_recognize_callbacks()
    watson_core.set_recognize_callback(rc)
    watson_core.set_audio_source_path(MP3_FILE_PATH)
    watson_core.set_base_language_model("en-US_BroadbandModel")
    watson_core.recognize_using_websockets()
    assert all([v for v in closure[0].values() if type(v) == bool])
