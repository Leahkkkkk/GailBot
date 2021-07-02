from typing import List, Any, Tuple, Dict
# Local imports
from ....io import IO

class PipelineServiceLoader:
    """
    Loader for the pipeline service. Enforces structure for configuration
    files.
    """

    def __init__(self) -> None:
        self.io = IO()

    def parse_analysis_plugin_configuration_file(self, config_file : str) \
            -> List[Dict]:
        """
        Parse the configuration file for analysis plugins.

        Args:
            config_file (str): Path to the config file.

        Returns:
            (List[Dict]):
                Returns a list of dictionaries, each of which is used to
                configure a plugin.
        """
        try:
            _ , data = self.io.read(config_file)
            return data["plugin_configs"]
        except:
            return []

    def parse_format_configuration_file(self, config_file : str) \
            -> Tuple[str,List[Dict[str,Any]]]:
        """
        Parse a format plugin configuration file.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            (Tuple[str,List[Dict[str,Any]]]):
                Name of the format + list of plugin config dictionaries.
        """
        try:
            _, data = self.io.read(config_file)
            return (data["format_name"], data["format_plugin_configs"])
        except Exception as e:
            return ("",[])
