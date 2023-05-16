from typing import List, Dict

class PluginSettingsInterface():
    """
    Interface for plugin settings
    """
    def __init__(self, plugins: List[str]):
        self.plugins = plugins
   
    def get_data(self):
        """
        Accesses and returns and object's plugin settings
        """
        return self.plugins