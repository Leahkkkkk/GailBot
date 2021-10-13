# Standard imports
from typing import List, Dict, Tuple, Any
# Local imports
from ....io import IO


class PipelineServiceLoader:
    """
    Responsible for loading and parsing files for the PipelineService.
    """

    def __init__(self) -> None:
        self.io = IO()

    def parse_analysis_plugin_configuration_file(self, config_file: str) \
            -> Tuple[bool, List[Dict]]:
        """
        Parse an analysis plugin configuration file.

        Args:
            config_file (str): Path to the config file.

        Returns:
            (Tuple[bool, List[Dict]]):
                Obtain True + list of dictionaries containing Config data for
                analysis plugins if successful, False + None otherwise.
        """
        try:
            _, data = self.io.read(config_file)
            return (True, data["plugin_configs"])
        except:
            return (False, None)

    def parse_format_configuration_file(self, config_file: str) \
            -> Tuple[bool, Tuple[str, List[Dict[str, Any]]]]:
        """
        Parse an analysis plugin configuration file.

        Args:
            config_file (str): Path to the config file.

        Returns:
            (Tuple[bool, Tuple[str,List[Dict[str,Any]]]])
                True + tuple containing the format ame + Config data for the
                format plugins. False, (None, None) otherwise.
        """
        try:
            _, data = self.io.read(config_file)
            return (True, (data["format_name"], data["format_plugin_configs"]))
        except Exception as e:
            return (False, (None, None))
