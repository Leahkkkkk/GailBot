""" implenmentation of Worker class 
a subclass of QRunnable class 
used to run a function on separte thread 
with the added feature of handling signals
"""
from PyQt6.QtCore import QRunnable, QObject, pyqtSlot, pyqtSignal
from gailbot import GailBotController, GailBotSettings
import os
import logging
import time
from util import Logger

WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
WORKSPACE_DIRECTORY_PATH = "/Users/yike/Desktop/GB-UI/workdir"
#  ------------- Controller
SETTINGS_PROFILE_NAME = "test_profile"
SETTINGS_PROFILE_EXTENSION = "json"

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
    finished = pyqtSignal(int)
    start = pyqtSignal()
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    result = pyqtSignal()
    killed = pyqtSignal()
    endThread = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, filename:str, filepath:str, key:int):
        super(Worker, self).__init__()
        self.signals = Signals()
        self.key = key
        self.is_killed = False
        self.filepath = filepath
        self.filename = filename
        self.logger = Logger.makeLogger("Backend: ")

    def makeLogger(self):
        self.logExtra = {"source": "Backend"}
        self.logger = logging.getLogger()
        self.logger = logging.LoggerAdapter(self.logger, self.logExtra)

    @pyqtSlot()
    def run(self):
        self.logger.info("file ready to be transcribed" )
        
        

        try:
            # assert(0 == 1)
            self.signals.start.emit()
            gb = GailBotController(WORKSPACE_DIRECTORY_PATH)
            self.signals.progress.emit(str("GailBot controller Initialized"))
            # time.sleep(10)
        
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
        self.logger.info("User tring to cancel thread")
        self.is_killed = True