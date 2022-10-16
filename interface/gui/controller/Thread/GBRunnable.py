'''
File: GBRunnable.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 5th October 2022 5:04:58 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

import os
import logging
import time

from gailbot import GailBotController
from PyQt6.QtCore import (
    QRunnable, 
    QObject, 
    pyqtSlot, 
    pyqtSignal
)

WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
WORKSPACE_DIRECTORY_PATH = "/Users/yike/Desktop/GB-UI/workdir"
#  ------------- Controller
SETTINGS_PROFILE_NAME = "test_profile"
SETTINGS_PROFILE_EXTENSION = "json"

""" Gailbot plugins from documentation  
"""
PLUGINS_TO_APPLY = [
        "constructTree",
        "utteranceDict",
        "speakerDict",
        "conversationDict",
        "convModelPlugin",
        "overlaps",
        "pauses",
        "gaps",
        "syllRate",
        "layerPrint01",
        "plainPrint",
        "chat",
        "txt",
        "csvPlugin",
        "csvWordLevel",
        "XMLtoCSV",
        "xmlSchema"
]

def get_settings_dict():
    """ returns a dictionary that contains the setting information
    """
    return {
        "core": {},
        "plugins": {
                "plugins_to_apply": PLUGINS_TO_APPLY
        },
        "engines": {
            "engine_type": "watson",
            "watson_engine": {
                "watson_api_key": WATSON_API_KEY,
                "watson_language_customization_id": "",
                "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                "watson_region": WATSON_REGION,

            }
        }
    }

class Signals(QObject):
    """ contain signals in order for Qrunnable object to communicate
        with controller
    """
    finished = pyqtSignal(int)
    start = pyqtSignal()
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    result = pyqtSignal()
    killed = pyqtSignal()
    endThread = pyqtSignal()

class Worker(QRunnable):
    """ a subclass of QRunnable class 
        used to run GailBot function on separte thread 
        with the added feature of handling signals
    """
    def __init__(self, filename:str, filepath:str, key:int):
        """constructor for Worker class

        Args:
            filename (str): filename 
            filepath (str): absolute file path to the file
            key (int): an index key that identify the file in file database
        """
        super(Worker, self).__init__()
        self.signals = Signals()
        self.key = key
        self.is_killed = False
        self.filepath = filepath
        self.filename = filename
        self._initLogger()

    def _initLogger(self):
        """ initialize the logger  """
        self.logExtra = {"source": "Backend"}
        self.logger = logging.getLogger()
        self.logger = logging.LoggerAdapter(self.logger, self.logExtra)


    @pyqtSlot()
    def run(self):
        """ public function that can be called to run GailBot """
        self.logger.info("file ready to be transcribed" )
        
        try:
            self.signals.start.emit()
            gb = GailBotController(WORKSPACE_DIRECTORY_PATH)
            self.signals.progress.emit(str("GailBot controller Initialized"))
        
            if not self.is_killed:
                plugin_suite_paths = gb.download_plugin_suite_from_url(
            "https://sites.tufts.edu/hilab/files/2022/05/HiLabSuite.zip", "./plugins")
                self.signals.progress.emit(str("Plugins Downloaded"))
                path = os.path.join(os.getcwd(), plugin_suite_paths[0])
                self.signals.progress.emit(str("Plugins Applied"))
                self.logger.info(gb.register_plugins(path))

            if not self.is_killed:
                assert gb.add_source(self.filename, 
                                     f"{self.filepath}/{self.filename}", 
                                     "/Users/yike/Desktop/output")
                self.logger.info("Source Added")
                self.signals.progress.emit(str("Source Added"))
                
            if not self.is_killed:
                gb.create_new_settings_profile("test-settings", 
                                               get_settings_dict())
                assert gb.is_settings_profile("test-settings")
                self.logger.info("Create Setting File")
                self.signals.progress.emit(str("Create Setting File"))

            if not self.is_killed:
                assert gb.apply_settings_profile_to_source(self.filename, 
                                                           "test-settings")
                self.logger.info("Apply Setting")
                self.signals.progress.emit(str("Apply Setting"))

            if not self.is_killed:
                assert gb.is_source_ready_to_transcribe(self.filename)
                self.logger.info("Ready to transcribe")
                self.signals.progress.emit(str("Ready to transcribe"))
            
            if not self.is_killed:
                self.signals.progress.emit(str("Transcribing"))
                self.logger.info("transcribing")
                gb.transcribe()
            
            if self.is_killed:
                self.logger.info("User killed the thread")
                self.signals.killed.emit()
        
        except Exception as e:
            self.signals.error.emit(f"${e.__class__}fails")
            self.logger.error(f"{e.__class__}fails")
            time.sleep(2)
        else:
            if not self.is_killed:
                self.signals.result.emit()
                self.signals.finished.emit(self.key)
            self.signals.endThread.emit()    
        finally:
            self.signals.endThread.emit()


    def kill(self):
        """ public function to kill current running thread, the thread 
            will terminates after finishing the last function call 
        """
        self.logger.info("User tring to cancel thread")
        self.is_killed = True