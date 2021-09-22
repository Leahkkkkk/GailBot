# Standard imports
import sys
# Local imports
from Src.Interfaces import GailBotGUI


class App:

    def __init__(self, enable_gui: bool = False) -> None:
        self.interface = None
        if enable_gui:
            self.interface = GailBotGUI()
        else:
            raise Exception("Not yet implemented")

    def run(self) -> None:
        self.interface.run()


if __name__ == "__main__":
    app = App(enable_gui=True)
    sys.exit(app.run())
