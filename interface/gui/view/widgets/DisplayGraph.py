from typing import Dict, List
from PyQt6.QtGui import  QTextDocument
from PyQt6.QtWidgets import QTextEdit, QWidget

class DisplayGraph(QTextEdit):
    def __init__(self, dependencyGraph: Dict[str, List[str]]):
      super().__init__()
      
    def displayGaph(self):
        raise NotImplementedError