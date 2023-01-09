# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-09 11:41:12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:45:27

from typing import List, Dict, Any, BinaryIO


class WatsonAMInterface:

    def __init__(self, apikey : str, region : str):
        pass

    def get_custom_models(self) -> Dict:
        pass

    def get_custom_model(
        self,
        customization_id: str
    ) -> Dict:
        pass

    def get_custom_models(self) -> Dict[str, str]:
        pass

    def create_custom_model(
        self,
        base_model_name : str,
        description : str
    ):
        pass

    def delete_custom_model(self, customization_id: str) -> bool:
        pass

    def train_custom_model(self, customization_id: str) -> bool:
        pass

    def reset_custom_model(self, customization_id: str) -> bool:
        pass

    def upgrade_custom_model(self, customization_id: str) -> bool:
        pass

    def get_custom_audio_resources(self, customization_id: str) -> List[Dict]:
        pass

    def get_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str
    ) -> Dict:
        pass

    def add_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str,
        audio_resource: BinaryIO,
        content_type: str
    ) -> bool:
        pass

    def delete_custom_audio_resource(
        self,
        customization_id: str,
        audio_name: str
    ) -> bool:
        pass
