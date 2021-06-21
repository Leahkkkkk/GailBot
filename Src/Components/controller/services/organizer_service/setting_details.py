# Standard library imports
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SettingDetails:
    name : str
    is_saved :  bool
    save_location : str
    used_by_sources : str
    profile_type : str
    attributes : List[str]
    values : Dict[str,str]
