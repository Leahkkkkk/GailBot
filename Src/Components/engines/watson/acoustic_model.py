# Standard library imports
from typing import List, Any
# Local imports 

# Third party imports 


class WatsonAcousticModel:

    def __init__(self) -> None:
        pass 

    ### GETTERS

    def get_custom_acoustic_models(self) -> List:
        pass 

    def get_custom_acoustic_model(self, customization_id : str) -> Any:
        pass 

    def get_custom_model_audio_resources(self, customization_id : str) -> List:
        pass

    def get_custom_model_audio_resource(self, customization_id : str, 
            audio_name : str) -> Any:
        pass

    ### OTHERS

    def create_custom_acoustic_model(self, name : str, base_model_name : str,
            description : str) -> bool:
        pass 

    def delete_custom_acoustic_model(self, customization_id : str) -> bool:
        pass

    def train_custom_acoustic_model(self, customization_id : str, 
            custom_language_model_id : str) -> bool:
        pass

    def reset_custom_acoustic_model(self, customization_id : str) -> bool:
        pass

    def upgrade_custom_acoustic_model(self, customization_id : str, 
            custom_language_model_id : str, force : bool) -> bool:
        pass 

    def add_custom_model_audio_resource(self, customization_id : str,
            audio_name : str, audio_resource : Any, content_type : str, 
            contained_content_type : str, allow_overwrite : bool) -> bool:
        pass

    def delete_custom_model_audio_resource(self, customization_id : str, 
            audio_name : str) -> Any:
        pass


