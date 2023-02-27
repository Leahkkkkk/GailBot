'''
File: ProgressBar.py
Project: GailBot GUI
File Created: Sunday, 4th December 2022 12:55:30 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 4th December 2022 1:02:53 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from util.Style import Dimension, Color
from view.style.WidgetStyleSheet import PROGRESS_BAR
from PyQt6.QtWidgets import QSlider
from PyQt6 import QtCore, QtGui, QtWidgets


DEFAULT_MAXIMUM = 100

class ProgressBar (QSlider):
    """ A progress bar with customized styles """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(Dimension.PROGRESSBARWIDTH)
        self.initStyle()
        self.setMaximum(100)
    
    def initStyle(self):
        self.setStyleSheet(PROGRESS_BAR)
        self.setEnabled(False)
    
    def updateValue(self, value: int):
        """ given a value, set the progress bar value to the given value """
        if value >= self.maximum() // 1.1:
            self.setMaximum(int (self.maximum() + 10))
        self.setValue(value)
    
    def resetRange(self):
        """ reset the progress bar's range  """
        self.setMaximum(DEFAULT_MAXIMUM)
    
    
class SimpleDial(QtWidgets.QDial):
    """ a circular dial widget to show progress, with customized style 
        that overwrites the original style from PyQt library """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(60)
        self.setDisabled(True)
        self.setValue(0)
        self.setMinimumHeight(100)
        self.maxi = 60
        
    def paintEvent(self, event):
        # create a QStyleOption for the dial, and initialize it with the basic properties
        # that will be used for the configuration of the painter
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        width = opt.rect.width()
        height = opt.rect.height()
        r = min(width, height) / 2
        r -= r / 50
        d_ = r / 6
        dx = opt.rect.x() + d_ + (width - 2 * r) / 2 + 1
        dy = opt.rect.y() + d_ + (height - 2 * r) / 2 + 1
        br = QtCore.QRectF(dx + .5, dy + .5, 
            int(r * 2 - 2 * d_ - 2), 
            int(r * 2 - 2 * d_ - 2))

        penColor = self.palette().dark().color()
        qp = QtGui.QPainter(self)
        qp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing)
        qp.setPen(QtGui.QPen(penColor, 4))
        qp.drawEllipse(br)
        realValue = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        angle = 240 - 300 * realValue
        line = QtCore.QLineF.fromPolar(r * .6, angle)
        line.translate(br.center())
        ds = r / 5
        handleRect = QtCore.QRectF(0, 0, ds, ds)
        handleRect.moveCenter(line.p2())
        qp.setPen(QtGui.QPen(penColor, 2))
        qp.drawEllipse(handleRect)
    
    def updateValue(self, value: int):
        """ update the value of the progress dial """
        self.setValue(int(value % self.maxi))

    def resetRange(self):
        """ reset the range of the widget """
        self.setMaximum(DEFAULT_MAXIMUM)