# Standard imports

# Local imports

# Third party imports
from PyQt5.QtCore import QObject, pyqtSlot


class MainController(QObject):

    def __init__(self, model) -> None:
        super().__init__()
