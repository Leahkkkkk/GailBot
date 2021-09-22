# Standard imports
from typing import List
# Local imports

# Third party imports
from PyQt5.QtWidgets import QApplication
from .views import MainView

class GailBotGUI(QApplication):

    def __init__(self,sys_argv : List[str] = []) -> None:
        super().__init__(sys_argv)
        ## Add all the models

        ## Add all the controllers

        ## Add all the views
        self.main_view = MainView()

    def run(self) -> None:
        self.main_view.show()
        self.exec_()
