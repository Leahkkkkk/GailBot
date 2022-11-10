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


EXIT_CODE_REBOOT = -20000
def main():
    exitCode = 0
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
    controller.run()
    exitCode = app.exec()
    if exitCode == EXIT_CODE_REBOOT:  
        app.exit()
        subprocess.run(["python", "main.py"], check=True)
        sys.exit(app)
    return exitCode


if __name__ == '__main__':
   main()