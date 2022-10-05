""" Logger.py 
For manage logger
"""

from distutils.log import WARN
import logging
import re
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import datetime

current_time = datetime.datetime.now()

""" return a logger with source set as source:str """
def makeLogger(source:str):
    logExtra = {"source": source}
    logger = logging.getLogger()
    logger = logging.LoggerAdapter(logger, logExtra)
    return logger

""" formatter for log file """
class CustomFileFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = "Backend"
        return super().format(record)

""" formatter for console log """
class ConsoleFormatter(logging.Formatter):
    def __init__(self, fmt):
        div = "</div>"
        grey = "<div style='color: grey'>"
        blue = "<div style='color: blue'>"
        orange = "<div style='color: #FFA500'>"
        red = "<div style='color: red'>" 
        super().__init__()
        self.fmt = fmt

        self.FORMATS = {
            logging.DEBUG: grey + self.fmt + div,
            logging.INFO: blue + self.fmt + div,
            logging.WARNING: orange + self.fmt + div,
            logging.ERROR: red + self.fmt + div,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

""" formatter for status bar """
class StatusBarFormatter(logging.Formatter):
    def __init__(self, fmt):
        self.fmt = fmt
        self.warn = "⚠ "
        self.error = "! "
        self.FORMATS = {
            logging.WARNING: self.warn + self.fmt,
            logging.ERROR: self.error + self.fmt,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

""" 
logging handler that shows the log message in a qt console and a file 
"""
class ConsoleHandler(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)
    def __init__(self, TextWidget):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = TextWidget
        self.appendPlainText.connect(self.widget.appendHtml)
        fmt = " %(source)s | %(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s "
        self.setFormatter(ConsoleFormatter(fmt))
        self._initLogFile(fmt)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)
    
    def _initLogFile(self,fmt):
        fh = logging.FileHandler(f"GailBot-GUI-Log-Report-{current_time}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(CustomFileFormatter(fmt))
        logging.getLogger().addHandler(fh)
        
"""
logging handler that shows log message above warning level in status bar 
"""       
class StatusBarHandler(logging.Handler, QtCore.QObject):
    addStatusMsg = QtCore.pyqtSignal(str)
    def __init__(self, showMsgFun):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.showMsg = showMsgFun
        self.addStatusMsg.connect(self.showMsg)
        fmt = "%(levelname)s | %(message)s"
        self.setFormatter(StatusBarFormatter(fmt))
        self.setLevel(logging.WARNING)
    
    def emit(self, record):
        msg = self.format(record)
        self.addStatusMsg.emit(msg)