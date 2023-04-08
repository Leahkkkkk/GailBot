'''
File: ToggleView.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:43:52 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a toggle widget with the functionalities to hide and show 
             a view object 
'''
from .Button import ToggleBtn
from .ScrollArea import ScrollArea
from .Background import initPrimaryColorBackground, initSecondaryColorBackground
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject

#### controlling style changes 
from view.config.Style import STYLE_DATA 
from view.Signals import GlobalStyleSignal

######################
class Signal(QObject):
    showview = pyqtSignal()
class ToggleView(QWidget):
    """ 
    A toggle view widget that shows and hides content,
    the content is passed in as a widget 

    Constructor Args:
        label(str):  the label that will displayed on the toggle bar
        view(object): the content that will be toggled 
        header(bool): if set to true, the width of the label will be wider
    """
    
    def __init__(
        self, 
        label:str, 
        view: QWidget, 
        header = False, 
        secondaryStyle = True,
        *args, 
        **kwargs):
        
        super().__init__(*args, **kwargs)
        QObject.__init__(self)
        self.labelStr = label
        self.view = view
        self.header = header
        self.secondaryStyle = secondaryStyle
        if secondaryStyle:
            self.headercolor = STYLE_DATA.Color.SUB_BACKGROUND
            self.viewcolor = STYLE_DATA.Color.SUB_BACKGROUND
        else:
            self.headercolor = STYLE_DATA.Color.MAIN_BACKGROUND
            self.viewcolor = STYLE_DATA.Color.MAIN_BACKGROUND
            
        self.signal = Signal() 
        self.setContentsMargins(0,0,0,0)
        self._configHeader()
        self._configViewField()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        self._scroll.setMaximumHeight(self.view.height())
    
    def setScrollHeight(self, size:int):
        """ public function to resize the _scroll area height 
        Args:
        size: the height of the _scroll area
        """
        self._scroll.setMinimumHeight(size)
    
    def hideView(self) -> None :
        """ hide the view area """
        self._scroll.hide()
        self.hide = True
        self.Btn.resetBtn()
    
    def colorChange(self):
        if self.secondaryStyle:
            self.headercolor = STYLE_DATA.Color.SUB_BACKGROUND
            self.viewcolor = STYLE_DATA.Color.SUB_BACKGROUND
        else:
            self.headercolor = STYLE_DATA.Color.MAIN_BACKGROUND
            self.viewcolor = STYLE_DATA.Color.MAIN_BACKGROUND
        self._initStyle()
         
    def _configHeader(self):
        """ configures the toggle header """
        self.Btn = ToggleBtn(text=self.labelStr)
        if self.header:
            self.Btn.setMinimumWidth(STYLE_DATA.Dimension.TOGGLEBARMAXWIDTH)
        else:
            self.Btn.setMinimumWidth(STYLE_DATA.Dimension.TOGGLEBARMINWIDTH)
       
    def _configViewField(self):
        """ configures the toggle view """
        self._scroll = ScrollArea()
        self._scroll.setMinimumWidth(self.Btn.width() - STYLE_DATA.Dimension.TOGGLEVIEWOFFSET)
        self._scroll.setMaximumWidth(self.Btn.width())
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self.view)
        self._scroll.ensureWidgetVisible(self.view)
        self._scroll.setBaseSize(self.view.width(), self.view.height())
        self._scroll.hide()
        self.hide = True
        
    def _initStyle(self):
        self.Btn.setStyleSheet(STYLE_DATA.StyleSheet.toggleBtnBasic + \
                                f"background-color:{self.headercolor};" + \
                                f"color: {STYLE_DATA.Color.MAIN_TEXT}")
        self._scroll.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        if self.secondaryStyle:
            initSecondaryColorBackground(self._scroll)
            initSecondaryColorBackground(self.view)
        else:
            initPrimaryColorBackground(self._scroll)
            initPrimaryColorBackground(self.view)
          
    def _initLayout(self):
        """ initializes the layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(
            self.Btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self._scroll)
    
    def _connectSignal(self):
        """ connects signals upon button clicks """
        self.Btn.clicked.connect(self._toggleView)
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        
    def _toggleView(self):
        """ sets view for toggle class """
        if self.hide:
            self._scroll.show()
            self.signal.showview.emit()
            self.hide = False
        else:
            self._scroll.hide()
            self.hide = True
    

