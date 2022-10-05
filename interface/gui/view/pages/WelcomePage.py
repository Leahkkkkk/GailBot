from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from view.widgets import Button, Label, Image, Button
from view.style.style import FontFamily, FontSize, Color
from util import Path  
import os

""" TODO: 1. current background is not responsive ;
          2. Links are not clickable
"""

""" class for welcome page """
class WelcomePage(QWidget):
    """ initialize class """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
    """ initialize widgets """
    def _initWidget(self):
        """ add text and button widget """
        self.WelcomeText = Label.Label("Welcome to \n GailBot", 
                                        FontSize.HEADER1, 
                                        FontFamily.MAIN)
        self.WelcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.captionText = Label.Label("GailBot is the world's first application"
                                       " that let's you convert audio and\n"
                                       " video file into customizd transcript.",
                                       FontSize.BODY, FontFamily.OTHER,Color.GREYMEDIUM2)
        self.captionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        self.HomeSetBtn = Button.ColoredBtn("⚙", Color.BLUEMEDIUM,"35px")
        self.StartBtn = Button.ColoredBtn("Get Started", Color.GREEN)
        
        self.InstructionText = Label.Label("How GailBot Works", FontSize.HEADER2, 
                                           FontFamily.MAIN)
        self.InstructionText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        
        """ instruction texts """
        self.AudioInstruction = Label.Label("1. Select audio and video files" 
                                            "\n or record live in Gailbot", 
                                            FontSize.INSTRUCTION_CAPTION, 
                                            FontFamily.OTHER,Color.GREYMEDIUM2)
        
        self.AudioInstruction.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
        self.SettingsInstruction = Label.Label("2. Apply settings",
                                               FontSize.INSTRUCTION_CAPTION, 
                                               FontFamily.OTHER,Color.GREYMEDIUM2)
        
        self.TranscribeInstruction = Label.Label("3. Transcribe", 
                                                 FontSize.INSTRUCTION_CAPTION, 
                                                 FontFamily.OTHER,
                                                 Color.GREYMEDIUM2)
        
        self.FileInstruction = Label.Label("4. Get a transcribed file", 
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)
        
        self.EditInstruction = Label.Label("5. Edit settings \n or retranscribe",
                                           FontSize.INSTRUCTION_CAPTION, 
                                           FontFamily.OTHER,
                                           Color.GREYMEDIUM2)
        
        self.EditInstruction.setAlignment(Qt.AlignmentFlag.AlignHCenter) 


        """ instruction icons """
        self.AudioIcon = Image.Image("sound.jpeg")
        self.SettingsIcon = Image.Image("setting.jpeg")
        self.TranscribeIcon = Image.Image("loading.jpeg")
        self.FileIcon = Image.Image("file.jpeg")
        self.EditIcon = Image.Image("file.jpeg")
    
        """ instruction text """
        self.ResourcesText = Label.Label("Resources",FontSize.HEADER2, FontFamily.OTHER)
        self.ResourcesText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.TutorialText = Label.Label("GailBot Beginner Tutorial",FontSize.LINK,
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;")
        self.GuideText = Label.Label("GailBot Settings Guide",FontSize.LINK, 
                                        FontFamily.OTHER, Color.BLUEMEDIUM,
                                        "text-decoration: underline;")
        
        self.GBLinkText = Label.Label("GailBot.com",FontSize.BODY, 
                                      FontFamily.OTHER,Color.BLUEMEDIUM,)
        
        self.GBLinkText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

        self.MoreInfoText = Label.Label("For more information visit", 
                                        FontSize.SMALL, FontFamily.OTHER)
        
        self.MoreInfoText.setAlignment(Qt.AlignmentFlag.AlignHCenter) 

      
    """ initialize layouts """
    def _initLayout(self):
        """ grid layout """
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
        self.verticalLayout.addWidget(self.captionText, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.StartBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        # padding here
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, 
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
        

    """ initialize style """
    def _initStyle(self):
        self.HomeSetBtn.setFixedSize(QtCore.QSize(40,40))
        self.StartBtn.setMinimumSize(QtCore.QSize(150,30))
        self.setAutoFillBackground(True)
        palette = self.palette()
        brush = QtGui.QBrush()
        brush.setTextureImage(QtGui.QImage
                              (os.path.join(Path.get_project_root(), 
                                       "view/asset/background.png")))
        palette.setBrush(QtGui.QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        
        
