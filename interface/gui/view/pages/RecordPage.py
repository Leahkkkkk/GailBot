import datetime

from util.Config import Color, FontSize, Dimension, Asset, RecordForm
from util.Config import RecordPageText as Text
from view.style.styleValues import FontFamily 
from view.style.Background import initBackground
from view.widgets import (
    InputBox, 
    Button, 
    Label, 
    ToggleView, 
    TextForm)
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QProgressBar)
from PyQt6.QtCore import Qt, QTimer

center = Qt.AlignmentFlag.AlignHCenter

class RecordProgress(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.recording = False
        self._initWidget()
        self._iniLayout()
        self._initTimer()
        self._connectSignal()
        initBackground(self)
    
    def _initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._ontime)
    
    def _ontime(self):
        """ slot to display timer """
        self.counter += 1
        time = datetime.datetime.fromtimestamp(self.counter/1000).strftime("%M:%S")
        self.timeDisplay.setText(time)
        
    def _initWidget(self):
        """ initialize the widget """
        self.timeDisplay = Label.Label(str(self.counter), FontSize.BODY)
        self.iconBtn = Button.ToggleBtn((Asset.recordStop, Asset.recordPlay))
        self.endBtn  = Button.ColoredBtn(Text.end, Color.ORANGE)
        self.recordBar = ProgressBar()
        self.recordBar.setMinimumWidth(Dimension.PROGRESSBARWIDTH)
        self.recordBar.setMinimumHeight(Dimension.PROGRESSBARHEIGHT)
    
    def _iniLayout(self):
        """ initalize the layout  """
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.horizontalContainer = QWidget()
        self.horizontalContainer.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.iconBtn, alignment=center)
        self.horizontalLayout.addWidget(self.recordBar, alignment=center)
        self.horizontalLayout.addWidget(self.endBtn, alignment=center)
        self.verticalLayout.addWidget(self.timeDisplay, 
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.horizontalContainer)
        self.verticalLayout.addStretch()
    
    def _connectSignal(self):
        """ connecting the button signal """
        self.endBtn.clicked.connect(self.clearTimer)
        self.iconBtn.clicked.connect(self.recordSwitch)
        
    def recordSwitch(self):
        """ start or stop the timer depending on the current recording state """
        if not self.recording: 
            self._startTimer()
        else: 
            self._stopTimer()
        self.recording = not self.recording
        
    def _startTimer(self):
        """ start the timer """
        self.timer.start(1)
    
    def clearTimer(self):
        """ resume the timer """
        self.counter = 0
        self.recording = False
        self.hide()

    def _stopTimer(self):
        """  """
        self.timer.stop()


class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
    
    def start(self):
        self.startTimer(0)


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
        self.recordForm    = TextForm.TextForm(RecordForm)
        self.toggleSetting = ToggleView.ToggleView(Text.recSet, 
                                                   self.recordForm,
                                                   header=True)
        self.testBtn = Button.BorderBtn(Text.test, Color.BLACK)
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
        self.layout.addWidget(self.startRecordBtn,
                              alignment=center)
        self.layout.addWidget(self.cancelBtn,
                              alignment=center)
        self.layout.addStretch()
        initBackground(self)
    
    def _connectSignal(self):
        self.startRecordBtn.clicked.connect(
            self.startRecord)
        self.cancelBtn.clicked.connect(
            self.cancelRecord
        )
        self.recordInprogress.endBtn.clicked.connect(
            self.cancelRecord
        )
        
    def startRecord(self):
        """ handler for start recording """
        self.recordInprogress.recordSwitch()
        self.recordInprogress.show()
        self.recordForm.disableForm()
        
    def cancelRecord(self):
        """ handler for cancel recording """
        self.recordInprogress.hide()
        self.recordInprogress.clearTimer()
        self.recordForm.enableForm()
        

        

