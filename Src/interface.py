# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 18:01:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-12 15:05:34

from .interfaces import CLIController


class Interface:

    def __init__(self):
        self.interfaces = {
            "cli_basic": CLIController
        }

    def run(self, interface: str) -> None:
        try:
            self.interfaces[interface]().run()
        except Exception as e:
            print("INTERFACE ERROR: {}".format(e))
