from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Any, Union
import toml


@dataclass
class WhisperTranscribeConfig(DataclassFromDict):
    remove_punctuation_from_words : bool = field_from_dict()
    compute_word_confidence : bool = field_from_dict()
    include_punctuation_in_confidence : bool = field_from_dict()
    refine_whisper_precision : bool = field_from_dict()
    min_word_duration : float = field_from_dict()
    plot_word_alignment : bool = field_from_dict()
    naive_approach : bool = field_from_dict()
    compression_ratio_threshold : float = field_from_dict()
    logprob_threshold : Union[float, int] = field_from_dict()
    no_speech_threshold : float = field_from_dict()
    condition_on_previous_text : bool = field_from_dict()
    verbose : bool = field_from_dict()
    best_of : int = field_from_dict(default=None)
    beam_size : int = field_from_dict(default=None)
    patience : float = field_from_dict(default=None)
    length_penalty : float  = field_from_dict(default=None)
    fp16 : Any = field_from_dict(default=None)

@dataclass
class WhisperConfig(DataclassFromDict):
    engine_name : str = field_from_dict()
    model_name : str =  field_from_dict()
    transcribe_configs : WhisperTranscribeConfig = field_from_dict()

def load_whisper_config(path: str):
    """Loads data from the Watson engine configuration

    Args:
        path (str) : path to the toml file to load
    """
    d = toml.load(path)
    return WhisperConfig.from_dict(d["whisper"])