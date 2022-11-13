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

from util.Style import  (
    Color,  
    Dimension,  
    FontFamily,  
    Asset,
    StyleSheet
)
from util.Style import FontSize as FS
from util.Text import WelcomePageText as Text
from util.Text import Links
from view.widgets import (
    Button, 
    Label, 
    Image, 
    Button
)


from view.widgets.Background import addLogo

from PyQt6.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QHBoxLayout, 
    QVBoxLayout
)
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class WelcomePage(QWidget):
    """ class representing the welcome page """
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
        addLogo(self.verticalLayout)
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
        """ initializes the style  of the page """
        self.StartBtn.setMinimumSize(QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))

    
    """ TODO: separate to a different file """   
    def _initInstructionText(self):
        """ adds widgets for the instructions text and icons """

        """ instruction text """
        self.AudioInstruction = Label.Label(Text.audioInstructionText, 
                                            FS.INSTRUCTION_CAPTION, 
                                            FontFamily.OTHER, Color.LOW_CONTRAST2)
        
        self.SettingsInstruction = Label.Label(Text.settingsInstructionText,
                                               FS.INSTRUCTION_CAPTION, 
                                               FontFamily.OTHER, Color.LOW_CONTRAST2)
        
        self.TranscribeInstruction = Label.Label(Text.transcribeInstructionText, 
                                                 FS.INSTRUCTION_CAPTION, 
                                                 FontFamily.OTHER,
                                                 Color.LOW_CONTRAST2)
        
        self.FileInstruction = Label.Label(Text.fileInstructionText, 
                                           FS.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.LOW_CONTRAST2)
        
        self.EditInstruction = Label.Label(Text.editInstructionText,
                                           FS.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.LOW_CONTRAST2)

        """ instruction icons """
        self.AudioIcon = Image.Image(Asset.instructionSound)
        self.SettingsIcon = Image.Image(Asset.instructionSetting)
        self.TranscribeIcon = Image.Image(Asset.instructionTranscribe)
        self.FileIcon = Image.Image(Asset.instructionFile)
        self.EditIcon = Image.Image(Asset.instructionEdit)
        
      
    def _initInstructionGrid(self):
        """ adds a grid layout for the instruction texts and icons """
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
                                        FS.HEADER1, 
                                        FontFamily.MAIN)
        self.WelcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.CaptionText = Label.Label(Text.captionText,
                                       FS.BODY, 
                                       FontFamily.OTHER,
                                       Color.LOW_CONTRAST2)
        
        self.CaptionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        self.StartBtn = Button.ColoredBtn(Text.startBtnText, Color.SECONDARY_BUTTON)
        
        self.InstructionText = Label.Label(Text.instructionText, FS.HEADER2, 
                                           FontFamily.MAIN)
        self.InstructionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
    
        
    """ TODO: put the link onto separate file """
    def _initLinkText(self):
        """ initializes the link text and functionality """
        self.ResourcesText = Label.Label(Text.resourcesText, 
                                         FS.HEADER2, 
                                         FontFamily.OTHER)
        self.ResourcesText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.TutorialText = Label.Label(Links.tutorialLink, FS.LINK,
                                        FontFamily.OTHER, Color.PRIMARY_BUTTON,
                                        StyleSheet.linkStyle, link=True)

        self.GuideText = Label.Label(Links.guideLink, FS.LINK, 
                                        FontFamily.OTHER, Color.PRIMARY_BUTTON,
                                         StyleSheet.linkStyle, link=True)
        self.GBLinkText = Label.Label(Links.gbWebLink, FS.BODY, 
                                      FontFamily.OTHER, Color.PRIMARY_BUTTON, link=True)
        
        self.GBLinkText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.MoreInfoText = Label.Label(Text.moreInfoText, 
                                        FS.SMALL, FontFamily.OTHER)
        
        self.MoreInfoText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
