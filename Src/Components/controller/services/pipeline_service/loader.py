# Standard imports
from typing import List, Dict, Tuple, Any
# Local imports
from ....io import IO

class PipelineServiceLoader:

    def __init__(self) -> None:
        self.io = IO()

    def parse_analysis_plugin_configuration_file(self, config_file : str) \
            -> Tuple[List[Dict]]:
        try:
            _ , data = self.io.read(config_file)
            return (True, data["plugin_configs"])
        except:
            return (False, None)

    def parse_format_configuration_file(self, config_file : str) \
            -> Tuple[Tuple[str,List[Dict[str,Any]]]]:
        try:
            _, data = self.io.read(config_file)
            return (True,(data["format_name"], data["format_plugin_configs"]))
        except Exception as e:
            return (False, (None, None))
