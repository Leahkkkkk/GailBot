'''
File: Logger.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 3:09:55 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: 
'''
import os
import datetime
import logging
import re

from view.config import getWorkPaths
from PyQt6 import QtCore
from PyQt6.QtWidgets import QLineEdit

current_time = datetime.datetime.now()
fileHandlerAdded = False

def makeLogger(source:str = None ):
    """ return a logger that specifies the source of the log information
    
    Args:
        source(str): indicates the source of the log, 
                     either "Backend" or "Frontend"
    """
    source = "Frontend"
    logger = logging.getLogger()
    # create log file handler
    global fileHandlerAdded
    logdir = getWorkPaths().frontendLogFiles
    print(f"log files {logdir}")
    filePath = os.path.join(logdir, f"GailBot-GUI-Log-Report-{current_time}.log")
    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    if not fileHandlerAdded:
        fmt = " %(source)s |  %(lineno)s | %(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s "
        if not os.path.isfile(filePath):
            f = open(filePath, "w+")
            f.close()
        fh = logging.FileHandler(filePath)
        fh.setFormatter(CustomFileFormatter(fmt))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logging.getLogger().addHandler(fh)
        fileHandlerAdded = True
    logExtra = {"source": source}
    logger = logging.LoggerAdapter(logger, logExtra)
    return logger

class CustomFileFormatter(logging.Formatter):
    """ formatter for log file """
    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = "Backend"
        return super().format(record)

class ConsoleFormatter(logging.Formatter):
    """ formatter for console log """
    def __init__(self, fmt):
        div = "</div>"
        grey = "<div style='color: grey'>"
        blue = "<div style='color: blue'>"
        orange = "<div style='color: #FFA500'>"
        red = "<div style='color: red'>" 
        super().__init__()
        self.fmt = fmt

        self.FORMATS = {
            logging.DEBUG: f"{grey}{self.fmt}{div}",
            logging.INFO: f"{blue}{self.fmt}{div}",
            logging.WARNING: f"{orange}{self.fmt }{div}",
            logging.ERROR: f"{red}{self.fmt}{div}",
        }

    def format(self, record):
        """ return a formatted logging string  """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class StatusBarFormatter(logging.Formatter):
    """ formatter for status bar """
    def __init__(self, fmt):
        self.fmt = fmt
        self.warn = "\u26A0"
        self.error = "\u2757"
        self.FORMATS = {
            logging.WARNING: f"{self.warn}{self.fmt}",
            logging.ERROR: f"{self.error}{self.fmt}",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class ConsoleHandler(logging.Handler, QtCore.QObject):
    """ logging handler that shows the log message in a qt console and a file 
    
    Args:
        TextWidget( QLineEdit ): 
            the widget that the log message will be displayed 
    """
    appendPlainText = QtCore.pyqtSignal(str)
    def __init__(self, TextWidget:QLineEdit):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = TextWidget
        self.appendPlainText.connect(self.widget.appendHtml)
        fmt = " %(source)s |  %(lineno)s | %(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s "
        self.setFormatter(ConsoleFormatter(fmt))
        self.setLevel(logging.INFO)

    def emit(self, record):
        """ display log changes """
        msg = self.format(record)
        self.appendPlainText.emit(msg)
        
        
class StatusBarHandler(logging.Handler, QtCore.QObject):
    """ logging handler that send log message above warning level 
        
    Args: 
        showMsgFun: a handler function that takes in the log message 
                    as argument 
    """ 
    addStatusMsg = QtCore.pyqtSignal(str)
    def __init__(self, showMsgFun:callable):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.showMsg = showMsgFun
        self.addStatusMsg.connect(self.showMsg)
        fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
        self.setFormatter(StatusBarFormatter(fmt))
        self.setLevel(logging.WARNING)
    
    def emit(self, record):
        """ handling log message """
        msg = self.format(record)
        self.addStatusMsg.emit(msg)