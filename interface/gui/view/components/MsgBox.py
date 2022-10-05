from PyQt6.QtWidgets import QMessageBox

class ConfirmBox:
    def __init__(self, msg:str, confirm):
        self.msgBox = QMessageBox(text=msg)
        self.msgBox.setIcon(QMessageBox.Icon.Warning)
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | 
                                  QMessageBox.StandardButton.No)
        self.msgBox.buttonClicked.connect(self.checkCancel)
        self.confirm = confirm 
        self.msgBox.exec()
    
    def checkCancel(self, button):
        if button.text() == "&No":
            return
        else:
            self.confirm()


class WarnBox:
    def __init__(self, msg:str, ok=None) -> None:
        self.ok = ok
        self.msgBox = QMessageBox(text=msg)
        self.msgBox.setIcon(QMessageBox.Icon.Warning)
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.buttonClicked.connect(self.btnClicked)
        self.msgBox.exec()
    
    def btnClicked(self, button):
        if self.ok:
            self.ok()
