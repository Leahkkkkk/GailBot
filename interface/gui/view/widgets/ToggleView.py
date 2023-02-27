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
from view.widgets import Button, ScrollArea
from util.Style import (
    Color, 
    FontSize, 
    Dimension, 
    StyleSheet
)

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from PyQt6.QtCore import Qt

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
        headercolor = Color.SUB_BACKGROUND, 
        viewcolor = Color.SUB_BACKGROUND,
        *args, 
        **kwargs):
        
        super().__init__(*args, **kwargs)
        self.labelStr = label
        self.view = view
        self.header = header
        self.headercolor = headercolor
        self.viewcolor = viewcolor
        self.setContentsMargins(0,0,0,0)
    
        self._configHeader()
        self._configViewField()
        self._initLayout()
        self._connectSignal()
        self.setScrollHeight(self.view.height())
    
    def setScrollHeight(self, size:int):
        """ public function to resize the scroll area height 
        Args:
        size: the height of the scroll area
        """
        self.scroll.setMinimumHeight(size)
    
    def hideView(self) -> None :
        """ hide the view area """
        self.scroll.hide()
        self.hide = True
        self.Btn.resetBtn()
        
    def _configHeader(self):
        """ configures the toggle header """
        self.Btn = Button.ToggleBtn(text=self.labelStr)
        self.Btn.setStyleSheet(f"{StyleSheet.toggleBtnBasic}"
                               f"background-color: {self.headercolor};"
                               f"font-size: {FontSize.BODY};"
                               f"color:{Color.MAIN_TEXT}")
        if self.header:
            self.Btn.setMinimumWidth(Dimension.TOGGLEBARMAXWIDTH)
        else:
            self.Btn.setMinimumWidth(Dimension.TOGGLEBARMINWIDTH)
       
    def _configViewField(self):
        """ configures the toggle view """
        self.scroll = ScrollArea.ScrollArea()
        self.scroll.setMinimumWidth(self.Btn.width() - Dimension.TOGGLEVIEWOFFSET)
        self.scroll.setMaximumWidth(self.Btn.width())
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.view)
        self.scroll.ensureWidgetVisible(self.view)
        self.scroll.setBaseSize(self.view.width(), self.view.height())
        self.setObjectName("viewWrapper")
        self.scroll.setObjectName("view")
        self.scroll.setStyleSheet(
            f"#viewWrapper, #view {{background-color:{self.viewcolor}; color: {Color.MAIN_TEXT}}}")
        self.view.setObjectName("viewContainer")
        self.view.setStyleSheet(
            f"#viewContainer {{background-color:{self.viewcolor}}}")
        self.scroll.verticalScrollBar().setStyleSheet(f"background-color:{Color.SCROLL_BAR}; border: 1px solid {Color.MAIN_BACKGROUND}")
        self.scroll.hide()
        self.hide = True
        
          
    def _initLayout(self):
        """ initializes the layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(
            self.Btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.scroll)
    
    def _connectSignal(self):
        """ connects signals upon button clicks """
        self.Btn.clicked.connect(self._toggleView)
        
    def _toggleView(self):
        """ sets view for toggle class """
        if self.hide:
            self.scroll.show()
            self.hide = False
        else:
            self.scroll.hide()
            self.hide = True
    

