from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from view.components import MsgBox
from util import Path
import os 

""" class for transcription in progress page """
class TranscribeProgressPage(QWidget):
    """ initialize class """
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initstyle()
        self._initLayout()
        self._connectSignal()
        self.parent = parent
    """ start loading icon movie """
    def loadStart(self):
        self.IconImg.start()
    """ stop loading icon movie """
    def loadStop(self):
        self.IconImg.stop()
    """ initialize widgets """
    def _initWidget(self):
        self.label = QLabel("Transcribe in Progress")
        self.loadIcon = QLabel()
        self.IconImg = QMovie(os.path.join(Path.get_project_root(), "view/asset/gbloading.gif"))
        self.loadIcon.setMovie(self.IconImg)
        self.loadIcon.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.loadStart()
        self.cancelBtn = QPushButton("Cancel")
    """ styles loading icon movie """
    def _initstyle(self):
        self.loadIcon.setMinimumSize(QtCore.QSize(150, 150))
        self.loadIcon.setMaximumSize(QtCore.QSize(150, 150))
        self.loadIcon.setScaledContents(True)
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    """ intiializes layout """
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.loadIcon)
        self.verticalLayout.addWidget(self.cancelBtn)
    """ connects signal """
    def _connectSignal(self):
        self.cancelBtn.clicked.connect(self._confirm)
    """ handles confirm transcription message box """
    def _confirm(self):
        self.confirmCancel = MsgBox.ConfirmBox("Confirm Cancel?", 
                                               self.parent.confirmCancel)
        

        
    