'''
File: main.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:19:06 am
Modified By:  Siara Small  & Vivian Li
-----
'''


import sys
import subprocess

from controller import Controller
from PyQt6.QtWidgets import QApplication
from multiprocessing import Process, Queue


EXIT_CODE_REBOOT = -20000

exitCode = Queue()

def main(exitCode:Queue):
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
    controller.run()
    code = app.exec()
    exitCode.put(code)
    controller = None 
    app = None

if __name__ == '__main__':
    process = Process(target = main, args = (exitCode,))
    process.start()
    code = exitCode.get()
    process.join()
    del process
    print(code)
    
    while code == EXIT_CODE_REBOOT:
        process = Process(target = main, args = (exitCode,))
        process.start()
        code = exitCode.get()
        process.join()
        del process
    
