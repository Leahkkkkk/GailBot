
# Local imports
from Src.components.engines import GoogleCore
from Src.components.io import IO
from Tests.engines.vardefs import *

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_google_core_set_get_audio_path_valid_mp3() -> None:
    """
    Tests:
        1. Sets and gets valid MP3 path.
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(AUDIO2)
    assert success and core.get_audio_path() == AUDIO2


def test_google_core_set_get_audio_path_valid_wav() -> None:
    """
    Tests:
        1. Sets and gets valid wav path.
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(AUDIO1)
    assert success and core.get_audio_path() == AUDIO1


def test_google_core_set_get_audio_path_non_audio() -> None:
    """
    Tests:
        1. Sets and gets invalid non-audio path (gif).
    """
    core = GoogleCore(IO())
    success = core.set_audio_path(NON_AUDIO)
    assert not success and core.get_audio_path() == None


def test_google_core_set_get_audio_path_unsupported() -> None:
    """
    Tests:
        1. Sets and gets invalid unsupported audio file
    """
    pass


def test_google_core_set_get_sample_rate_hertz_valid() -> None:
    """
    Tests:
        1. Sets and gets valid sample rate
    """
    core = GoogleCore(IO())
    success = core.set_sample_rate_hertz(16000)
    assert success and core.get_sample_rate_hertz() == 16000


def test_google_core_set_get_sample_rate_hertz_invalid() -> None:
    """
    Tests:
        1. Sets and gets invalid sample rate
    """
    core = GoogleCore(IO())
    success = core.set_sample_rate_hertz(-10)
    assert not success and core.get_sample_rate_hertz() == None


def test_google_core_set_get_speaker_count_valid() -> None:
    """
    Tests:
        1. Sets and gets valid speaker count
    """
    core = GoogleCore(IO())
    success = core.set_diarization_speaker_count(1)
    assert success and core.get_diarization_speaker_count() == 1


def test_google_core_set_get_speaker_count_invalid() -> None:
    """
    Tests:
        1. Sets and gets invalid speaker count
    """
    core = GoogleCore(IO())
    success = core.set_diarization_speaker_count(0)
    assert not success and core.get_diarization_speaker_count() == None


def test_google_core_get_supported_audio_formats() -> None:
    """
    Tests:
        1. Gets supported audio formats and confirms correct formats returned
    """
    core = GoogleCore(IO())
    formats = core.get_supported_audio_formats()
    assert formats == ["flac", "mp3", "wav"]


def test_google_core_get_supported_language_codes() -> None:
    """
    Tests:
        1. Gets supported languages and confirms correct languages returned
    """
    core = GoogleCore(IO())
    languages = core.get_supported_language_codes()
    assert languages == ["english"]


def test_google_core_reset_configurations() -> None:
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
    assert success and is_set and is_reset


def test_google_core_transcribe() -> None:
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
