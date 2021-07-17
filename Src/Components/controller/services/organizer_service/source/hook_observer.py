# Standard imports
from typing import Dict, Any
# Local imports
from ......utils.observer import Subscriber
from ......utils.logger import BaseLogHandler
from .source_logs import RequestType

class SourceHookObserver(Subscriber):
    """
    Subscriber for a SourceHook object.
    """

    def __init__(self, logger : BaseLogHandler) -> None:
        self.logger = logger

    def handle(self, event_type : str,  data : Dict[str,Any]) -> None:
        """
        Logs the event of the source hook to file.
        """
        msg = "source hook event of type: {} with data: {}".format(
            event_type,data)
        self.logger.handle(RequestType.FILE,msg)
