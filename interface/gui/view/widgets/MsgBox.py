'''
File: MsgBox.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 10:18:15 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from util.Logger import makeLogger
from view.style.Background import initBackground
from util.SytemSet import SysColor, SysStyleSheet
from PyQt6.QtWidgets import QMessageBox


loggger = makeLogger("Frontend")
class ConfirmBox:
    """ create and display a Confirm box """
    def __init__(self, msg: str, confirm: callable):
        """ A confirm box 
        
        Args:
            msg (str): message displayed in the box
            confirm (function): function get called when the confirmation 
                                is made
        """
        self.msgBox = QMessageBox(text=msg)
        self.msgBox.setIcon(QMessageBox.Icon.Warning)
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | 
                                  QMessageBox.StandardButton.No)
        self.msgBox.buttonClicked.connect(self._confirm)
        self.confirm = confirm 
        initBackground(self.msgBox, color = SysColor.subBackground)
        self.msgBox.exec()
        
    
    def _confirm(self, button):
        """ Check and handle user's confrimation 
        
        Args:
            button (QButton)
        """
        loggger.info("confirm message box buttonc click")
        if button.text() == "&No":
            return
        else:
            loggger.info("confirmed") 
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
        initBackground(self.msgBox, color= SysColor.subBackground)
        self.msgBox.exec()
        
    
    def _ok(self, button):
        """ handle event when button is clicked 

        Args:
            button (QButton)
        """
        if self.ok:
            self.ok()


