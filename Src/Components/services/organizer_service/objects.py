# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-20 09:24:22
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 14:02:15
from dataclasses import dataclass
from typing import Dict, Any
# Local imports
from ...organizer import Conversation, Settings
from ..fs_service import SourceHook, SettingsHook


class Source:
    def __init__(self, source_name: str, source_path: str,
                 transcriber_name: str, hook: SourceHook) -> None:
        self.source_name: str = source_name
        self.source_path: str = source_path
        self.transcriber_name: str = transcriber_name
        self.settings_profile_name: str = None
        self.conversation: Conversation = None
        self.configured: bool = False
        self.hook: SourceHook = hook


class SettingsProfile:

    def __init__(self, profile_name: str, settings: Settings,
                 hook: SettingsHook, settings_type: str) -> None:
        """
        Args:
            profile_name (str): Name of the profile.
            settings (Settings)
            hook (SettingsHook)
        """
        self.profile_name: str = profile_name
        self.settings: Settings = settings
        self.hook: SettingsHook = hook
        self.settings_type: str = settings_type
