from gailbot.plugins import Methods
from typing import Dict, Union, List

""" TODO:
1. connection GBPluginMethods with analysis component, add testing
"""
class GBPluginMethods(Methods):
    def __init__(self):
        pass

    @property
    def audios(self) -> Dict[str,str]:
        """ map from name to audio path """
        raise NotImplementedError()

    @property
    def utterances(self) -> Dict[str,Dict]:
        raise NotImplementedError()

    @property
    def save_dir(self) -> str:
        """ NOTE: if we have save item, should we delete this? """
        raise NotImplementedError()
        

    def save_item(self, 
                  data: Union[str, List[str]] ,  
                  temp: bool = True, 
                  format: str = None, 
                  fun: callable = None ) -> bool :
        """ function provided for the plugin to save file """
        raise NotImplementedError()