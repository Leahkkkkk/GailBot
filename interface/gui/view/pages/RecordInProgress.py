from view.widgets import Button, Label
from view.style.styleValues import Color, FontFamily, FontSize, Dimension
from view.style.Background import initBackground, initImgBackground

from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import QSize, Qt



class RecordDialog(QDialog):
    def __init__(self, 
                 *args, 
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(QSize(600, 400))
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.startBtn = Button.ColoredBtn("Start Reecording", Color.GREEN)
        self.startBtn.setFixedSize(Dimension.BGBUTTON)
      
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE)
        self.cancelBtn.setFixedSize(Dimension.BGBUTTON)
        
        self.endBtn = Button.ColoredBtn("End Recording", Color.ORANGE)
        self.endBtn.setFixedSize(Dimension.BGBUTTON)
        self.iconBtn = Button.ToggleBtn(("stop.png", "play.png"), minHeight=200)
        # self.iconBtn.setFixedSize(QSize(200,200))
        self.iconBtn.setMinimumHeight(80)
        self.iconBtn.hide()
        self.endBtn.hide()
        
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        

    def _initLayout(self):
        self.layout.addWidget(self.startBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|
                                                 Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.iconBtn, 3,
                              alignment = Qt.AlignmentFlag.AlignHCenter|
                                                 Qt.AlignmentFlag.AlignVCenter)
        
        self.layout.addWidget(self.endBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|
                                                 Qt.AlignmentFlag.AlignVCenter)
     
        self.layout.addWidget(self.cancelBtn,
                                      alignment = Qt.AlignmentFlag.AlignRight)
    

    def _initStyle(self):
        initBackground(self)
        # initImgBackground(self)
        
        # self.setStyleSheet("border: 1px solid black")
        
    
    def _connectSignal(self):
        self.startBtn.clicked.connect(self.startBtn.hide)
        self.endBtn.clicked.connect(self.endBtn.hide)
        self.startBtn.clicked.connect(self.iconBtn.show)
        self.startBtn.clicked.connect(self.endBtn.show)
        
        self.endBtn.clicked.connect(self.startBtn.show)
        self.endBtn.clicked.connect(self.iconBtn.hide)
        
        self.cancelBtn.clicked.connect(self.close)