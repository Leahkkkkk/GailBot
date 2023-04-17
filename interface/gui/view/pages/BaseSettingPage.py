
from view.config.Style import STYLE_DATA,  FontFamily
from view.config.Text import ENGINE_SETTING_TEXT as Text
from view.Signals import DataSignal
from view.Request import Request
from gbLogger import makeLogger
from view.widgets import Label, ColoredBtn
from view.widgets.Table import BaseTable 
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout)
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter

class BaseSettingPage(QWidget):
    headerText = None 
    captionText = None 
    mainTable = None 
    signal = None 
    
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        """ initializes class """
        self.logger = makeLogger("F")
        self._initWidget()
        self._initlayout()
        self._connectSignal()
    
    def _initWidget(self):
        self.header = Label(
           self.headerText, STYLE_DATA.FontSize.HEADER2, FontFamily.MAIN
        )
        self.caption = Label(
            self.captionText, STYLE_DATA.FontSize.DESCRIPTION, FontFamily.MAIN
        )
        self.addBtn = ColoredBtn(Text.ADD_BUTTON, STYLE_DATA.Color.PRIMARY_BUTTON)
    
    def _initlayout(self):
        """" initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.setSpacing(STYLE_DATA.Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.caption, alignment=center)
        self.verticalLayout.addSpacing(STYLE_DATA.Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.mainTable, alignment=center)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.addBtn, alignment=center)
        
    def _connectSignal(self):
        self.addBtn.clicked.connect(self.addItem)
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
    
    def changeColor(self):
        self.addBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
    
    def changeFont(self):
        self.header.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.caption.fontChange(STYLE_DATA.FontSize.DESCRIPTION)
        
    def addItem(self):
        pass 
    
    def addSucceed(self, data):
        pass 
