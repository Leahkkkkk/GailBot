'''
File: MsgBox.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 10:18:15 am
Modified By:  Siara Small  & Vivian Li
-----
Description implement pop up message dialogue to display message for user
'''
from typing import List 
from util.Style import Color
from util.Logger import makeLogger
from view.widgets.Background import initSecondaryColorBackground
from PyQt6.QtWidgets import QMessageBox


class ConfirmBox:
    """ create and display a Confirm box """
    def __init__(
        self, 
        msg: str, 
        confirm: callable, 
        confirmButton: QMessageBox.standardButton = QMessageBox.StandardButton.Yes):
        """ A confirm box 
        
        Args:
            msg (str): message displayed in the box
            confirm (function): function get called when the confirmation 
                                is made
        """
        self.logger = makeLogger("Frontend")
        self.msgBox = QMessageBox(text=msg)
        self.msgBox.setStyleSheet(f"color:{Color.MAIN_TEXT};")
        self.msgBox.setIcon(QMessageBox.Icon.Warning)
        
       
        self.msgBox.setStandardButtons(
            confirmButton| QMessageBox.StandardButton.Cancel)
        self.msgBox.buttonClicked.connect(self._confirm)
        self.confirm = confirm 
        initSecondaryColorBackground(self.msgBox)
        self.msgBox.exec()
        
    
    def _confirm(self, button):
        """ Check and handle user's confirmation 
        
        Args:
            button (QButton)
        """
        self.logger.info("confirm message box button click")
        if button.text() == "Cancel":
            return
        else:
            self.logger.info("confirmed") 
            self.confirm()


class WarnBox:
    """ create and display a warning box """
    def __init__(self, msg:str, ok : callable = None) -> None:
        """ A Warning box
        
        Args:
            msg (str): message displayed in the box
            ok (function, optional): function get called when user click 
                                     okay button
        """
        self.ok = ok
        self.msgBox = QMessageBox(text=msg)
        self.msgBox.setIcon(QMessageBox.Icon.Warning)
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.buttonClicked.connect(self._ok)
        self.msgBox.setStyleSheet(f"color:{Color.MAIN_TEXT};")
        
        initSecondaryColorBackground(self.msgBox)
        self.msgBox.exec()
        
    
    def _ok(self, button):
        """ handle event when button is clicked 
        Args:
            button (QButton)
        """
        if self.ok:
            self.ok()


