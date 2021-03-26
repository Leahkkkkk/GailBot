"""
Testing script for the engines component.
"""
# Standard library imports 
from typing import Any, Tuple, Dict, List
# Local imports 
from ..suites import TestSuite
from Src.Components.engines import WatsonCore, customWatsonCallbacks,\
        WatsonLanguageModel, WatsonAcousticModel, Engines,Utterance,\
        UtteranceAttributes
from Src.Components.engines import GoogleCore
from Src.Components.io import IO 
from Src.Components.network import Network
from Src.Components.engines.google import GoogleEngine
# Third party imports 

############################### GLOBALS #####################################
API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
LANG_CUSTOM_ID =  "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
ACOUSTIC_CUSTOM_ID = "some_valid_id "
WAV_FILE_PATH = "Test_files/Media/test2b.wav"
MP3_FILE_PATH = "Test_files/Media/sample1.mp3"
BASE_LANG_MODEL = "en-US_BroadbandModel"
REGION = "dallas"
AUDIO1 = "Test_files/Media/gettysburg.wav"
AUDIO2 = "Test_files/Media/excerpt-8-whats-your-favorite-show.mp3"

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
    watson_core = WatsonCore(Network(), IO()) 
    watson_core.set_api_key(API_KEY)
    watson_core.set_service_region("dallas")
    rc, closure = create_custom_recognize_callbacks()
    watson_core.set_recognize_callback(rc)
    watson_core.set_audio_source_path(MP3_FILE_PATH)
    watson_core.set_base_language_model("en-US_BroadbandModel")
    watson_core.recognize_using_websockets()
    return all([v for v in closure[0].values() if type(v) == bool])


#### WatsonLanguageModel tests

def watson_lm_get_language_model_valid() -> bool:
    """
    Tests:
        1. Get a model with a valid name.
    """
    resp_keys = ["name","language", "rate","url"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,"dallas")
    info = lm.get_language_model("en-US_BroadbandModel")
    return info != None and \
        all([k in info.keys() for k in resp_keys])

def watson_lm_get_language_model_invalid() -> bool:
    """
    Tests:
        1. Get a model with an invalid name
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,"dallas")
    info = lm.get_language_model("en-US_Broadband")
    return info == None

def watson_lm_get_custom_language_model_valid() -> bool:
    """
    Tests:
        1. Get info on a valid custom model ID.
    """
    resp_keys = [
        "customization_id", "created", "updated","language", "dialect", 
        "versions", "name", "description", "base_model_name", "status",
        "progress","owner"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,"dallas") 
    info = lm.get_custom_language_model(LANG_CUSTOM_ID)
    return info != None and \
        all([k in info.keys() for k in resp_keys])

def watson_lm_get_custom_language_model_invalid() -> bool:
    """
    Tests:
        1. Attempt to get info. with an invalid custom model ID.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,"dallas") 
    info = lm.get_custom_language_model("invalid")
    return info == None 

def watson_lm_get_custom_model_corpora() -> bool:
    """
    Tests:
        1. Get the corpora for a valid custom language model.
        2. Get the corpora for an invalid id.
    """
    resp_keys = ["name", "out_of_vocabulary_words", "total_words","status"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY,"dallas") 
    resp = lm.get_custom_model_corpora(LANG_CUSTOM_ID)
    return len(resp) > 0 and \
        all([k in resp[0].keys() for k in resp_keys]) and \
        lm.get_custom_model_corpora("invalid") == None

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
    # s1 = engine.configure(
    #     api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH, 
    #     base_model_name=BASE_LANG_MODEL)
    # print(s1)
    #utterances = engine.transcribe()
    s2 = engine.configure(
        api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH, 
        base_model_name=BASE_LANG_MODEL)
    print(s2)
    utterances = engine.transcribe()
    # for utterance in utterances:
    #     label = utterance.get(UtteranceAttributes.speaker_label)[1]
    #     start_time = utterance.get(UtteranceAttributes.start_time)[1]
    #     end_time = utterance.get(UtteranceAttributes.end_time)[1]
    #     transcript = utterance.get(UtteranceAttributes.transcript)[1]
    #     print("{}: {} {}_{}".format(label,transcript,start_time,end_time))  
    # print(len(utterances))      
    
def watson_engine_transcribe_invalid() -> bool:
    """
    Tests:
        1. Attempt to transcribe with invalid configurations.
        2. Attempt to transcribe without configuring first. 
    """
    engine = WatsonEngine(IO(), Network())

# Google Core     

# Google Engine
def google_transcribe() -> bool:
    engine = GoogleEngine(IO())
    engine.configure(AUDIO1, 22050, 1)
    response = engine.transcribe()

    # for utterance in response:
    #     label = utterance.get(UtteranceAttributes.speaker_label)[1]
    #     start_time = utterance.get(UtteranceAttributes.start_time)[1]
    #     end_time = utterance.get(UtteranceAttributes.end_time)[1]
    #     transcript = utterance.get(UtteranceAttributes.transcript)[1]
    #     print("{}: {} {}_{}".format(label,transcript,start_time,end_time))  
    # print(len(response))  

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

    ### GoogleCore tests
    

    ### GoogleEngine tests
    suite.add_test("google_transcribe", (), True, True, 
        google_transcribe)
    return suite 





