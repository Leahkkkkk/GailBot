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


from controller import Controller
from PyQt6.QtWidgets import QApplication
import sys


EXIT_CODE_REBOOT = -11231351

def main():
    exitCode = 0
    while True:
        print("try")
        app = QApplication(sys.argv)
        controller = Controller.Controller()
        controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
        controller.run()
        exitCode = app.exec()
        app = None 
        controller = None
      
        print(exitCode)
        if exitCode != EXIT_CODE_REBOOT: break
    return exitCode


if __name__ == '__main__':
   main()