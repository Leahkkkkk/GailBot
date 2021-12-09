# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 17:52:42
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-09 18:04:30


import sys
from Src import Interface


class App:

    def __init__(self) -> None:
        self.interface = Interface()

    def run(self, interface: str) -> None:
        self.interface.run(interface)


if __name__ == "__main__":
    pass


if __name__ == "__main__":
    app = App()
    sys.exit(app.run(interface="cli_basic"))
