
from util.Config import Color, FontSize, Dimension
from util.Config import RecordPageText as Text
from view.style.styleValues import FontFamily 
from view.style.Background import initBackground
from view.widgets import InputBox, Button, Label, ToggleView

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt6.QtCore import Qt

center = Qt.AlignmentFlag.AlignHCenter



class RecordProgress(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._iniLayout()
        self._connectSignal()
        initBackground(self)
    
    def _initWidget(self):
        self.iconBtn = Button.ToggleBtn(("stop.png", "play.png"))
        self.endBtn  = Button.ColoredBtn(Text.end, Color.ORANGE)
        self.recordBar = ProgressBar()
        self.recordBar.setMinimumWidth(Dimension.PROGRESSBARWIDTH)
        self.recordBar.setMinimumHeight(Dimension.PROGRESSBARHEIGHT)
    
    def _iniLayout(self):
        self.horizontalLayout = QHBoxLayout()
        self.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.iconBtn, alignment=center)
        self.horizontalLayout.addWidget(self.recordBar, alignment=center)
        self.horizontalLayout.addWidget(self.endBtn, alignment=center)
    
    def _connectSignal(self):
        self.endBtn.clicked.connect(lambda: self.hide())
        


class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
    
    def start(self):
        self.startTimer(20)
        
            


class RecordPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
    def _initWidget(self):
        self.header = Label.Label(Text.record, 
                                  FontSize.HEADER2, 
                                  FontFamily.MAIN)
        self.recordForm = RecordForm(parent=self)
        self.toggleSetting = ToggleView.ToggleView(Text.recSet, 
                                                   self.recordForm,
                                                   header=True)
        self.testBtn = Button.BorderBtn(Text.test, "#000")
        self.startRecordBtn = Button.ColoredBtn(Text.start, Color.GREEN)
        self.cancelBtn = Button.ColoredBtn(Text.cancel, Color.ORANGE)
        self.recordInprogress =  RecordProgress()
        self.recordInprogress.hide()

    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.header, 
                              alignment=center)
        self.layout.addWidget(self.toggleSetting,
                            alignment=center)
        self.layout.addStretch()
        self.layout.addWidget(self.recordInprogress)
        self.layout.addWidget(self.testBtn,
                              alignment=center)
        self.layout.addWidget(self.startRecordBtn,
                              alignment=center)
        self.layout.addWidget(self.cancelBtn,
                              alignment=center)
        initBackground(self)
    
    def _connectSignal(self):
        self.startRecordBtn.clicked.connect(
            lambda: self.recordInprogress.show())
        self.startRecordBtn.clicked.connect(
            lambda: self.recordInprogress.recordBar.start())
        self.cancelBtn.clicked.connect(
            lambda: self.recordInprogress.hide())
        
        

class RecordForm(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        self.basicLabel = Label.Label(Text.basic, FontSize.BODY, FontFamily.MAIN)
        self.basicInput = InputBox.InputBox(Text.filename)
        self.audioCombo = InputBox.InputCombo([Text.mp3, Text.wav], Text.format)
        self.advancedLabel = Label.Label(Text.advanced,
                                         FontSize.BODY, 
                                         FontFamily.MAIN)
        self.recordingRate = InputBox.InputBox(Text.rate)
        self.maxDuration = InputBox.InputBox(Text.duration)
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.basicLabel)
        self.layout.addWidget(self.basicInput)
        self.layout.addWidget(self.audioCombo)
        self.layout.addWidget(self.advancedLabel)
        self.layout.addWidget(self.recordingRate)
        self.layout.addWidget(self.maxDuration)

        
        