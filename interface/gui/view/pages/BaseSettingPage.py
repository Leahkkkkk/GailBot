'''
File: BaseSettingPage.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: The base class of setting page  
'''
from view.config.Style import STYLE_DATA,  FontFamily
from view.widgets.Button import InstructionBtn
from view.signal.interface import DataSignal
from view.Request import Request
from gbLogger import makeLogger
from view.widgets import Label, ColoredBtn
from view.widgets.Table import BaseTable 
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter

class BaseSettingPage(QWidget):
    headerText = None 
    captionText = None 
    addNewButtonText = None
    mainTable:BaseTable = None 
    signal: DataSignal = None 
    instruction = {}  
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        """ initializes class """
        self.logger = makeLogger()
        self._initWidget()
        self._initlayout()
        self._connectSignal()
    
    def _initWidget(self):
        self.header = Label(
           self.headerText, STYLE_DATA.FontSize.HEADER2, FontFamily.MAIN
        )
        self.caption = Label(
            self.captionText, STYLE_DATA.FontSize.DESCRIPTION, FontFamily.MAIN, others="text-align: center;"
        )
        self.caption.setAlignment(center)
        self.caption.setMinimumWidth(STYLE_DATA.Dimension.FORMWIDTH)
        self.addBtn = ColoredBtn(self.addNewButtonText, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.instruction = InstructionBtn(self.instruction)
        
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
        self.verticalLayout.addWidget(self.instruction, alignment= Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignAbsolute)
        
    def _connectSignal(self):
        self.addBtn.clicked.connect(self.addItem)
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
    
    def changeColor(self):
        self.addBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
    
    def changeFont(self):
        self.header.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.caption.fontChange(STYLE_DATA.FontSize.DESCRIPTION)
        
    def addSucceed(self, data):
        name, setting = data
        self.mainTable.addItem(data)
        self.signal.addSucceed.emit(name)
    
    def sendAddRequest(self, data):
        self.signal.postRequest.emit(
            Request(data=data, succeed=self.addSucceed))
    
    def addItem(self):
        pass 
   