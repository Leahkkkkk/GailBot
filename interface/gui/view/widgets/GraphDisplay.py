from typing import Dict, List
from PyQt6.QtWidgets import QTextEdit, QWidget
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QHBoxLayout, QWidget


class GraphDisplay(QGraphicsView):
    def __init__(self, dependencyGraph: Dict[str, List[str]]):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumSize(QSize(200,200)) # TODO: check the size
      
    def displayGaph(self):
        raise NotImplementedError