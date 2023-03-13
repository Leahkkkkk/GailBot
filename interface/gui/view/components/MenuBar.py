'''
File: MenuBar.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 10:17:30 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the menu bar 
'''
from view.config.Text import MenuBarText

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QDesktopServices, QAction
from PyQt6.QtCore import QUrl
from view.widgets.MsgBox import WarnBox
import logging

class ManuBar(QMenuBar):
    """ implementation of Gui menu bar, include open and close 
        console option """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # console
        self.Console = QMenu(MenuBarText.console)
        self.OpenConsole = QAction(MenuBarText.open)
        self.Console.addAction(self.OpenConsole)
        self.CloseConsole = QAction(MenuBarText.close)
        self.Console.addAction(self.CloseConsole)
        self.addMenu(self.Console)
       
        # help menu
        self.Help = QMenu(MenuBarText.help)
        self.addMenu(self.Help)
        self.Contact = QAction(MenuBarText.contact)
        self.Contact.triggered.connect(lambda: self.activateLink(MenuBarText.email))
        self.BugReport = QAction(MenuBarText.bugreport)
        self.Help.addAction(self.BugReport)
        self.Help.addAction(self.Contact)
        self.BugReport.triggered.connect(lambda: self.activateLink(MenuBarText.buglink))
    
    
    def activateLink(self, link:str):
        try:
            QDesktopServices.openUrl(QUrl(link))
        except Exception as e:
            logging.error(e)
            WarnBox(MenuBarText.mailFailed)
    
    