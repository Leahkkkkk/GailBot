# Standard imports
from typing import Any
from abc import ABC, abstractmethod
# Local imports

class LogRequestType:
    pass

class BaseLogHandler(ABC):

    def __init__(self) -> None:
        self.next : BaseLogHandler = None
        self.handle_type = None

    def handle(self, request_type : LogRequestType, request : Any) -> None:
        if self.next != None:
            self.next.handle(request_type, request)

    def can_handle(self, request_type :  LogRequestType) -> bool:
        return request_type == self.handle_type

    def set_next(self, handler : Any) -> None:
        self.next = handler



