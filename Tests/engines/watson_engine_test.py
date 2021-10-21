
# Local imports
from Src.components.engines import WatsonEngine, Utterance, UtteranceAttributes
from Src.components.io import IO
from Src.components.network import Network
from Tests.engines.vardefs import *

############################### GLOBALS #####################################


########################## TEST DEFINITIONS ##################################


def test_watson_engine_configure_valid() -> None:
    """
    Tests:
        1. Configure WatsonEngine with valid attributes.
    """
    engine = WatsonEngine(IO(), Network())
    assert engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL) and \
        engine.configure(
            workspace_directory_path=WORKSPACE_DIR_PATH,
            api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
            base_model_name=BASE_LANG_MODEL,
            language_customization_id=LANG_CUSTOM_ID)


def test_watson_engine_configure_invalid() -> None:
    """
    Tests:
        1. Configure WatsonEngine with invalid attributes.
    """
    engine = WatsonEngine(IO(), Network())
    s1 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key="invalid", region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    s2 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region="invalid", audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    s3 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name="invalid")
    s4 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL,
        language_customization_id="invalid")
    s5 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path="invalid",
        base_model_name=BASE_LANG_MODEL)
    assert not s1 and not s2 and not s3 and not s4 and not s5


def test_watson_engine_get_configurations() -> None:
    """
    Compare the configurations agains the inputs
    """
    engine = WatsonEngine(IO(), Network())
    resp_keys = ["api_key", "region", "audio_path", "base_model_name",
                 "language_customization_id", "acoustic_customization_id"]
    engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    configs = engine.get_configurations()
    assert all([k in configs.keys() for k in resp_keys]) and \
        configs["api_key"] == API_KEY and \
        configs["region"] == REGION and \
        configs["base_model_name"] == BASE_LANG_MODEL


def test_watson_engine_get_engine_name() -> None:
    """
    Tests:
        1. Obtain the name and compare it.
    """
    engine = WatsonEngine(IO(), Network())
    assert engine.get_engine_name() == "watson"


def test_watson_engine_get_supported_formats() -> None:
    """
    Tests:
        1. Ensure the correct return type
    """
    engine = WatsonEngine(IO(), Network())
    formats = engine.get_supported_audio_formats()
    assert len(formats) > 0


def test_watson_engine_was_transcription_successful_valid() -> None:
    """
    Tests:
        1. Determine if the transcription was successful after transcribing.
    """
    engine = WatsonEngine(IO(), Network())
    assert engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    engine.transcribe()
    assert engine.was_transcription_successful()


def test_watson_engine_was_transcription_successful_invalid() -> None:
    """
    Tests:
        1. Check if transcription successful before configuration.
        2. Check if successful after clearing configurations.
    """
    engine = WatsonEngine(IO(), Network())
    assert not engine.was_transcription_successful()
    assert engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=MP3_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    assert not engine.was_transcription_successful()


def test_watson_engine_is_file_supported() -> None:
    """
    Tests:
        1. Ensure mp3 file is supported.
        2. Ensure wav file is supported.
        3. Ensure does not work with invalid file name.
    """
    engine = WatsonEngine(IO(), Network())
    assert engine.is_file_supported(MP3_FILE_PATH) and  \
        not engine.is_file_supported("invalid")


def test_watson_engine_transcribe_valid() -> None:
    """
    Tests:
        1. Transcribe a file with valid configurations
    """
    engine = WatsonEngine(IO(), Network())
    s1 = engine.configure(
        workspace_directory_path=WORKSPACE_DIR_PATH,
        api_key=API_KEY, region=REGION, audio_path=WAV_FILE_PATH,
        base_model_name=BASE_LANG_MODEL)
    print(s1)
    utterances = engine.transcribe()
    # s2 = engine.configure(
    #     api_key = API_KEY, region = REGION, audio_path = MP3_FILE_PATH,
    #     base_model_name=BASE_LANG_MODEL)
    # print(s2)
    #utterances = engine.transcribe()
    for utterance in utterances:
        label = utterance.get(UtteranceAttributes.speaker_label)[1]
        start_time = utterance.get(UtteranceAttributes.start_time)[1]
        end_time = utterance.get(UtteranceAttributes.end_time)[1]
        transcript = utterance.get(UtteranceAttributes.transcript)[1]
        print("{}: {} {}_{}".format(label, transcript, start_time, end_time))
    print(len(utterances))

# TODO: Need to write this test!!!


def test_watson_engine_transcribe_invalid() -> None:
    """
    Tests:
        1. Attempt to transcribe with invalid configurations.
        2. Attempt to transcribe without configuring first.
    """
    engine = WatsonEngine(IO(), Network())
