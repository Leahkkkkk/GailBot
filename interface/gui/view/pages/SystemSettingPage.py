

from view.widgets import Label,TextForm
from view.style.Background import initBackground
from model.dummySettingData import dummySystemSettingForm
from view.style.styleValues import FontFamily, FontSize

from PyQt6.QtWidgets import QWidget, QVBoxLayout,QScrollArea
from PyQt6.QtCore import Qt


class SystemSettingPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, data=dummySystemSettingForm, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        initBackground(self)
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """initialize widgets"""
        self.header = Label.Label("System Setting",
                                  FontSize.HEADER2,FontFamily.MAIN)
        self.caption = Label.Label("These settings are applied for system setting",
                                   FontSize.DESCRIPTION, FontFamily.MAIN)
        self.PostSet = TextForm.TextForm(self.data)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget( self.PostSet)
        self.scroll.setFixedWidth(600)
        self.PostSet.setFixedWidth(600)
        self.scroll.setMaximumHeight(750)
        self.scroll.setMinimumHeight(430)
 
    def _initLayout(self):
        """ initialize layout"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.header, stretch= 1, alignment=Qt.AlignmentFlag.AlignHCenter
                                                    |Qt.AlignmentFlag.AlignTop)
        # self.layout.addWidget(self.caption,alignment=Qt.AlignmentFlag.AlignCenter)
        self.caption.setContentsMargins(80,0,0,0)
        self.layout.addWidget(self.scroll,stretch = 7, alignment=Qt.AlignmentFlag.AlignHCenter
                                                    |Qt.AlignmentFlag.AlignTop)
    
    def setValue(self, values:dict):
        self.PostSet.updateValues(values)
    
    def getValue(self) -> dict:
        return self.PostSet.getValue()
        
       
    