# Standard library imports
from dataclasses import dataclass
from typing import List, Dict, Any
# Local imports

@dataclass
class ApplyConfig:
    plugin_name : str
    args : List[Any]
    kwargs : Dict[str,Any]