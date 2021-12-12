# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 13:46:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-12 15:21:14

from typing import Tuple, Any
import os
import sys
import json
# Local imports
from ...components import GailBotController
from .views import CLIView


class CLIController:

    def __init__(self) -> None:
        # TODO: This path should come from the user for now
        self.controller = None
        self.view = CLIView()
        self.menus = {
            "main": self._main_menu,
        }
        self.current_menu = "main"

    def run(self) -> None:
        try:
            self.view.clear()
            self.view.start_message()
            while True:
                if self.controller == None:
                    self._initialize_controller()
                else:
                    self._menus()
        except KeyboardInterrupt:
            self.view.exiting()

    def _initialize_controller(self):
        self.view.uninitialized()
        ws_dir_path = self.view.get_input("Enter workspace directory path...")
        try:
            self.controller = GailBotController(ws_dir_path)
        except Exception as e:
            pass

    def _menus(self):
        self.menus[self.current_menu]()

    def _main_menu(self):
        self.view.clear()
        self._display_settings_profiles()
        self._display_sources()
        self.view.main_menu()
        option = self.view.get_input()
        if option == '1':
            self._add_source()
        elif option == '2':
            self._create_settings_profile()
        elif option == '3':
            self._apply_settings_profile()
        elif option == '4':
            self._transcribe()
        elif option == '5':
            self.view.exiting()
            sys.exit(0)
        else:
            self.view.invalid_input()

    def _add_source(self):
        name = self.view.get_input("Enter source name")
        path = self.view.get_input("Enter source path")
        result_dir = self.view.get_input("Enter source result directory path")
        is_added = self.controller.add_source(
            name, path, result_dir)
        self.view.add_source(name, is_added)

    def _create_settings_profile(self):
        name = self.view.get_input("Enter settings profile name")
        path = self.view.get_input("Enter settings file path")
        with open(path, 'r') as f:
            data = json.load(f)
            is_created = self.controller.create_new_settings_profile(
                name, data)
            self.view.create_new_settings_profile(name, is_created)

    def _apply_settings_profile(self):
        source_name = self.view.get_input("Enter source name")
        profile_name = self.view.get_input("Enter profile name")
        self.controller.apply_settings_profile_to_source(
            source_name, profile_name)

    def _display_sources(self):
        source_names = self.controller.get_source_names()
        for name in source_names:
            self.view.display_source(
                name, self.controller.get_source_settings_profile_name(name))

    def _display_settings_profiles(self):
        profile_names = self.controller.get_settings_profile_names()
        for name in profile_names:
            self.view.display_settings_profile(name)

    def _transcribe(self):
        self.view.start_transcription()
        self.controller.transcribe()
        self.view.finished_transcription()
