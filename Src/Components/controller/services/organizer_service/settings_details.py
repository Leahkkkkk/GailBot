from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SettingsDetails:
    profile_name : str
    is_saved : str
    used_by_sources : List[str]
    values : Dict[str,Any]
