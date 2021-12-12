# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 18:15:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-12 15:21:30

from typing import Any
import os


class CLIView:

    def __init__(self):
        pass

    def start_message(self):
        print("GailBot starting...")
        print("To report bugs, email: muhammad.umair@tufts.edu")

    def uninitialized(self):
        print("GailBot not initialized...")

    def get_input(self, message: str = None) -> str:
        if message != None:
            print(message)
        return str(input(" >> "))

    def invalid_input(self):
        print("ERROR: invalid option selected")

    def main_menu(self):
        print("1. Add source")
        print("2. Create settings profile")
        print("3. Apply settings profiles")
        print("4. Transcribe")
        print("5. Exit")

    def display_source(self, source_name: str, settings_profile_name: str) -> None:
        print("Source: {} | Profile {}".format(
            source_name, settings_profile_name))

    def display_settings_profile(self, profile_name: str):
        print("Settings profile {}".format(profile_name))

    def add_source(self, name: str, is_added: bool):
        print("Adding source {} -> Status : {}".format(
            name, "SUCCESS" if is_added else "FAILED"))

    def create_new_settings_profile(self, name: str, is_added: bool):
        print("Creating profile {} -> Status : {}".format(
            name, "SUCCESS" if is_added else "FAILED"))

    def clear(self):
        os.system('clear')

    def exiting(self):
        print("Exiting...")

    def start_transcription(self):
        print("Starting transcription...")

    def finished_transcription(self):
        print("Completed transcription")
