from typing import List, Dict

class PluginSettingsInterface():
    def __init__(self, plugins: List[str]):
        self.plugins = plugins
   
    def get_data(self):
        return self.plugins