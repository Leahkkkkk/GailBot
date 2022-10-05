""" takes in image name and generates an image widget """

import imghdr
from PyQt6.QtWidgets import QLabel,QGridLayout,QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import  QSize
from util import Path  
import os 

class Image(QLabel):
    def __init__(self, imagename:str, size = 50, *args, **kwargs)->None:
        super().__init__(*args, **kwargs)
        imgpath = os.path.join(Path.get_project_root(), f"view/asset/{imagename}")
        self.img = QPixmap(imgpath)
        self.setPixmap(self.img)
        self.resize(self.img.width(), self.img.height())
        self.setFixedSize(QSize(size, size))
        self.setScaledContents(True)
        