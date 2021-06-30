from typing import List, Any, Tuple, Dict
# Local imports
from ....io import IO

class PipelineServiceLoader:

    def __init__(self) -> None:
        self.io = IO()

    def parse_analysis_plugin_configuration_file(self, config_file : str) \
            -> List[Dict]:
        try:
            _ , data = self.io.read(config_file)
            return data["plugin_configs"]
        except:
            return []

    def parse_format_configuration_file(self, config_file : str) -> Tuple[str,Dict[str,Any]]:
        try:
            _, data = self.io.read(config_file)
            return (data["format_name"], data["format_plugin_configs"])
        except Exception as e:
            return ("",[])
