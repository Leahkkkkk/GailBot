# Local imports
from Src.components.engines import GoogleEngine
from Src.components.io import IO
from Tests.engines.vardefs import *

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_google_engine_configure_valid() -> None:
    """
    Tests:
        1. Configures google engine with valid settings.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, 22050, 1)
    assert is_configured


def test_google_engine_configure_invalid() -> None:
    """
    Tests:
        1. Configures google engine with invalid settings.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, -10, 1)
    assert not is_configured


def test_google_engine_get_configurations_unset() -> None:
    """
    Tests:
        1. Gets unset configurations and confirms all inputs set to None.
    """
    engine = GoogleEngine(IO())
    config = engine.get_configurations()
    assert config == {
        "audio_path": None,
        "sample_rate_hertz": None,
        "diarization_speaker_count": None
    }


def test_google_engine_get_configurations_set() -> None:
    """
    Tests:
        1. Configures valid settings.
        2. Gets conigurations and confirms set was successful.
    """
    engine = GoogleEngine(IO())
    is_configured = engine.configure(AUDIO1, 22050, 1)
    config = engine.get_configurations()
    assert config == {
        "audio_path": AUDIO1,
        "sample_rate_hertz": 22050,
        "diarization_speaker_count": 1
    } and is_configured


def test_google_engine_get_name() -> None:
    """
    Tests:
        1. Gets engine name
    """
    engine = GoogleEngine(IO())
    assert engine.get_engine_name() == "google"


def test_google_engine_get_supported_audio_formats() -> None:
    """
    Tests:
        1. Gets supported audio formats.
    """
    engine = GoogleEngine(IO())
    assert engine.get_supported_formats() == ["flac", "mp3", "wav"]


def test_google_engine_is_file_supported_wav() -> None:
    """
    Tests:
        1. Confirms wav extension file is a supported file
    """
    engine = GoogleEngine(IO())
    assert engine.is_file_supported(AUDIO1)


def test_google_engine_is_file_supported_non_audio() -> None:
    """
    Tests:
        1. Confirms non-audio file is an unsupported file
    """
    engine = GoogleEngine(IO())
    assert not engine.is_file_supported(NON_AUDIO)


def test_google_engine_transcribe() -> None:
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


def test_google_engine_was_transcription_successful() -> None:
    """
    Tests:
        1. Ensure that the transcription raises exception for now.
    """
    try:
        engine = GoogleEngine(IO())
        engine.was_transcription_successful()
        assert False
    except:
        assert True
