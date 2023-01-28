from dataclasses import dataclass 
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict 
import os 

from gailbot.configs.conf_path import ENGINE_PATH, CONFIG_ROOT

import toml 

@dataclass
class WatsonRegionsUris(DataclassFromDict):
    dallas: str = field_from_dict()
    washington: str = field_from_dict()
    frankfurt: str = field_from_dict()
    sydney: str = field_from_dict()
    tokyo: str = field_from_dict()
    london: str = field_from_dict()
    seoul: str = field_from_dict()
    
@dataclass
class FormatToContent(DataclassFromDict):
    flac: str = field_from_dict()
    mp3: str = field_from_dict()
    mpeg: str = field_from_dict()
    wav: str = field_from_dict()
    webm: str = field_from_dict()
    ogg: str = field_from_dict()
    opus: str = field_from_dict()

@dataclass 
class Defaults(DataclassFromDict):
    ssl_verification: bool = field_from_dict()
    customization_weight: float = field_from_dict()
    inactivity_timeout: int = field_from_dict()
    interim_results: bool = field_from_dict()
    keyword_threshold: float = field_from_dict()
    max_alternatives: int = field_from_dict()
    word_confidence: bool = field_from_dict()
    timestamps: bool = field_from_dict()
    profanity_filter: bool = field_from_dict()
    smart_formatting: bool = field_from_dict()
    speaker_labels: bool = field_from_dict()
    redaction: bool = field_from_dict()
    processing_metrics: bool = field_from_dict()
    processing_metrics_interval: float = field_from_dict()
    audio_metrics: bool = field_from_dict()
    end_of_phrase_silence_time: float = field_from_dict()
    split_transcript_at_phrase_end: bool = field_from_dict()
    speech_detector_sensitivity: float = field_from_dict()
    background_audio_supression: float = field_from_dict()
    # headers: Dict[str, bool] = field_from_dict()
    

watson_data = toml.load(os.path.join(CONFIG_ROOT, ENGINE_PATH.watson))["watson"]
watson_region_uris = WatsonRegionsUris.from_dict(watson_data["regions"]["uris"])
watson_format_to_content = FormatToContent.from_dict(watson_data["format_to_content"])
watson_default = Defaults.from_dict(watson_data["defaults"])

@dataclass 
class Watson:
    max_file_size_bytes = watson_data["max_file_size_bytes"]
    WatsonRegionsUris: WatsonRegionsUris  = watson_region_uris
    FormatToContent: FormatToContent  = watson_format_to_content
    Defaults: Defaults = watson_default