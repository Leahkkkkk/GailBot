
import sys
# from multiprocessing import Queue
from controller import Controller
from PyQt6.QtWidgets import QApplication

   
EXIT_CODE_REBOOT = -20000
def run(exitCodeQueue=None):
    """ main driver function to run the app  """
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    # controller.signal.restart.connect(lambda: app.exit(EXIT_CODE_REBOOT))
    controller.run()
    sys.exit(app.exec())
    # exitCodeQueue.put(exitCode)
    # controller = None 
    # app = None