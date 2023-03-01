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
from typing import List, Tuple, Dict
import os
import logging
from model.dataBase.FileDatabase import FileObj
from util.GailBotData import Credential, ProfileConfig, Plugin, getWorkPath
from util.io import get_name

from PyQt6.QtCore import (
    QRunnable, pyqtSlot
)
class Worker(QRunnable):
    """ Worker 
        A sub-class of QRunnable class that is able to run the main function 
        on a separate thread 
        The Worker contains the main driver to run backend function, it is also 
        able to communicates the progress of running the backend function 
        through pyqtsignal
    
        Constructor Args:
            1.  files List[Tuple (str, FileObj, Dict)]: 
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
    def __init__(self, files: List [Tuple [str, FileObj, Dict]], signal):
        """ TODO: the input for the files should be files: List [Tuple[str, str]] """
        super(Worker, self).__init__()
        self.signals = signal
        self.killed = False
        self.files = files 
        self._initLogger()
        self.logger.info("gailbot runnable initialized")
        
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
        from gailbot.api import GailBot
        
        try:
            self.signals.start.emit()
            try:
                gb = GailBot()
                self.logger.info("get gailbot")
            except Exception as e:
                self.logger.error(e)
            self.signals.progress.emit(str("GailBot controller Initialized"))
            self.logger.info(self.files)
            self.logger.info(gb.gb.organizer.get_configured_sources()) 
            for file in self.files:
                self.logger.info(file)
                #iterate through the list of the file
                key, filedata, profile = file 
                filename = filedata.Name
                filePath = filedata.FullPath
                outPath = filedata.Output
                profile_name  = filedata.Profile 
                self.logger.info(key)
                self.logger.info(filename)
                self.logger.info(filePath)
                self.logger.info(outPath)
                self.logger.info(f"the profile name is {profile_name}, \
                                   the profile is {profile}")
                
                if not self.killed:
                    print("ready to add source")
                    print(filePath, outPath)
                    assert gb.add_source(filePath, outPath)
                    self.logger.info(filedata)
                    self.logger.info("Source Added")
                    # self.signals.progress.emit(f"Source{filename} Added")
                
                # TODO: change the way the frontend passes the setting data 
                if not self.killed and not gb.is_setting(profile_name):
                    try:
                        assert gb.create_new_setting(profile_name, profile)
                    except Exception as e:
                        self.logger.error("the profile cannot be created")
                        self.logger.error(e)
                        self.signals.error.emit("the profile cannot be created")
                    else:
                        self.logger.info("profile is created")
                        
                    try:
                        assert gb.apply_setting_to_source(filePath, profile_name)
                    except Exception as e:
                        self.logger.error(f"profile cannot be applied {e}")
                        self.signals.error.emit(f"profile cannot be applied {e}")
        
                    self.logger.info("Create Setting File")
                    # self.signals.progress.emit("Setting created")
                    self.signals.progress.emit("Transcribing")

            if not self.killed:
                self.signals.progress.emit(str("Transcribing"))
                self.logger.info("Transcribing")
                result, invalid = gb.transcribe()
                assert result
                if len(invalid) != 0:
                    invalid_files = str(invalid)
                    self.signals.error.emit(f"ERROR: the following files cannot be transcribed:{invalid_files}")
       
        except Exception as e:
            if  len(invalid) == 0:
                self.signals.error.emit(f"Error: the transcription fails")
            self.logger.error(f"{e} fails")
            self.signals.finish.emit()
        
        else:
            if not self.killed:
                for file in self.files:
                    key, filedata, profile = file 
                    if get_name(filedata) not in invalid:
                        self.signals.fileTranscribed.emit(key)
                    self.signals.finish.emit()
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
        
        
