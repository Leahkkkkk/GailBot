'''
File: WelcomePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:11:47 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import List
from view.config.Style import STYLE_DATA
from view.config.Text import WELCOME_PAGE as Text
from view.config.Text import LINK
from view.widgets import (
    ColoredBtn, 
    Label, 
    Image)
from view.pages.BasicPage import BasicPage

from PyQt6.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QHBoxLayout, 
    QVBoxLayout
)
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class WelcomePage(BasicPage):
    """ class representing the welcome page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
        
    def _initWidget(self):
        """ initialize widgets """
        self._initMainText()
        self._initInstructionText()
        self._initLinkText()
        self._initInstructionGrid()
        self._initLinkText()
        
    def _initLayout(self): 
        """ horizontal layout """
        self.horizontoalBox = QWidget()
        self.horizontalLayout = QHBoxLayout()
        self.horizontoalBox.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.TutorialText,
                                        alignment = Qt.AlignmentFlag.AlignRight)
        self.horizontalLayout.addWidget(self.GuideText)
        
        """ vertical layout """
    
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.logoContainer, alignment=self.logopos)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.WELCOME_TEXT)
        self.verticalLayout.addWidget(self.START, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.StartBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.InstructionText)
        self.verticalLayout.addWidget(self.gridBox)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.ResourcesText)
        self.verticalLayout.addWidget(self.horizontoalBox)
        self.verticalLayout.addWidget(self.MoreInfoText)
        self.verticalLayout.addWidget(self.GBLinkText)
        self.verticalLayout.addStretch()

    def _initStyle(self):
        """ initializes the style  of the page """
        self.StartBtn.setMinimumSize(QtCore.QSize(STYLE_DATA.Dimension.BTNWIDTH, STYLE_DATA.Dimension.BTNHEIGHT))
 
    def _initInstructionText(self):
        """ add widgets for the instructions text and icons """

        """ instruction text """
        self.AudioInstruction = Label(Text.AUDIO_INST, 
                                            STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                                            STYLE_DATA.FontFamily.OTHER, STYLE_DATA.Color.LOW_CONTRAST2)
        
        self.SettingsInstruction = Label(Text.SETTING_INS,
                                               STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                                               STYLE_DATA.FontFamily.OTHER, STYLE_DATA.Color.LOW_CONTRAST2)
        
        self.TranscribeInstruction = Label(Text.TRANSCRIBE_INS, 
                                                 STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                                                 STYLE_DATA.FontFamily.OTHER,
                                                 STYLE_DATA.Color.LOW_CONTRAST2)
        
        self.FileInstruction = Label(Text.FILE_INS, 
                                           STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                                           STYLE_DATA.FontFamily.OTHER,
                                           STYLE_DATA.Color.LOW_CONTRAST2)
        
        self.EditInstruction = Label(Text.EDIT_INS,
                                           STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                                           STYLE_DATA.FontFamily.OTHER,
                                           STYLE_DATA.Color.LOW_CONTRAST2)
        self.insLabels : List[Label]= [
            self.AudioInstruction, 
            self.SettingsInstruction, 
            self.TranscribeInstruction, 
            self.FileInstruction, 
            self.EditInstruction]

        """ instruction icons """
        self.AudioIcon = Image(STYLE_DATA.Asset.instructionSound)
        self.SettingsIcon = Image(STYLE_DATA.Asset.instructionSetting)
        self.TranscribeIcon = Image(STYLE_DATA.Asset.instructionTranscribe)
        self.FileIcon = Image(STYLE_DATA.Asset.instructionFile)
        self.EditIcon = Image(STYLE_DATA.Asset.instructionEdit)
        
      
    def _initInstructionGrid(self):
        """ add a grid layout for the instruction texts and icons """
        self.gridBox = QWidget()
        self.gridLayout = QGridLayout()
        self.gridBox.setLayout(self.gridLayout)
        self.gridLayout.addWidget(self.AudioInstruction, 1, 0, 
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.addWidget(self.AudioIcon, 0, 0,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.gridLayout.addWidget(self.SettingsInstruction, 1, 1, 
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.addWidget(self.SettingsIcon, 0, 1, 
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.gridLayout.addWidget(self.TranscribeInstruction, 1, 2,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.addWidget(self.TranscribeIcon, 0, 2,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.gridLayout.addWidget(self.FileInstruction, 1, 3,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.addWidget(self.FileIcon, 0, 3,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.gridLayout.addWidget(self.EditInstruction, 1, 4,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.addWidget(self.EditIcon, 0, 4,
                                  alignment = Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setRowMinimumHeight(1,50)
        self.gridLayout.setRowMinimumHeight(0,50)


    def _initMainText(self):
        """ initialize the main text on home page  """
        self.WELCOME_TEXT = Label(Text.WELCOME_TEXT, 
                                        STYLE_DATA.FontSize.HEADER1, 
                                        STYLE_DATA.FontFamily.MAIN)
        self.WELCOME_TEXT.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.START = Label(Text.START,
                                       STYLE_DATA.FontSize.BODY, 
                                       STYLE_DATA.FontFamily.OTHER,
                                       STYLE_DATA.Color.GREYDARK)
        
        self.START.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        self.StartBtn = ColoredBtn(Text.START_BTN, STYLE_DATA.Color.SECONDARY_BUTTON)
        
        self.InstructionText = Label(Text.INSTRUCTION_HEADER, STYLE_DATA.FontSize.HEADER2, 
                                           STYLE_DATA.FontFamily.MAIN)
        self.InstructionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
    
        
    def _initLinkText(self):
        """ initializes the link text and functionality """
        self.ResourcesText = Label(Text.RESOURCE_HEADER, STYLE_DATA.FontSize.HEADER2, 
                                         STYLE_DATA.FontFamily.OTHER)
        self.ResourcesText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.TutorialText = Label(LINK.USER_MANUAL, STYLE_DATA.FontSize.LINK,
                                        STYLE_DATA.FontFamily.OTHER, STYLE_DATA.Color.PRIMARY_BUTTON,
                                        STYLE_DATA.StyleSheet.linkStyle, link=True)

        self.GuideText = Label(LINK.TECH_DOC, STYLE_DATA.FontSize.LINK, 
                                        STYLE_DATA.FontFamily.OTHER, STYLE_DATA.Color.PRIMARY_BUTTON,
                                         STYLE_DATA.StyleSheet.linkStyle, link=True)
        self.GBLinkText = Label(LINK.GB_WEB, STYLE_DATA.FontSize.BODY, 
                                      STYLE_DATA.FontFamily.OTHER, STYLE_DATA.Color.PRIMARY_BUTTON, link=True)
        
        self.GBLinkText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.MoreInfoText = Label(Text.MORE_INFO, 
                                        STYLE_DATA.FontSize.SMALL, STYLE_DATA.FontFamily.OTHER)
        
        self.MoreInfoText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        self.buttomText : List[Label] = [self.GuideText, self.TutorialText, self.GBLinkText]
    
    
    def changeColor(self, colormode = None):
        super().changeColor()
        for label in self.insLabels:
            label.colorChange(STYLE_DATA.Color.LOW_CONTRAST2)
        for label in self.buttomText:
            label.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.START.colorChange(STYLE_DATA.Color.GREYDARK)
        self.StartBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        
    def changeFont(self, fontmode = None):
        for label in self.insLabels:
            label.fontChange(STYLE_DATA.FontSize.INSTRUCTION_CAPTION)
        self.WELCOME_TEXT.fontChange(STYLE_DATA.FontSize.HEADER1)
        self.ResourcesText.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.TutorialText.fontChange(STYLE_DATA.FontSize.LINK)
        self.GuideText.fontChange(STYLE_DATA.FontSize.LINK)
        self.GBLinkText.fontChange(STYLE_DATA.FontSize.BODY)
        self.MoreInfoText.fontChange(STYLE_DATA.FontSize.SMALL)
    