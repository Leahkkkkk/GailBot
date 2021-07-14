# Standard library imports
from enum import Enum

class GBSettingAttrs(Enum):
    engine_type = "engine_type"
    watson_api_key = "watson_api_key"
    watson_language_customization_id = "watson_language_customization_id"
    watson_base_language_model = "watson_base_language_model"
    watson_region = "watson_region"
    output_format = "output_format"
    analysis_plugins_to_apply = "analysis_plugins_to_apply"
