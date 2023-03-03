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
import huggingface_hub 
# import pyannote.audio
import dtw 
import whisper
import scipy
import gailbot

EXIT_CODE_REBOOT = -20000
def run(exitCodeQueue):
    """ main driver function to run the app  """
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
    controller.run()
    exitCode = app.exec()
    exitCodeQueue.put(exitCode)
    controller = None 
    app = None