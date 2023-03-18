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
        #self.setTransformationAnchor()
        return scene







      


    def drawLine(self, x0, y0, x1, y1):
        self.scene.addLine(x0,y0,x1,y1,self.pen)

    def drawLineByPoints(self,points):
            self.scene.addPolygon(points,self.pen)




    def changePenColor(self,color):
        self.pen.setColor(color)
