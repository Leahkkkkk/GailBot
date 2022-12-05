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

from PyQt6.QtWidgets import QSlider
from PyQt6 import QtCore, QtGui, QtWidgets


DEFAULT_MAXIMUM = 100

class ProgressBar (QSlider):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(Dimension.PROGRESSBARWIDTH)
        self.initStyle()
        self.setMaximum(100)
    
    def initStyle(self):
        self.setStyleSheet("QSlider::groove:horizontal {"
                            "border: 1px solid #bbb;"
                            f"background: {Color.PRIMARY_BUTTON};"
                            "height: 10px; border-radius: 4px;"
                            "}"
                            "QSlider::add-page:horizontal {"
                            f"background: {Color.GREYEXTRALIGHT};"
                            "border: 1px solid #777;"
                            "height: 10px; border-radius: 4px;"
                            "}"
                            "QSlider::handle:horizontal {"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #eee, stop:1 #ccc);"
                            "border: 1px solid #777;width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;"
                            "}")
        self.setEnabled(False)
    
    def updateValue(self, value: int):
        if value >= self.maximum() // 1.1:
            self.setMaximum(int (self.maximum() + 10))
        self.setValue(value)
    
    def resetRange(self):
        self.setMaximum(DEFAULT_MAXIMUM)
    
    
class SimpleDial(QtWidgets.QDial):
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

        # construct a QRectF that uses the minimum between width and height, 
        # and adds some margins for better visual separation
        # this is partially taken from the fusion style helper source
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

        # find the "real" value ratio between minimum and maximum
        realValue = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        # compute the angle at which the dial handle should be placed, assuming
        # a range between 240° and 300° (moving clockwise)
        angle = 240 - 300 * realValue
        # create a polar line for the position of the handle; this can also
        # be done using the math module with some performance improvement
        line = QtCore.QLineF.fromPolar(r * .6, angle)
        line.translate(br.center())
        ds = r / 5
        # create the handle rect and position it at the end of the polar line
        handleRect = QtCore.QRectF(0, 0, ds, ds)
        handleRect.moveCenter(line.p2())
        qp.setPen(QtGui.QPen(penColor, 2))
        qp.drawEllipse(handleRect)
    
    
    def updateValue(self, value: int):
        self.setValue(int(value % self.maxi))

    def resetRange(self):
        self.setMaximum(DEFAULT_MAXIMUM)