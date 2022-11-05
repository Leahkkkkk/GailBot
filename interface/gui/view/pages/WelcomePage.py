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

import tomli

from util.Style import  Color,  FontSize,  Dimension,  FontFamily,  Asset
from util.Text import WelcomePageText as Text
from view.widgets import (
    Button, 
    Label, 
    Image, 
    Button
)

from view.Text.LinkText import Links

from PyQt6.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QHBoxLayout, 
    QVBoxLayout
)

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

""" TODO: 1. current background is not responsive ;
          2. Links are not clickable
"""
class WelcomePage(QWidget):
    """ class for welcome page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
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
        self.verticalLayout.addWidget(self.HomeSetBtn)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.WelcomeText)
        self.verticalLayout.addWidget(self.CaptionText, 
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
        """ initialize style """
        self.HomeSetBtn.hide()
        self.StartBtn.setMinimumSize(QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))

    
    """ TODO: separate to a different file """   
    def _initInstructionText(self):
        """ add widgets for the instructions text and icon """
        """ instruction text """
        self.AudioInstruction = Label.Label(Text.audioInstructionText, 
                                            FontSize.INSTRUCTION_CAPTION, 
                                            FontFamily.OTHER, Color.GREYMEDIUM2)
        
        self.SettingsInstruction = Label.Label(Text.settingsInstructionText,
                                               FontSize.INSTRUCTION_CAPTION, 
                                               FontFamily.OTHER, Color.GREYMEDIUM2)
        
        self.TranscribeInstruction = Label.Label(Text.transcribeInstructionText, 
                                                 FontSize.INSTRUCTION_CAPTION, 
                                                 FontFamily.OTHER,
                                                 Color.GREYMEDIUM2)
        
        self.FileInstruction = Label.Label(Text.fileInstructionText, 
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)
        
        self.EditInstruction = Label.Label(Text.editInstructionText,
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)


        """ instruction icons """
        self.AudioIcon = Image.Image(Asset.instructionSound)
        self.SettingsIcon = Image.Image(Asset.instructionSetting)
        self.TranscribeIcon = Image.Image(Asset.instructionTranscribe)
        self.FileIcon = Image.Image(Asset.instructionFile)
        self.EditIcon = Image.Image(Asset.instructionEdit)
        
      
 
    def _initInstructionGrid(self):
        """ add a grid layout for the instruction """
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
        self.WelcomeText = Label.Label(Text.welcomeText, 
                                        FontSize.HEADER1, 
                                        FontFamily.MAIN)
        self.WelcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.CaptionText = Label.Label(Text.captionText,
                                       FontSize.BODY, 
                                       FontFamily.OTHER,
                                       Color.GREYMEDIUM2)
        
        self.CaptionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.HomeSetBtn = Button.ColoredBtn("⚙", Color.BLUEMEDIUM,"35px")
        self.StartBtn = Button.ColoredBtn(Text.startBtnText, Color.GREEN)
        
        self.InstructionText = Label.Label(Text.instructionText, FontSize.HEADER2, 
                                           FontFamily.MAIN)
        self.InstructionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
    
        
    """ TODO: put the link onto separate file """
    def _initLinkText(self):
        """ initialize the link text on homepage """
        self.ResourcesText = Label.Label(Text.resourcesText, 
                                         FontSize.HEADER2, 
                                         FontFamily.OTHER)
        self.ResourcesText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.TutorialText = Label.Label(Links.tutorialLink, FontSize.LINK,
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;", link=True)
        print(Links.tutorialLink)
        
        self.GuideText = Label.Label(Links.guideLink, FontSize.LINK, 
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;", link=True)
        self.GBLinkText = Label.Label(Links.gbWebLink, FontSize.BODY, 
                                      FontFamily.OTHER, Color.BLUEMEDIUM, link=True)
        
        self.GBLinkText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.MoreInfoText = Label.Label(Text.moreInfoText, 
                                        FontSize.SMALL, FontFamily.OTHER)
        
        self.MoreInfoText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
