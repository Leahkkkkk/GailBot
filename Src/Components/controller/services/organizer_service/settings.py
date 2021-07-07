# Standard imports
from typing import Dict
from dataclasses import dataclass
# Local imports
from ....organizer import Settings
from ..fs_service import SettingsHook

@dataclass
class SettingProfile:
    profile_name : str
    settings : Settings
    hook : SettingsHook