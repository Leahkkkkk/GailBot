'''
File: main.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:19:06 am
Modified By:  Siara Small  & Vivian Li
-----
Description: main driver for a GUI app that support front and interface to 
             allow user transcribe file using gailbot 
'''

import hooks
import ssl
import os 
import logging
from controller import Controller 
from PyQt6.QtWidgets import QApplication
import sys

def run():
    """ main driver function to run the app  """
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()
    app.exec()
    
    
if __name__ == '__main__':
    run()
    
    