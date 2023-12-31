'''
File: Image.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:55 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a image widget to support displaying image on the interface
'''

import os 
from config_frontend import PROJECT_ROOT 
from view.config.Style import Dimension
from PyQt6.QtWidgets import (
    QLabel)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import  QSize

class Image(QLabel):
    """ takes in the filename of image and generates a image widget that 
        can be displayed  
        
        Args:
            imagename (str): relative file path of the image, relative to the 
                             project root 
            size (int, Optional) : size of the image, default to 50
    """
    def __init__(
        self, 
        imagename:str, 
        size = (Dimension.ICONBTN,Dimension.ICONBTN), 
        *args, 
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        imgpath = os.path.join(PROJECT_ROOT, f"{imagename}")
        self.img = QPixmap(imgpath)
        self.setPixmap(self.img)
        self.resize(self.img.width(), self.img.height())
        self.setFixedSize(QSize(size[0], size[1]))
        self.setScaledContents(True)
        