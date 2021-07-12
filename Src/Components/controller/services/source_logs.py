# Standard imports
from enum import Enum
# Local imports
from ....utils.logger import BaseLogHandler,LogRequestType


class RequestType(LogRequestType):
    ERROR = "ERROR"
    FILE = "FILE"
    CONSOLE = "CONSOLE"

class ErrorLogHandler(BaseLogHandler):

    def __init__(self) -> None:
        super().__init__()
        self.handle_type = RequestType.ERROR

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            pass
        else:
            super().handle(request_type, request)

class ConsoleLogHandler(BaseLogHandler):

    def __init__(self) -> None:
        super().__init__()
        self.handle_type = RequestType.CONSOLE

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            pass
        else:
            super().handle(request_type, request)


class FileLogHandler(BaseLogHandler):

    def __init__(self) -> None:
        super().__init__()
        self.handle_type = RequestType.FILE

    def handle(self, request_type : RequestType, request : str) -> None:
        if self.can_handle(request_type):
            pass
        else:
            super().handle(request_type, request)


