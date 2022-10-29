import tomli

from view.style.styleValues import FontFamily, FontSize, Color, Dimension
from view.style.Background import initBackground
from view.widgets import InputBox, Button, Label, ToggleView
from view.pages import RecordInProgress

from PyQt6.QtWidgets import QWidget, QVBoxLayout,QSpacerItem, QComboBox
from PyQt6.QtCore import Qt


class RecordPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initConfig()
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        self.header = Label.Label("Record Audio File", 
                                  self.config["fontSizes"]["HEADER2"], 
                                  FontFamily.MAIN)
        self.recordForm = RecordForm(parent=self)
        self.toggleSetting = ToggleView.ToggleView("Recording Settings", 
                                                   self.recordForm,
                                                   header=True)
        self.testBtn = Button.BorderBtn("Test MicroPhone", "#000")
        self.startRecordBtn = Button.ColoredBtn("Start Recording", self.config["colors"]["GREEN"])
        self.cancelBtn = Button.ColoredBtn("Cancel", self.config["colors"]["ORANGE"])
        self.startRecordBtn.clicked.connect(self._startRecord)
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.header, 
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.header.setContentsMargins(0,20,0,40)
        self.layout.addWidget(self.toggleSetting,
                            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addStretch()
        self.layout.addWidget(self.testBtn,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.startRecordBtn,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.cancelBtn,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.testBtn.setFixedSize(Dimension.BGBUTTON)
        self.startRecordBtn.setFixedSize(Dimension.BGBUTTON)
        self.cancelBtn.setFixedSize(Dimension.BGBUTTON)
        self.spacer = QSpacerItem(200,150)
        self.layout.addItem(self.spacer)
        self.cancelBtn.setContentsMargins(0,10,0,150)
        initBackground(self)
    
    
    def _startRecord(self):
        self.recordDialog = RecordInProgress.RecordDialog()
        self.recordDialog.exec()

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
        
        

class RecordForm(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initConfig()
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        self.basicLabel = Label.Label("Basic", self.config["fontSizes"]["BODY"], FontFamily.MAIN)
        self.basicInput = InputBox.InputBox("Filename")
        self.audioCombo = InputBox.InputCombo(["MP3", "WAV"], "Audio Format")
        self.advancedLabel = Label.Label("Advanced",
                                         self.config["fontSizes"]["BODY"], 
                                         FontFamily.MAIN)
        self.recordingRate = InputBox.InputBox("Recording Rate (Hertz)")
        self.maxDuration = InputBox.InputBox("Max Recording Duration")
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.basicLabel)
        self.layout.addWidget(self.basicInput)
        self.layout.addWidget(self.audioCombo)
        self.layout.addWidget(self.advancedLabel)
        self.layout.addWidget(self.recordingRate)
        self.layout.addWidget(self.maxDuration)

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
        
        
        
