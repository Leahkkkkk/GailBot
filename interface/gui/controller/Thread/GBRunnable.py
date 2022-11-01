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
from typing import List, Tuple, Dict
import os
import logging
import time

from controller.Signals import Signal

from gailbot import GailBotController
from PyQt6.QtCore import (
    QRunnable, 
    QObject, 
    pyqtSlot, 
    pyqtSignal
)

# TODO: move this to a config file 
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

def get_settings_dict(): #TODO: get the actual setting dictionary for the 
                         #      profile database
                         
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
    finished = pyqtSignal(str)
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
    def __init__(self, files: List [Tuple [str, Dict]], signal:Signal):
        """constructor for Worker class

        Args:
            files List[Tuple (filekey, file data)]: a list of tuples that 
            stores the file data, the first element of tuple is filekey 
            and the second is the file object
        """
        super(Worker, self).__init__()
        self.signals = signal
        self.killed = False
        self.files = files 
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
        profiles = set()
        
        try:
            self.signals.start.emit()
            gb = GailBotController(WORKSPACE_DIRECTORY_PATH)
            self.signals.progress.emit(str("GailBot controller Initialized"))
        
            if not self.killed:
                plugin_suite_paths = gb.download_plugin_suite_from_url(
                "https://sites.tufts.edu/hilab/files/2022/05/HiLabSuite.zip", 
                "./plugins")
                self.signals.progress.emit(str("Plugins Downloaded"))
                path = os.path.join(os.getcwd(), plugin_suite_paths[0])
                self.signals.progress.emit(str("Plugins Applied"))
                self.logger.info(gb.register_plugins(path))

            for file in self.files:
                #iterate through the list of the file
                key, filedata = file 
                filename = filedata["Name"]
                filePath = filedata["FullPath"]
                outPath = f"{filedata['Output']}/output/"
                profile = filedata["Profile"]  
                self.logger.info(key)
                self.logger.info(filename)
                self.logger.info(filePath)
                self.logger.info(outPath)
                
                if not self.killed:
                    assert gb.add_source(filename, filePath, outPath)
                    self.logger.info(filedata)
                    self.logger.info("Source Added")
                    self.signals.progress.emit(f"Source{filename} Added")
    
                if not self.killed and not gb.is_settings_profile(profile):
                    gb.create_new_settings_profile(profile, get_settings_dict())
                    profiles.add(profile)
                    assert gb.is_settings_profile(profile)
                    self.logger.info("Create Setting File")
                    self.signals.progress.emit("Setting created")

                if not self.killed:
                    assert gb.apply_settings_profile_to_source(
                        filename, profile)
                    self.logger.info("Apply Setting")
                    self.signals.progress.emit(str("Apply Setting"))

                    assert gb.is_source_ready_to_transcribe(filename)
                    self.logger.info("Ready to transcribe")
                    self.signals.progress.emit(f"{filename} Ready to transcribe")
                
            if not self.killed:
                self.signals.progress.emit(str("Transcribing"))
                self.logger.info("transcribing")
                gb.transcribe()
            
            if self.killed:
                self.logger.info("User killed the thread")
                self.signals.killed.emit()
                
        except Exception as e:
            self.signals.error.emit(f"${e.__class__}fails")
            self.logger.error(f"{e.__class__}fails")
            time.sleep(2)
        else:
            if not self.killed:
                for file in self.files:
                    key, filedata = file 
                    self.signals.fileTranscribed.emit((key, "Transcribed"))
                    self.signals.finish.emit()
        finally:
            self.setAutoDelete(True)


    def kill(self):
        """ public function to kill current running thread, the thread 
            will terminates after finishing the last function call 
        """
        self.logger.info("User tring to cancel thread")
        self.killed = True
        self.signals.killed.emit()