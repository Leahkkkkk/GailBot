# Standard library imports
from typing import Any, List
# Local imports 

# Third party imports 

class WatsonLanguageModel:

    def __init__(self) -> None:
        pass 

    ### GETTERS

    def get_language_model(self, language_model_name : str) -> Any:
        pass 

    def get_custom_language_model(self, custom_model_name : str) -> Any:
        pass 

    def get_all_custom_model_corpora(self, customization_id : str) -> List:
        pass 

    def get_all_custom_model_custom_words(self, customization_id : str) -> List:
        pass 

    def get_specific_custom_language_corpus(
            self, customization_id : str, corpus_name : str) -> List:
        pass 

    def get_supported_language_models(self) -> List[str]:
        pass 

    def get_custom_language_models(self) -> List[str]:
        pass

    def get_custom_model_custom_word(
            self, customization_id : str, word : str) -> str:
        pass 

    def get_custom_model_grammars(self, customization_id : str ) -> List:
        pass 

    def get_custom_model_grammar(
            self, customization_id : str, grammar_name : str) -> Any:
        pass 

    ### OTHERS

    def create_custom_language_model(self, name : str, base_model_name : str, 
            dialect : str, description : str) -> bool:
        pass 

    def delete_custom_language_model(self, customization_id : str) -> bool:
        pass 

    def train_custom_language_model(self, customization_id : str) -> bool:
        pass 

    def reset_custom_language_model(self, customization_id : str) -> bool:
        pass 

    def upgrade_custom_language_model(self, customization_id : str) -> bool:
        pass 

    def add_corpus(self, customization_id : str, corpus_name : str, 
            corpus_file : str, allow_overwrite : bool) -> bool:
        pass 

    def delete_custom_model_corpus(
            self, customization_id : str, corpus_name : str) -> bool:
        pass

    def add_custom_model_words(
            self, customization_id : str, words : List[str]) -> bool:
        pass 

    def delete_custom_model_custom_word(
            self, customization_id : str, word : str) -> bool:
        pass 

    def add_custom_model_grammar(self, customization_id : str, 
            grammar_name : str, grammar_file : str, content_type : str, 
            allow_overwrite : bool) -> bool:
        pass 

    def delete_custom_model_grammar(
            self, customization_id : str, grammar_name : str) -> bool:
        pass