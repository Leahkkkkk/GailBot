from typing import List, Tuple, Dict
from gailbot.api import GailBot
from PyQt6.QtCore import QObject, pyqtSignal
from util.Logger import makeLogger

logger = makeLogger("F")

profileNameExist = "setting profile name {name} already exists"
fileExist = "file name {name} already exists"
profileCreateError = "setting profile {name} cannot be created"
fileUploadError = "file {name} cannot be uploaded"

profileCreated = "profile {name} has been created"
fileUploaded = "file {name} has been uploaded"

class ProfileSignal(QObject):
    load_profile = pyqtSignal(object, name="load_profile")
    send_profile_name = pyqtSignal(str, name="send_profile_name")
    plugin_details = pyqtSignal(object, name="plugin_details")
    

class FileSignal(QObject):
    show_files = pyqtSignal(list)
    show_file_profile = pyqtSignal(tuple)
    show_file_details = pyqtSignal(object)
    file_transcribed = pyqtSignal(str)
    file_status = pyqtSignal(str)
      
class StatusSignal(QObject):
    error = pyqtSignal(str)
    succeed = pyqtSignal(str)

class GBController:
    def __init__(self, userRoot:str) -> None:
        self.gb = GailBot(userRoot)
        self.profileSignal = ProfileSignal()
        self.fileSignal = FileSignal()
        self.statusSignal = StatusSignal()
        
    def addSources(self, sources: List[Tuple[str, str]]):
        try:
            assert self.gb.add_sources(sources)
            self.statusSignal.succeed("files are added")
        except Exception as e:
            logger.error(e)
            self.statusSignal.error("files cannot be added")
    
    def addSource(self, source: str):
        try:
            assert self.gb.add_source(source)
            self.statusSignal.succeed(fileUploaded.format(name=source))
        except Exception as e:
            logger.error(f"add source error {e}")
            self.statusSignal.error(fileUploadError.format(name=source))
            
    def removeSource(self, source:str):
        try:
            assert self.gb.remove_source(source)
        except Exception as e:
            logger.error(f"file remove error {e}")
            self.statusSignal.error("file cannot be removed")
        
    def removeSetting(self, setting: str):
        try: 
            assert self.gb.remove_setting(setting)
        except Exception as e:
            logger.error(f"setting remove error {e}")
            self.statusSignal.error(f"setting {setting} cannot be removed")
        
    def createNewSetting(self, setting: Tuple[str, Dict[str, str]]):
        name, data = setting
        try:
            if self.gb.is_setting(name):
                self.statusSignal.error(profileNameExist.format(name=name))
                logger.warn(f"setting {setting} already exists")
                return False
            assert self.gb.create_new_setting(name, data)
        except Exception as e:
            logger.error("setting creation fails, error: {e}")
            self.statusSignal.error(profileCreateError.format(name=setting))
            return False 
        else:
            self.statusSignal.succeed(profileCreated.format(name=setting))
            

        
    