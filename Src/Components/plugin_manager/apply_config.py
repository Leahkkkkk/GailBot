# Standard library imports
from dataclasses import dataclass
from typing import List, Dict, Any
# Local imports

@dataclass
class ApplyConfig:
    """
    Configuration data for a plugin.

    Args:
        plugin_name (str): Name of the plugin.
        args (List[str]): non-keyword input args.
        kwargs (Dict[str,Any]): Keyworded input args.
    """
    plugin_name : str
    args : List[Any]
    kwargs : Dict[str,Any]