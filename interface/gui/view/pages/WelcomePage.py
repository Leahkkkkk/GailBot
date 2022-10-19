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

 

from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initImgBackground
from view.widgets import (
    Button, 
    Label, 
    Image, 
    Button
)

from view.Text.WelcomePageText import WelcomePageText

from view.Text.LinkText import Links

from PyQt6.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QHBoxLayout, 
    QSpacerItem, 
    QSizePolicy,
    QVBoxLayout
)

from PyQt6 import QtCore, QtGui
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
        self.verticalLayout.addWidget(self.WelcomeText)
        self.verticalLayout.addWidget(self.CaptionText, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.StartBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        spacer = QSpacerItem(40, 50, QSizePolicy.Policy.Preferred, 
                             QSizePolicy.Policy.Preferred)
    
        self.verticalLayout.addItem(spacer)
        self.verticalLayout.addWidget(self.InstructionText)
        self.verticalLayout.addWidget(self.gridBox)
        self.verticalLayout.addItem(spacer)
        self.verticalLayout.addWidget(self.ResourcesText)
        self.verticalLayout.addWidget(self.horizontoalBox)
        self.verticalLayout.addWidget(self.MoreInfoText)
        self.verticalLayout.addWidget(self.GBLinkText)
        self.verticalLayout.addItem(spacer)
        
    def _initStyle(self):
        """ initialize style """
        self.HomeSetBtn.setFixedSize(QtCore.QSize(40,40))
        self.HomeSetBtn.hide()
        self.StartBtn.setMinimumSize(QtCore.QSize(150,30))
        initImgBackground(self)

    
    """ TODO: separate to a different file """   
    def _initInstructionText(self):
        """ add widgets for the instructions text and icon """
        """ instruction text """
        self.AudioInstruction = Label.Label(WelcomePageText.audioInstructionText, 
                                            FontSize.INSTRUCTION_CAPTION, 
                                            FontFamily.OTHER,Color.GREYMEDIUM2)
        
        self.SettingsInstruction = Label.Label(WelcomePageText.settingsInstructionText,
                                               FontSize.INSTRUCTION_CAPTION, 
                                               FontFamily.OTHER,Color.GREYMEDIUM2)
        
        self.TranscribeInstruction = Label.Label(WelcomePageText.transcribeInstructionText, 
                                                 FontSize.INSTRUCTION_CAPTION, 
                                                 FontFamily.OTHER,
                                                 Color.GREYMEDIUM2)
        
        self.FileInstruction = Label.Label(WelcomePageText.fileInstructionText, 
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)
        
        self.EditInstruction = Label.Label(WelcomePageText.editInstructionText,
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)


        """ instruction icons """
        self.AudioIcon = Image.Image("sound.jpeg")
        self.SettingsIcon = Image.Image("settings.png")
        self.TranscribeIcon = Image.Image("loading.jpeg")
        self.FileIcon = Image.Image("file.jpeg")
        self.EditIcon = Image.Image("edit.jpeg")
        
      
 
    def _initInstructionGrid(self):
        """ add a gird layout for the instruction """
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
        self.WelcomeText = Label.Label(WelcomePageText.welcomeText, 
                                        FontSize.HEADER1, 
                                        FontFamily.MAIN)
        self.WelcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.CaptionText = Label.Label(WelcomePageText.captionText,
                                       FontSize.BODY, 
                                       FontFamily.OTHER,
                                       Color.GREYMEDIUM2)
        
        self.CaptionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.HomeSetBtn = Button.ColoredBtn("⚙", Color.BLUEMEDIUM,"35px")
        self.StartBtn = Button.ColoredBtn(WelcomePageText.startBtnText, Color.GREEN)
        
        self.InstructionText = Label.Label(WelcomePageText.instructionText, FontSize.HEADER2, 
                                           FontFamily.MAIN)
        self.InstructionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
    
        
    """ TODO: put the link onto separate file """
    def _initLinkText(self):
        """ initialize the link text on homepage """
        linkTemplate = "<a href={0}>{1}</a>"
        self.ResourcesText = Label.Label(WelcomePageText.resourcesText, 
                                         FontSize.HEADER2, 
                                         FontFamily.OTHER)
        self.ResourcesText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        
        self.TutorialText = Label.Label(Links.tutorialLink, FontSize.LINK,
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;", link=True)
        
        self.GuideText = Label.Label(Links.guideLink,FontSize.LINK, 
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;", link=True)
        self.GBLinkText = Label.Label(Links.gbWebLink, FontSize.BODY, 
                                      FontFamily.OTHER,Color.BLUEMEDIUM,link=True)
        
        self.GBLinkText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.MoreInfoText = Label.Label(WelcomePageText.moreInfoText, 
                                        FontSize.SMALL, FontFamily.OTHER)
        
        self.MoreInfoText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 