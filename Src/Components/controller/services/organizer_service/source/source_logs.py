# Standard imports
from enum import Enum
from datetime import datetime
# Local imports
from ......utils.logger import BaseLogHandler,LogRequestType
from .....io import IO

class RequestType(LogRequestType):
    ERROR = "ERROR"
    FILE = "FILE"
    CONSOLE = "CONSOLE"

class ErrorLogHandler(BaseLogHandler):

    def __init__(self,  result_dir_path : str) -> None:
        super().__init__()
        ## Vars.
        self.handle_type = RequestType.ERROR
        self.log_count = 0
        self.log_file_base_name = "error_log"
        self.log_extension = "txt"
        self.log_path = "{}/{}.{}".format(
            result_dir_path,self.log_file_base_name,self.log_extension)
        ## Objects
        self.io = IO()
        ## Initialize
        if not self.io.is_directory(result_dir_path):
            raise Exception("Cannot initialize ErrorLogHandler")

    def get_log_path(self) -> str:
        return self.log_path

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            # Create the message.
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            msg = "[log: {}] [{}]: {}\n".format(self.log_count,dt_string,request)
            # Write the message to the log file.
            self.io.write(self.log_path,msg,False)
            self.log_count+=1
        else:
            super().handle(request_type, request)

class ConsoleLogHandler(BaseLogHandler):

    def __init__(self) -> None:
        super().__init__()
        self.log_count = 0
        self.handle_type = RequestType.CONSOLE

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            # This log simply writes to the console.
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            msg = "[log: {}] [{}]: {}".format(self.log_count,dt_string,request)
            self.log_count+=1
            print(msg)
        else:
            super().handle(request_type, request)

class FileLogHandler(BaseLogHandler):

    def __init__(self,  result_dir_path : str) -> None:
        super().__init__()
        ## Vars.
        self.handle_type = RequestType.FILE
        self.log_count = 0
        self.log_file_base_name = "log"
        self.log_extension = "txt"
        self.log_path = "{}/{}.{}".format(
            result_dir_path,self.log_file_base_name,self.log_extension)
        ## Objects
        self.io = IO()
        ## Initialize
        if not self.io.is_directory(result_dir_path):
            raise Exception("Cannot initialize FileLogHandler")

    def get_log_path(self) -> str:
        return self.log_path

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            # Create the message.
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            msg = "[log: {}] [{}]: {}\n".format(self.log_count,dt_string,request)
            self.log_count+=1
            # Write the message to the log file.
            self.io.write(self.log_path,msg,False)
        else:
            super().handle(request_type, request)


