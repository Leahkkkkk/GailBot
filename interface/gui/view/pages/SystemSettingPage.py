import tomli

from util.Config import Color, FontSize, SystemSettingForm, About, StyleSheet
from util.Config import SystemSetPageText as Text 
from util.Config import FontSize as FS 
from util.Config import StyleSheet as ass
from view.widgets import SideBar, SettingForm,  Label, Button
from view.style.Background import initBackground
from view.style.styleValues import  FontSize
from view.Text.LinkText import Links

from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QStackedWidget)
from PyQt6.QtCore import Qt

bottom = Qt.AlignmentFlag.AlignBottom
class SystemSettingPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        initBackground(self)
        self.data = SystemSettingForm
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
    def _initWidget(self):
        """initialize widgets"""
        self.sideBar = SideBar.SideBar()
       
        self.Mainstack = QStackedWidget()
        self.SysSet = SettingForm.SettingForm(
            Text.header, self.data, Text.caption)
        self.Mainstack.addWidget(self.SysSet)
        self.GuideLink = Label.Label(Links.guideLink, FontSize.LINK, link=True)
        self.cancelBtn = Button.BorderBtn(
            Text.cancelBtn, Color.ORANGE)
        self.saveBtn = Button.ColoredBtn(
            Text.saveBtn, Color.GREEN)
        self.versionLabel = Label.Label(About.version, FontSize.SMALL)
        self.copyRightLabel = Label.Label(About.copyRight, FontSize.SMALL)
        
        self.sideBar.addStretch()
        self.sideBar.addWidget(self.saveBtn)
        self.sideBar.addWidget(self.cancelBtn)
        self.sideBar.addStretch()
        self.sideBar.addWidget(self.GuideLink, alignment=bottom)
        self.sideBar.addWidget(self.versionLabel, alignment=bottom)
        self.sideBar.addWidget(self.copyRightLabel, alignment=bottom)
        
        
    def _initLayout(self):
        """ initialize layout"""
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        
        self.setLayout(self.horizontalLayout)
        """ add widget to layout """
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.Mainstack)

    def _initStyle(self):
        self.Mainstack.setObjectName(StyleSheet.sysSettingStackID)
        """ add this to an external stylesheet"""
        self.Mainstack.setStyleSheet(StyleSheet.sysSettingStack)
   
    def setValue(self, values:dict):
        self.SysSet.setValue(values)
    
    def getValue(self) -> dict:
        return self.SysSet.getValue()

    