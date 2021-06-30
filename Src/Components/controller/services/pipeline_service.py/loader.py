from typing import List, Any, Tuple, Dict

class PipelineServiceLoader:

    def __init__(self) -> None:
        pass

    def parse_analysis_plugin_configuration_file(self, config_file : str) -> List[Any]:
        pass

    def parse_format_configuration_file(self, config_file : str) -> Tuple[str,Dict[str,Any]]:
        pass
