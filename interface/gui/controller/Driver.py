'''
File: Driver.py
Project: GailBot GUI
File Created: Tuesday, 22nd November 2022 2:09:54 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 27th November 2022 10:25:00 am
Modified By:  Siara Small  & Vivian Li
-----
Description: the driver for running GailBot on a single process
'''
import sys
from controller import Controller
from PyQt6.QtWidgets import QApplication

def run():
    """ main driver function to run the app  """
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()
    app.exec()
