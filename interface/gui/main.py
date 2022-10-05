from view import MainWindow 
from controller import Controller
from model import Model
from PyQt6.QtWidgets import QApplication
import sys

# app = QApplication(sys.argv)

# window = MainWindow.MainWindow()
# window.show()

# app.exec()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    controller.run()
    app.exec()
    