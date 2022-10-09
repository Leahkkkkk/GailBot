from platform import python_branch
import sys

from view.widgets import ToggleView, Label, Table

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel


class dummyWidget(QWidget):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        for i in range (10):
            newlabel = QLabel(f"dummy lable{i}")
            self.layout.addWidget(newlabel)
        self.btn = QPushButton("add")
        self.layout.addWidget(self.btn)
        self.btn.clicked.connect(self._addWidget)
    
    def _addWidget(self):
        newLabel = QLabel("new label")
        self.layout.addWidget(newLabel)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        table = Table.Table()

        self.setFixedSize(QSize(700, 200))

        # Set the central widget of the Window.
        self.setCentralWidget(table)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
