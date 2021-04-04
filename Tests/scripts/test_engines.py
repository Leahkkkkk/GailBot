"""
Testing script for the engines component.
"""
# Standard library imports
from Src.Components.engines.watson.watson import WatsonEngine
from typing import Any, Tuple, Dict, List
# Local imports
from ..suites import TestSuite
from Src.Components.engines import WatsonCore, customWatsonCallbacks,\
        WatsonLanguageModel, WatsonAcousticModel, Engines,Utterance,\
        UtteranceAttributes

from Src.Components.engines.google import GoogleCore, GoogleEngine
from Src.Components.io import IO
from Src.Components.network import Network
# Third party imports

############################### GLOBALS #####################################
API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
LANG_CUSTOM_ID =  "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
ACOUSTIC_CUSTOM_ID = "some_valid_id"
WAV_FILE_PATH = "Test_files/Media/test2b.wav"
MP3_FILE_PATH = "Test_files/Media/sample1.mp3"
BASE_LANG_MODEL = "en-US_BroadbandModel"
REGION = "dallas"

AUDIO1 = "Test_files/Media/gettysburg.wav"
AUDIO2 = "Test_files/Media/excerpt-8-whats-your-favorite-show.mp3"

NON_AUDIO = "Test_files/Media/cat.gif"


########################## TEST DEFINITIONS ##################################

#### Custom callbacks for the websocket connection

def on_transcription(closure : List, transcript : Any) -> None:
    """
    Called after the service returns the final result for the transcription.
    """
    closure[0]["transcript"] = transcript
    closure[0]["on_transcription"] = True

def on_connected(closure : List) -> None:
    """
    Called when a Websocket connection was made
    """
    closure[0]["on_connected"] = True

def on_error(closure : List, error : Any) -> None:
    """
    Called when there is an error in the Websocket connection.
    """
    closure[0]["on_error_error"] = error
    closure[0]["on_error"] = True

def on_inactivity_timeout(closure : List, error : Any) -> None:
    """
    Called when there is an inactivity timeout.
    """
    closure[0]["on_inactivity_timeout_error"] = error
    closure[0]["on_inactivity_timeout"] = True

def on_listening(closure : List) -> None:
    """
    Called when the service is listening for audio.
    """
    closure[0]["on_listening"] = True

def on_hypothesis(closure : List, hypothesis : Any) -> None:
    """
    Called when an interim result is received.
    """
    closure[0]["hypothesis"] = hypothesis
    closure[0]["on_hypothesis"] = True

def on_data(closure : List, data : Any) -> None:
    """
    Called when the service returns results. The data is returned unparsed.
    """
    closure[0]["on_data"] = True
    closure[0]["data"] = data

def on_close(closure : List) -> None:
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
    return (cb,closure)

#### WatsonCore tests

def watson_core_set_api_key_valid() -> bool:
    """
    Tests:
        1. Set a valid api key
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_api_key(API_KEY)

def watson_core_set_api_key_invalid() -> bool:
    """
    Tests:
        1. Set an invalid api key.
    """
    watson_core = WatsonCore(Network(), IO())
    return not watson_core.set_api_key("invalid")

def watson_core_set_service_region_valid() -> bool:
    """
    Tests:
        1. Set a valid service region.
        2. Set a valid service region in uppercase letters.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_service_region("dallas") and \
        watson_core.set_service_region("DALLAS") and \
        watson_core.set_service_region("seoul")

def watson_core_set_service_region_invalid() -> bool:
    """
    Tests:
        1. Set an invalid service region.
    """
    watson_core = WatsonCore(Network(), IO())
    return not watson_core.set_service_region("dalls") and \
        not watson_core.set_service_region("invalid")

def watson_core_set_recognize_callback() -> bool:
    """
    Tests:
        1. Set a recognize callback object.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_recognize_callback(customWatsonCallbacks([{}]))

def watson_core_set_audio_source_path_valid() -> bool:
    """
    Tests:
        1. Set a valid path to the source audio file.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_audio_source_path(WAV_FILE_PATH)

def watson_core_set_audio_source_path_invalid() -> bool:
    """
    Tests:
        1. Set an invalid path for the source audio file.
    """
    watson_core = WatsonCore(Network(), IO())
    return not watson_core.set_audio_source_path("invalid/")

def watson_core_set_base_language_model() -> bool:
    """
    Tests:
        1. Set a supported base language model.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_base_language_model("en-US_BroadbandModel")

def watson_core_set_language_customization_id() -> bool:
    """
    Tests:
        1. Set a language customization id.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_language_customization_id(LANG_CUSTOM_ID)

def watson_core_set_acoustic_customization_id() -> bool:
    """
    Tests:
        1. Set an acoustic customization id.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)

def watson_core_get_api_key() -> bool:
    """
    Tests:
        1. Obtain a valid api key that was set.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_api_key(API_KEY)
    return watson_core.get_api_key() == API_KEY

def watson_core_get_service_region() -> bool:
    """
    Tests:
        1. Obtain a valid service region that was set.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_service_region("dallas")
    return watson_core.get_service_region() == "dallas"

def watson_core_get_audio_source_path() -> bool:
    """
    Tests:
        1. Obtain the valid audio source that was set.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_audio_source_path(WAV_FILE_PATH)
    return watson_core.get_audio_source_path() == WAV_FILE_PATH

def watson_core_get_selected_base_model() -> bool:
    """
    Tests:
        1. Obtain the previously set base language model.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_base_language_model("en-US_BroadbandModel")
    return watson_core.get_selected_base_model() == "en-US_BroadbandModel"

def watson_core_get_language_customization_id() -> bool:
    """
    Tests:
        1. Obtain the previously set language customization id.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_language_customization_id(LANG_CUSTOM_ID)
    return watson_core.get_language_customization_id() == LANG_CUSTOM_ID

def watson_core_get_acoustic_customization_id() -> bool:
    """
    Tests:
        1. Obtain the previously set acoustic customization id.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)
    return watson_core.get_acoustic_customization_id() == ACOUSTIC_CUSTOM_ID

def watson_core_get_supported_regions() -> bool:
    """
    Tests:
        1. Obtain the list of supported regions.
    """
    watson_core = WatsonCore(Network(), IO())
    return watson_core.get_supported_regions() == [
        "dallas", "washington", "frankfurt", "sydney", "tokyo", "london",
        "seoul"]

def watson_core_get_supported_audio_formats() -> bool:
    """
    Tests:
        1. Obtain the list of supported audio formats.
    """
    watson_core = WatsonCore(Network(), IO())
    return len(watson_core.get_supported_audio_formats()) > 0

def watson_core_reset_configurations() -> bool:
    """
    Test:
        1. Reset the configurations of a  WatsonCore object that was previously
        configured and check to make sure that all attributes have been reset.
    """
    watson_core = WatsonCore(Network(), IO())
    watson_core.set_api_key(API_KEY)
    watson_core.set_service_region("dallas")
    watson_core.set_recognize_callback(customWatsonCallbacks([{}]))
    watson_core.set_audio_source_path(WAV_FILE_PATH)
    watson_core.set_base_language_model("en-US_BroadbandModel")
    watson_core.set_language_customization_id(LANG_CUSTOM_ID)
    watson_core.set_acoustic_customization_id(ACOUSTIC_CUSTOM_ID)
    watson_core.reset_configurations()
    return watson_core.get_api_key() == None and \
        watson_core.get_service_region() == None and \
        watson_core.get_audio_source_path() == None and \
        watson_core.get_selected_base_model() == None and \
        watson_core.get_language_customization_id() == None and \
        watson_core.get_acoustic_customization_id() == None

def watson_core_recognize_using_websockets() -> bool:
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
    return all([v for v in closure[0].values() if type(v) == bool])


#### WatsonLanguageModel tests

def watson_lm_get_base_model() -> bool:
    """
    Tests:
        1. Get a valid base model.
        2. Get an invalid base model.
    """
    resp_keys = [
        "name", "language","rate", "url","supported_features","description"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    resp = lm.get_base_model(BASE_LANG_MODEL)
    return resp != None and \
        all([key in resp_keys for key in resp.keys()]) and \
        lm.get_base_model("invalid") == None

def watson_lm_get_base_models() -> bool:
    """
    Tests:
        1. Make sure there is at least one base model.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    resp = lm.get_base_models()
    return resp != None and len(resp) > 0

def watson_lm_get_custom_model() -> bool:
    """
    Tests:
        1. Obtain a valid model and check return keys
        2. Ensure invalid key returns None.
    """
    resp_keys = [
        "customization_id", "created", "updated","language", "dialect",
        "versions", "owner", "name", "description", "base_model_name", "status",
        "progress"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    resp = lm.get_custom_model(LANG_CUSTOM_ID)
    return resp != None and \
        all([key in resp_keys for key in resp.keys()]) and \
        lm.get_custom_model("invalid") == None


def watson_lm_get_custom_models() -> bool:
    """
    Tests:
        1. Ensure that all the ids for the custom model returned and valid ids.
    """
    resp_keys = [
        "customization_id", "created", "updated","language", "dialect",
        "versions", "owner", "name", "description", "base_model_name", "status",
        "progress"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    models = lm.get_custom_models()
    if models == None:
        return False
    for custom_id in models.values():
        resp = lm.get_custom_model(custom_id)
        if resp == None or \
                not all([key in resp_keys for key in resp.keys()]):
            return False
    return True

def watson_lm_delete_custom_model() -> bool:
    """
    Tests:
        1. Create a model and delete it.
        2. Delete a model that does not exist
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    s1 = lm.create_custom_model("test_1",BASE_LANG_MODEL,"test model 1")
    models = lm.get_custom_models()
    return s1 and lm.delete_custom_model(models["test_1"]) and \
        not lm.delete_custom_model("invalid id")

def watson_lm_create_custom_model() -> bool:
    """
    Tests:
        1. Create a new model with a valid base model.
        2. Create a model with an invalid base model.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    models = lm.get_custom_models()
    s1 = lm.create_custom_model("test_1",BASE_LANG_MODEL,"test model 1")
    s2 = lm.create_custom_model("test_2","invalid base model","test model 1")
    models = lm.get_custom_models()
    return s1 and not s2 and \
        lm.delete_custom_model(models["test_1"])

def watson_lm_train_custom_model() -> bool:
    """
    Tests:
        1. Create a model, add a resource and train it.
        2. Create a model and train it without adding a resource.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name,BASE_LANG_MODEL,"test model 1")
    models = lm.get_custom_models()
    s1 = lm.add_custom_words(models[model_name],["pie"])
    s2 = lm.train_custom_model(models[model_name])
    s3 = lm.delete_custom_model(models[model_name])
    print(s1,s2,s3)
    return s1 and s2 and s3

def watson_lm_reset_custom_model() -> bool:
    """
    Tests:
        1. Reset a model that has already been trained.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name,BASE_LANG_MODEL,"test model 1")
    models = lm.get_custom_models()
    return lm.reset_custom_model(models[model_name]) and \
        lm.delete_custom_model(models[model_name])

def watson_lm_upgrade_custom_model() -> bool:
    """
    Tests:
        1. Upgrade the base model of a custom model that has been created.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name,BASE_LANG_MODEL,"test model 1")
    models = lm.get_custom_models()
    return lm.upgrade_custom_model(models[model_name]) and \
        lm.delete_custom_model(models[model_name])

def watson_lm_get_corpora() -> bool:
    """
    Tests:
        1. Obtain the corpora of a model that has already been trained.
        2. Obtain the corpora of a model that has not been trained.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name,BASE_LANG_MODEL,"test model 1")
    models = lm.get_custom_models()
    return lm.get_corpora(LANG_CUSTOM_ID) != None and \
        lm.get_corpora(models[model_name]) != None and \
        lm.delete_custom_model(models[model_name])

def watson_lm_add_corpus() -> bool:
    """
    Tests:
        1.
    """
    pass

def watson_lm_delete_corpus() -> bool:
    pass

def watson_lm_get_corpus() -> bool:
    pass

def watson_lm_get_custom_words() -> bool:
    pass

def watson_lm_add_custom_words() -> bool:
    pass

def watson_lm_delete_custom_word() -> bool:
    pass

def watson_lm_get_custom_grammars() -> bool:
    pass

def watson_lm_get_custom_grammar() -> bool:
    pass

def watson_lm_add_custom_grammar() -> bool:
    pass

def watson_lm_delete_custom_grammar() -> bool:
    pass

#### WatsonAcousticModel tests

def watson_am_get_custom_models() -> bool:
    pass

def watson_am_get_custom_model() -> bool:
    pass

def watson_am_create_custom_model() -> bool:
    pass

def watson_am_delete_custom_model() -> bool:
    pass

def watson_am_train_custom_model() -> bool:
    pass

def watson_am_reset_custom_model() -> bool:
    pass

def watson_am_upgrade_custom_model() -> bool:
    pass

def watson_am_get_custom_audio_resources() -> bool:
    pass

def watson_am_get_custom_audio_resource() -> bool:
    pass

def watson_am_add_custom_audio_resource() -> bool:
    pass

def watson_am_delete_custom_audio_resource() -> bool:
    pass


#### WatsonEngine tests

def watson_engine_configure_valid() -> bool:
    """
    Tests:
        1. Configure WatsonEngine with valid attributes.
    """
    engine = WatsonEngine(IO(), Network())
    return engine.configure(
            api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
            base_model_name=BASE_LANG_MODEL) and \
        engine.configure(
            api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
            base_model_name=BASE_LANG_MODEL,
            language_customization_id=LANG_CUSTOM_ID)

def watson_engine_configure_invalid() -> bool:
    """
    Tests:
        1. Configure WatsonEngine with invalid attributes.
    """
    engine = WatsonEngine(IO(), Network())
    s1 = engine.configure(
        api_key = "invalid", region = REGION, audio_path = MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    s2 = engine.configure(
        api_key = API_KEY, region = "invalid", audio_path = MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    s3 = engine.configure(
        api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
        base_model_name="invalid")
    s4 = engine.configure(
        api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL,
        language_customization_id="invalid")
    s5 = engine.configure(
        api_key = API_KEY, region = REGION, audio_path = "invalid",
        base_model_name=BASE_LANG_MODEL)
    return not s1 and not s2 and not s3 and not s4 and not s5

def watson_engine_get_configurations() -> bool:
    """
    Compare the configurations agains the inputs
    """
    engine = WatsonEngine(IO(), Network())
    resp_keys = ["api_key","region","audio_path","base_model_name",
        "language_customization_id","acoustic_customization_id"]
    engine.configure(
        api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    configs = engine.get_configurations()
    return all([k in configs.keys() for k in resp_keys]) and \
        configs["api_key"] == API_KEY and \
        configs["region"] == REGION and \
        configs["base_model_name"] == BASE_LANG_MODEL

def watson_engine_get_engine_name() -> bool:
    """
    Tests:
        1. Obtain the name and compare it.
    """
    engine = WatsonEngine(IO(), Network())
    return engine.get_engine_name() == "watson"

def watson_engine_get_supported_formats() -> bool:
    """
    Tests:
        1. Ensure the correct return type
    """
    engine = WatsonEngine(IO(), Network())
    formats = engine.get_supported_audio_formats()
    return len(formats) > 0

def watson_engine_is_file_supported() -> bool:
    """
    Tests:
        1. Ensure mp3 file is supported.
        2. Ensure wav file is supported.
        3. Ensure does not work with invalid file name.
    """
    engine = WatsonEngine(IO(), Network())
    return engine.is_file_supported(MP3_FILE_PATH) and  \
        not engine.is_file_supported("invalid")

def watson_engine_transcribe_valid() -> bool:
    """
    Tests:
        1. Transcribe a file with valid configurations
    """
    engine = WatsonEngine(IO(), Network())
    s1 = engine.configure(
        api_key = API_KEY, region = REGION, audio_path = WAV_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    print(s1)
    utterances = engine.transcribe()
    # s2 = engine.configure(
    #     api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
    #     base_model_name=BASE_LANG_MODEL)
    # print(s2)
    utterances = engine.transcribe()
    for utterance in utterances:
        label = utterance.get(UtteranceAttributes.speaker_label)[1]
        start_time = utterance.get(UtteranceAttributes.start_time)[1]
        end_time = utterance.get(UtteranceAttributes.end_time)[1]
        transcript = utterance.get(UtteranceAttributes.transcript)[1]
        print("{}: {} {}_{}".format(label,transcript,start_time,end_time))
    print(len(utterances))

def watson_engine_transcribe_invalid() -> bool:
    """
    Tests:
        1. Attempt to transcribe with invalid configurations.
        2. Attempt to transcribe without configuring first.
    """
    engine = WatsonEngine(IO(), Network())

# Google Core

def google_core_set_get_audio_path_valid_mp3() -> bool:
    """
    Tests:
        1. Sets and gets valid MP3 path.
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(AUDIO2)
    return success and core.get_audio_path() == AUDIO2

def google_core_set_get_audio_path_valid_wav() -> bool:
    """
    Tests:
        1. Sets and gets valid wav path.
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(AUDIO1)
    return success and core.get_audio_path() == AUDIO1

def google_core_set_get_audio_path_non_audio() -> bool:
    """
    Tests:
        1. Sets and gets invalid non-audio path (gif).
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(NON_AUDIO)
    return not success and core.get_audio_path() == None

def google_core_set_get_audio_path_unsupported() -> bool:
    """
    Tests:
        1. Sets and gets invalid unsupported audio file
    """
    pass

def google_core_set_get_sample_rate_hertz_valid() -> bool:
    """
    Tests:
        1. Sets and gets valid sample rate
    """
    core = GoogleCore(IO())
    success = core.set_sample_rate_hertz(16000)
    return success and core.get_sample_rate_hertz() == 16000

def google_core_set_get_sample_rate_hertz_invalid() -> bool:
    """
    Tests:
        1. Sets and gets invalid sample rate
    """
    core = GoogleCore(IO())
    success = core.set_sample_rate_hertz(-10)
    return not success and core.get_sample_rate_hertz() == None

def google_core_set_get_speaker_count_valid() -> bool:
    """
    Tests:
        1. Sets and gets valid speaker count
    """
    core = GoogleCore(IO())
    success = core.set_diarization_speaker_count(1)
    return success and core.get_diarization_speaker_count() == 1

def google_core_set_get_speaker_count_invalid() -> bool:
    """
    Tests:
        1. Sets and gets invalid speaker count
    """
    core = GoogleCore(IO())
    success = core.set_diarization_speaker_count(0)
    return not success and core.get_diarization_speaker_count() == None

def google_core_get_supported_audio_formats() -> bool:
    """
    Tests:
        1. Gets supported audio formats and confirms correct formats returned
    """
    core = GoogleCore(IO())
    formats = core.get_supported_audio_formats()
    print("formats:", formats)
    return formats == ["flac", "mp3", "wav"]

def google_core_get_supported_language_codes() -> bool:
    """
    Tests:
        1. Gets supported languages and confirms correct languages returned
    """
    core = GoogleCore(IO())
    languages = core.get_supported_language_codes()
    print("language code:", languages)
    return languages == ["english"]

def google_core_reset_configurations() -> bool:
    """
    Tests:
        1. Sets Google core
        2. Resets Google core
    """
    core = GoogleCore(IO())
    core.set_audio_path(AUDIO2)
    core.set_diarization_speaker_count(1)
    core.set_sample_rate_hertz(22050)
    is_set = core.get_audio_path() == AUDIO2 and core.get_sample_rate_hertz() == 22050 and\
        core.get_diarization_speaker_count() == 1
    success = core.reset_configurations()
    is_reset = core.get_audio_path() == None and core.get_diarization_speaker_count() == None and\
        core.get_sample_rate_hertz() == None

    return success and is_set and is_reset

def google_core_transcribe() -> bool:
    """
    Tests:
        1. Sets Google core
        2. Transcribes from core and checks utterances
    """
    core = GoogleCore(IO())
    core.set_audio_path(AUDIO1)
    core.set_diarization_speaker_count(1)
    core.set_sample_rate_hertz(22050)
    utterances = core.transcribe_audio()

    # for utterance in utterances:
    #     label = utterance.get(UtteranceAttributes.speaker_label)[1]
    #     start_time = utterance.get(UtteranceAttributes.start_time)[1]
    #     end_time = utterance.get(UtteranceAttributes.end_time)[1]
    #     transcript = utterance.get(UtteranceAttributes.transcript)[1]
    #     print("{}: {} {}_{}".format(label,transcript,start_time,end_time))
    # print(len(utterances))

    return True

# Google Engine
def google_engine_configure_valid() -> bool:
    """
    Tests:
        1. Configures google engine with valid settings.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, 22050, 1)
    return is_configured

def google_engine_configure_invalid() -> bool:
    """
    Tests:
        1. Configures google engine with invalid settings.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, -10, 1)
    return not is_configured

def google_engine_get_configurations_unset() -> bool:
    """
    Tests:
        1. Gets unset configurations and confirms all inputs set to None.
    """
    engine = GoogleEngine(IO())
    config = engine.get_configurations()
    return config == {
            "audio_path" : None,
            "sample_rate_hertz" : None,
            "diarization_speaker_count" : None
            }

def google_engine_get_configurations_set() -> bool:
    """
    Tests:
        1. Configures valid settings.
        2. Gets conigurations and confirms set was successful.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, 22050, 1)
    config = engine.get_configurations()
    return config == {
            "audio_path" : AUDIO1,
            "sample_rate_hertz" : 22050,
            "diarization_speaker_count" : 1
            } and is_configured

def google_engine_get_name() -> bool:
    """
    Tests:
        1. Gets engine name
    """
    engine = GoogleEngine(IO())
    return engine.get_engine_name() == "google"

def google_engine_get_supported_audio_formats() -> bool:
    """
    Tests:
        1. Gets supported audio formats.
    """
    engine = GoogleEngine(IO())
    return engine.get_supported_formats() == ["flac", "mp3", "wav"]

def google_engine_is_file_supported_wav() -> bool:
    """
    Tests:
        1. Confirms wav extension file is a supported file
    """
    engine = GoogleEngine(IO())
    return engine.is_file_supported(AUDIO1) == True

def google_engine_is_file_supported_non_audio() -> bool:
    """
    Tests:
        1. Confirms non-audio file is an unsupported file
    """
    engine = GoogleEngine(IO())
    return engine.is_file_supported(NON_AUDIO) == False

def google_engine_transcribe() -> bool:
    """
    Tests:
        1. Configures core from engine.
        2. Runs transcription from engine
    """
    engine = GoogleEngine(IO())
    engine.configure(AUDIO1, 22050, 1)
    utterances = engine.transcribe()

    # for utterance in utterances:
    #     label = utterance.get(UtteranceAttributes.speaker_label)[1]
    #     start_time = utterance.get(UtteranceAttributes.start_time)[1]
    #     end_time = utterance.get(UtteranceAttributes.end_time)[1]
    #     transcript = utterance.get(UtteranceAttributes.transcript)[1]
    #     print("{}: {} {}_{}".format(label,transcript,start_time,end_time))
    # print(len(utterances))

    return True

####################### TEST SUITE DEFINITION ################################

def define_engines_test_suite() -> TestSuite:
    suite = TestSuite()
    ### WatsonCore tests
    # suite.add_test("watson_core_set_api_key_valid", (), True, True,
    #     watson_core_set_api_key_valid)
    # suite.add_test("watson_core_set_api_key_invalid", (), True, True,
    #     watson_core_set_api_key_invalid)
    # suite.add_test("watson_core_set_service_region_valid", (), True, True,
    #     watson_core_set_service_region_valid)
    # suite.add_test("watson_core_set_service_region_invalid", (), True, True,
    #     watson_core_set_service_region_invalid)
    # suite.add_test("watson_core_set_recognize_callback", (), True, True,
    #     watson_core_set_recognize_callback)
    # suite.add_test("watson_core_set_audio_source_path_valid", (), True, True,
    #     watson_core_set_audio_source_path_valid)
    # suite.add_test("watson_core_set_audio_source_path_invalid", (), True, True,
    #     watson_core_set_audio_source_path_invalid)
    # suite.add_test("watson_core_set_base_language_model", (), True, True,
    #     watson_core_set_base_language_model)
    # suite.add_test("watson_core_set_language_customization_id", (), True, True,
    #     watson_core_set_language_customization_id)
    # suite.add_test("watson_core_set_acoustic_customization_id", (), True, True,
    #     watson_core_set_acoustic_customization_id)
    # suite.add_test("watson_core_get_api_key", (), True, True,
    #     watson_core_get_api_key)
    # suite.add_test("watson_core_get_service_region", (), True, True,
    #     watson_core_get_service_region)
    # suite.add_test("watson_core_get_audio_source_path", (), True, True,
    #     watson_core_get_audio_source_path)
    # suite.add_test("watson_core_get_selected_base_model", (), True, True,
    #     watson_core_get_selected_base_model)
    # suite.add_test("watson_core_get_language_customization_id", (), True, True,
    #     watson_core_get_language_customization_id)
    # suite.add_test("watson_core_get_acoustic_customization_id", (), True, True,
    #     watson_core_get_acoustic_customization_id)
    # suite.add_test("watson_core_get_supported_regions", (), True, True,
    #     watson_core_get_supported_regions)
    # suite.add_test("watson_core_get_supported_audio_formats", (), True, True,
    #     watson_core_get_supported_audio_formats)
    # suite.add_test("watson_core_reset_configurations", (), True, True,
    #     watson_core_reset_configurations)
    # suite.add_test("watson_core_recognize_using_websockets", (), True, True,
    #     watson_core_recognize_using_websockets)

    ### WatsonLanguageModel tests

    # suite.add_test("watson_lm_get_base_model",(), True, True,
    #     watson_lm_get_base_model)
    # suite.add_test("watson_lm_get_base_models", (), True, True,
    #     watson_lm_get_base_models)
    # suite.add_test("watson_lm_get_custom_model",(), True, True,
    #     watson_lm_get_custom_model)
    # suite.add_test("watson_lm_get_custom_models",(), True, True,
    #     watson_lm_get_custom_models)
    # suite.add_test("watson_lm_delete_custom_model", (), True, True,
    #     watson_lm_delete_custom_model)
    # suite.add_test("watson_lm_create_custom_model", (), True, True,
    #     watson_lm_create_custom_model)
    # suite.add_test("watson_lm_train_custom_model", (), True, True,
    #     watson_lm_train_custom_model)
    # suite.add_test("watson_lm_reset_custom_model", (), True, True,
    #     watson_lm_reset_custom_model)


    # suite.add_test("watson_lm_upgrade_custom_model", (), True, True,
    #     watson_lm_upgrade_custom_model)
    # suite.add_test("watson_lm_get_corpora", (), True, True,
    #     watson_lm_get_corpora)
    # suite.add_test("watson_lm_add_corpus", (), True, True,
    #     watson_lm_add_corpus)
    # suite.add_test("watson_lm_delete_corpus", (), True, True,
    #     watson_lm_delete_corpus)
    # suite.add_test("watson_lm_get_corpus", (), True, True,
    #     watson_lm_get_corpus)
    # suite.add_test("watson_lm_get_custom_words", (), True, True,
    #     watson_lm_get_custom_words)
    # suite.add_test("watson_lm_add_custom_words", (), True, True,
    #     watson_lm_add_custom_words)
    # suite.add_test("watson_lm_delete_custom_word", (), True, True,
    #     watson_lm_delete_custom_word)
    # suite.add_test("watson_lm_get_custom_grammars", (), True, True,
    #     watson_lm_get_custom_grammars)
    # suite.add_test("watson_lm_get_custom_grammar", (), True, True,
    #     watson_lm_get_custom_grammar)
    # suite.add_test("watson_lm_add_custom_grammar", (), True, True,
    #     watson_lm_add_custom_grammar)
    # suite.add_test("watson_lm_delete_custom_grammar",(), True, True,
    #     watson_lm_delete_custom_grammar)

    # ### WatsonAcousticeModel tests

    # suite.add_test("watson_am_get_custom_models", (), True, True,
    #     watson_am_get_custom_models)
    # suite.add_test("watson_am_get_custom_model", (), True, True,
    #     watson_am_get_custom_model)
    # suite.add_test("watson_am_create_custom_model", (), True, True,
    #     watson_am_create_custom_model)
    # suite.add_test("watson_am_delete_custom_model", (), True, True,
    #     watson_am_delete_custom_model)
    # suite.add_test("watson_am_delete_custom_model", (), True, True,
    #     watson_am_delete_custom_model)
    # suite.add_test("watson_am_reset_custom_model", (), True, True,
    #     watson_am_reset_custom_model)
    # suite.add_test("watson_am_upgrade_custom_model", (), True, True,
    #     watson_am_upgrade_custom_model)
    # suite.add_test("watson_am_get_custom_audio_resources", (), True, True,
    #     watson_am_get_custom_audio_resources)
    # suite.add_test("watson_am_get_custom_audio_resource", (), True, True,
    #     watson_am_get_custom_audio_resource)
    # suite.add_test("watson_am_add_custom_audio_resource", (), True, True,
    #     watson_am_add_custom_audio_resource)
    # suite.add_test("watson_am_delete_custom_audio_resource", (), True, True,
    #     watson_am_delete_custom_audio_resource)

    #### WatsonEngine tests
    # suite.add_test("watson_engine_configure_valid", (), True, True,
    #     watson_engine_configure_valid)
    # suite.add_test("watson_engine_configure_invalid", (), True, True,
    #     watson_engine_configure_invalid)
    # suite.add_test("watson_engine_get_configurations", (), True, True,
    #     watson_engine_get_configurations)
    # suite.add_test("watson_engine_get_engine_name", (), True, True,
    #     watson_engine_get_engine_name)
    # suite.add_test("watson_engine_get_supported_formats", (), True, True,
    #     watson_engine_get_supported_formats)
    # suite.add_test("watson_engine_is_file_supported", (), True, True,
    #     watson_engine_is_file_supported)

    # suite.add_test("watson_engine_transcribe_valid", (), True, True,
    #     watson_engine_transcribe_valid)
    # suite.add_test("watson_engine_transcribe_invalid", (), True, True,
    #     watson_engine_transcribe_invalid)

    # suite.add_test("watson_core_set_api_key_valid", (), True, True,
    #     watson_core_set_api_key_valid)
    # suite.add_test("watson_core_set_api_key_invalid", (), True, True,
    #     watson_core_set_api_key_invalid)

    suite.add_test("watson_engine_transcribe_valid", (), True, True,
        watson_engine_transcribe_valid)
    # suite.add_test("watson_engine_transcribe_invalid", (), True, True,
    #     watson_engine_transcribe_invalid)


    ### GoogleCore tests
    # suite.add_test("set_get_mp3_audio_path", (), True, True,
    #     google_core_set_get_audio_path_valid_mp3)
    # suite.add_test("set_get_wav_audio_path", (), True, True,
    #     google_core_set_get_audio_path_valid_wav)
    # suite.add_test("set_get_non_audio_path", (), True, True,
    #     google_core_set_get_audio_path_non_audio)
    # suite.add_test("set_get_sample_rate_hertz_valid", (), True, True,
    #     google_core_set_get_sample_rate_hertz_valid)
    # suite.add_test("set_get_sample_rate_hertz_invalid", (), True, True,
    #     google_core_set_get_sample_rate_hertz_invalid)
    # suite.add_test("set_get_speaker_count_valid", (), True, True,
    #     google_core_set_get_speaker_count_valid)
    # suite.add_test("set_get_speaker_count_invalid", (), True, True,
    #     google_core_set_get_speaker_count_invalid)
    # suite.add_test("get_supported_audio_formats", (), True, True,
    #     google_core_get_supported_audio_formats)
    # suite.add_test("get_supported_language_codes", (), True, True,
    #     google_core_get_supported_language_codes)
    # suite.add_test("reset_configurations", (), True, True,
    #     google_core_reset_configurations)

    # suite.add_test("core_transcribe_audio", (), True, True,
    #   google_core_transcribe)


    ### GoogleEngine tests
    # suite.add_test("is_configured_valid", (), True, True,
    #     google_engine_configure_valid)
    # suite.add_test("is_configured_invalid", (), True, True,
    #     google_engine_configure_invalid)
    # suite.add_test("get_configurations_unset", (), True, True,
    #     google_engine_get_configurations_unset)
    # suite.add_test("get_configurations_set", (), True, True,
    #     google_engine_get_configurations_set)
    # suite.add_test("get_engine", (), True, True,
    #     google_engine_get_name)
    # suite.add_test("get_audio_formats", (), True, True,
    #     google_engine_get_supported_audio_formats)
    # suite.add_test("file_supported_wav", (), True, True,
    #     google_engine_is_file_supported_wav)
    # suite.add_test("file_supported_non_audio", (), True, True,
    #     google_engine_is_file_supported_non_audio)
    # suite.add_test("engine_transcribe", (), True, True,
    #     google_engine_transcribe)
    return suite





