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


import sys

from controller import Controller
from PyQt6.QtWidgets import QApplication
from multiprocessing import Process, Queue
import multiprocessing



EXIT_CODE_REBOOT = -20000

exitCodeQueue = Queue()
def main(exitCodeQueue):
    """ main driver function to run the app  """
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
    controller.run()
    exitCode = app.exec()
    exitCodeQueue.put(exitCode)


if __name__ == '__main__':
    multiprocessing.set_start_method('forkserver', force=True)
    multiprocessing.freeze_support()
    EXIT_CODE_REBOOT = -20000
    exitCodeQueue = Queue()
    exitCode = EXIT_CODE_REBOOT
    print("top main")
    main(exitCodeQueue)
    
    while exitCode == EXIT_CODE_REBOOT:
        process = Process(target = main, args = (exitCodeQueue,))
        process.start()
        exitCode = exitCodeQueue.get()
        process.join()
        del process
    
