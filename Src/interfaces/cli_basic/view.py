# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 18:15:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-09 18:36:39

from typing import Any


class CLIView:

    def __init__(self):
        pass

    def start_message(self):
        print("Starting GailBot!")

    def uninitialized(self):
        pass

    def get_input(self, message: str = None) -> str:
        if message != None:
            print(message)
        return input(" > ")

    def invalid_input(self):
        print("Invalid option selected")

    def main_menu(self):
        print("1. Add source")
        print("2. Create settings profile")
        print("3. Apply settings profiles")
        print("4. Exit")
