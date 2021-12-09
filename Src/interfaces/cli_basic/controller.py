# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 13:46:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-09 18:37:18

from typing import Tuple, Any
# Local imports
from ...components import GailBotController
from .view import CLIView

WS_DIR_PATH = "test_data/controller_data/workspaces/temp_ws"


class CLIController:

    def __init__(self) -> None:
        # TODO: This path should come from the user for now
        self.controller = GailBotController(WS_DIR_PATH)
        self.view = CLIView()
        self.menus = {
            "main": self.view.main_menu
        }

    def run(self) -> None:
        self.view.start_message()
        while True:
            if self.controller == None:
                self._initialize_controller()

    def _initialize_controller(self):
        self.view.uninitialized()
        ws_dir_path = self.view.get_input(
            "Enter workspace directory path")
        try:
            self.controller = GailBotController(ws_dir_path)
        except:
            pass

    def _main_menu(self):
        self.view.main_menu()
        option = self.view.get_input()
        if option == '1':
            self.controller.add_source()
        elif option == '2':
            pass
        elif option == '3':
            pass
        elif option == '4':
            pass
        else:
            self.view.invalid_input()
