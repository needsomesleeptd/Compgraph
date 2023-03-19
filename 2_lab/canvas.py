import sys
import random
import numpy
import numpy as np
from drawing_algorithms import *

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent
matplotlib.use('QT5Agg')




from copy import deepcopy,copy

class Canvas(QtWidgets.QGraphicsView):

    def __init__(self,parent):
        super().__init__(parent)
        self.scene = self.CreateGraphicsScene()
        self.pen = QtGui.QPen(Qt.red)


    def CreateGraphicsScene(self):
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        scene.setSceneRect(-self.width() / 2, -self.height() / 2,self.width(),self.height())
        return scene


    def drawLine(self, x0, y0, x1, y1):
        self.scene.addLine(x0,y0,x1,y1,self.pen)

    def drawLineByPoints(self,points):
            self.scene.addPolygon(points,self.pen)

    def drawLineIntensivityByPoints(self,coloredPoints):

        default_color = self.pen.color()
        drawing_pen = QtGui.QPen(default_color)
        prev_x,prev_y = coloredPoints[0][0],coloredPoints[0][1]


        for point in coloredPoints:
            x,y,intersivity = point[0],point[1],point[2]
            new_red = default_color.red() * intersivity
            new_blue = default_color.blue() * intersivity
            new_green = default_color.green() * intersivity
            new_color = QtGui.QColor(new_red,new_blue,new_green)
            drawing_pen.setColor(new_color)
            self.scene.addLine(prev_x,prev_y,x,y,drawing_pen)
            prev_x = x
            prev_y = y


    def drawSpectre(self,spectreLines,method):
        for line in spectreLines:
            if (method == "brezSmoothSpectre"):
                self.drawLineIntensivityByPoints(line)
            elif (method == "defaultAlgoSpectre"):
                self.drawLine(*line)
            else:
                self.drawLineByPoints(line)
        self.update()




    def changePenColor(self,color):
        self.pen.setColor(color)

