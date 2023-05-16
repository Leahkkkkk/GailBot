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
from view.config.Text import MENU_BAR

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QDesktopServices, QAction
from PyQt6.QtCore import QUrl
from view.widgets.MsgBox import WarnBox
import logging

class MenuBar(QMenuBar):
    """ implementation of Gui menu bar, include open and close 
        console option """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # console
        self.Console = QMenu(MENU_BAR.CONSOLE)
        self.OpenConsole = QAction(MENU_BAR.OPEN)
        self.Console.addAction(self.OpenConsole)
        self.CloseConsole = QAction(MENU_BAR.CLOSE)
        self.Console.addAction(self.CloseConsole)
        self.addMenu(self.Console)
       
        # help menu
        self.Help = QMenu(MENU_BAR.HELP)
        self.addMenu(self.Help)
        self.Contact = QAction(MENU_BAR.CONTACT)
        self.BugReport = QAction(MENU_BAR.BUG)
        self.Help.addAction(self.BugReport)
        self.Help.addAction(self.Contact)
        self.Contact.triggered.connect(lambda: self.activateLink(MENU_BAR.EMAIL_LINK))
        self.BugReport.triggered.connect(lambda: self.activateLink(MENU_BAR.BUG_LINK))
    
    
    def activateLink(self, link:str):
        try:
            QDesktopServices.openUrl(QUrl(link))
        except Exception as e:
            logging.error(e)
            WarnBox(MENU_BAR.MAIL_FAILED)
    
    