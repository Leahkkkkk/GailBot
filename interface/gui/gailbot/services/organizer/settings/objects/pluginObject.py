from typing import List

class PluginSuiteSetObj:
    def __init__(self, plugins) -> None:
       self.data = plugins 
    
    def get_data(self) -> List[str]:
        return self.data