'''
File: GBRunnable.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 5th October 2022 5:04:58 pm
Modified By:  Siara Small  & Vivian Li
-----
Description:  Main driver for running the backend function
NOTE: 
- currently the function to apply customized profile is unimplemented 
- the function that kill the thread need to be improved
'''
import multiprocessing
""" declared at the top level for multi-processing support """
multiprocessing.freeze_support()  
import sys
from typing import List, Tuple
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
import logging
from model.dataBase.fileDB import FileObj
from util.GailBotData import Credential, ProfileConfig, Plugin, getWorkPath

from gailbot.controller import GailBotController

from PyQt6.QtCore import (
    QRunnable, pyqtSlot
)


WATSON_API_KEY = Credential.WATSON_API_KEY
WATSON_LANG_CUSTOM_ID = Credential.WATSON_LANG_CUSTOM_ID
WATSON_REGION = Credential.WATSON_REGION
WATSON_BASE_LANG_MODEL = Credential.WATSON_BASE_LANG_MODEL
SETTINGS_PROFILE_NAME = ProfileConfig.SETTINGS_PROFILE_NAME
SETTINGS_PROFILE_EXTENSION = ProfileConfig.SETTINGS_PROFILE_EXTENSION

PLUGINS_TO_APPLY = Plugin.PLUGINS_TO_APPLY

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

class Worker(QRunnable):
    """ Worker 
        A sub-class of QRunnable class that is able to run the main function 
        on a separate thread 
        The Worker contains the main driver to run backend function, it is also 
        able to communicates the progress of running the backend function 
        through pyqtsignal
    
        Constructor Args:
            1.  files List[Tuple (str, FileObj)]: 
                a list of tuples that stores the file data, 
                the first element of tuple is file key 
                and the second is the file object
                
            2.  signal: 
                a Signal object to support communication between the runnable
                and transcribe controller
        
        Field:
            1. signals: a signal object  
            2. killed: True if the transcription process is killed by user
            3. files: a list of files that will be transcribed 
        
        Public Function:
            1. run(): main driver for the running GailBot
                 
    """
    def __init__(self, files: List [Tuple [str, FileObj]], signal):
        super(Worker, self).__init__()
        self.signals = signal
        self.killed = False
        self.files = files 
        self._initLogger()
        
    @pyqtSlot()
    def run(self):
        """ Public function to run GailBot to transcribe a list of files 
            stored in the worker class. 
            Emit signal to communicate transcription progress, which is 
            expected to be handled by the caller
            
            Signals: 
            - start()               : transcription started 
            - progress(str)         : contains a string about current progress
            - killed()              : function canceled be the suer
            - finish()              : entire transcription finished
            - fileTranscribed(str)  : contains a string stores the transcribed 
                                      file file key
        """
        self.logger.info("file ready to be transcribed" )
        profiles = set()
        workPath = getWorkPath()
        WORKSPACE_DIRECTORY_PATH = workPath.workSpace
        PLUGIN_DOWNLOAD_DIRECORY = workPath.plugin
        try:
            self.signals.start.emit()
            gb = GailBotController(WORKSPACE_DIRECTORY_PATH)
            self.signals.progress.emit(str("GailBot controller Initialized"))
        
            if not self.killed:
                plugin_suite_paths = gb.download_plugin_suite_from_url(
                Plugin.HIL_PLUGIN_URL, PLUGIN_DOWNLOAD_DIRECORY)  
                self.signals.progress.emit(str("Plugins Downloaded"))
                path = os.path.join(os.getcwd(), plugin_suite_paths[0])
                self.signals.progress.emit(str("Plugins Applied"))
                self.logger.info(gb.register_plugins(path))

            for file in self.files:
                #iterate through the list of the file
                key, filedata = file 
                filename = filedata.Name
                filePath = filedata.FullPath
                outPath = f"{filedata.Output}/{filename}_output/"
                profile = filedata.Profile 
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
                self.logger.info("Transcribing")
                gb.transcribe()
            
            if self.killed:
                self.logger.info("User cancelled the transcription")
                self.signals.killed.emit()
                         
        except Exception as e:
            self.signals.error.emit(f"${e.__class__} fails")
            self.logger.error(f"{e.__class__} fails")
        else:
            if not self.killed:
                for file in self.files:
                    key, filedata = file 
                    self.signals.fileTranscribed.emit(key)
                    self.signals.finish.emit()
        finally:
            self.setAutoDelete(True)

            
    def kill(self):
        """ public function to kill current running thread, the thread 
            will terminates after finishing the last function call 
        """
        self.logger.info("received request to cancel the thread")
        self.killed = True
        self.signals.killed.emit()
    
    def _initLogger(self):
        """ initialize the logger  """
        self.logExtra = {"source": "Backend"}
        self.logger = logging.getLogger()
        self.logger = logging.LoggerAdapter(self.logger, self.logExtra)
        
        
