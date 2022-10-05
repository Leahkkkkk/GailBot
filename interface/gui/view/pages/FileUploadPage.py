from PyQt6.QtWidgets import *
from PyQt6 import QtCore

""" class for file upload page """
class FileUploadPage(QWidget):
    """ initialize class """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    """ initialzie widget """
    def _initWidget(self):
        self.label = QLabel("File to Transcribe")
        self.gotoMainBtn = QPushButton("back to main")
        self.uploadFileBtn = QPushButton("Upload File")
        self.transcribeBtn = QPushButton("Transcribe")
        self.settingBtn = QPushButton("⚙")
        self.fileTable = QTableView()
        self.fileTable.setMinimumSize(QtCore.QSize(700, 200))
        self.fileTable.setMaximumSize(QtCore.QSize(1000, 300))
    """ initialize layout """
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.gotoMainBtn)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.uploadFileBtn)
        self.verticalLayout.addWidget(self.transcribeBtn)
        self.verticalLayout.addWidget(self.settingBtn)
        
    