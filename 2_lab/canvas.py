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

from copy import deepcopy, copy


class Canvas(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = self.CreateGraphicsScene()
        self.pen = QtGui.QPen(Qt.red)
        self.pen.setJoinStyle(Qt.MiterJoin)
        #self.pen.setMiterLimit(0)
        self.backgroundColor = QtGui.QColor(Qt.white)
        self._zoom = 2  # times which picture is zoomed

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self.rect())

        self.setSceneRect(rect)

        unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewrect = self.viewport().rect()
        scenerect = self.transform().mapRect(rect)
        factor = min(viewrect.width() / scenerect.width(),
                     viewrect.height() / scenerect.height())
        self.scale(factor, factor)
        self._zoom = 0

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)
        newPos = self.mapToScene(event.pos())

    def mousePressEvent(self, event):
        oldPos = self.mapToScene(self.viewport().rect().center())

        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        newPos = self.mapToScene(event.pos())
        delta = oldPos - newPos
        self.translate(delta.x(), delta.y())

        # super().mousePressEvent(event)

    def CreateGraphicsScene(self):
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        # scene.setSceneRect(-self.width() / 2, -self.height() / 2,self.width(),self.height())
        return scene

    def drawLine(self, x0, y0, x1, y1):
        self.scene.addLine(x0, y0, x1, y1, self.pen)

    def drawLineByPoints(self, points):
        #self.scene.addPolygon(points, self.pen)
        for point in points:
            x,y = point.x(),point.y()
            self.scene.addRect(x, y, 1, 1, self.pen)
    def drawLineIntensivityByPoints(self, coloredPoints):

        default_drawing_color = self.pen.color()
        drawing_pen = QtGui.QPen(default_drawing_color)
        drawing_pen.setJoinStyle(Qt.MiterJoin)
        prev_x, prev_y = coloredPoints[0][0], coloredPoints[0][1]

        for point in coloredPoints:
            x, y, intensivity = point[0], point[1], point[2]
            new_red = default_drawing_color.red()
            new_blue = default_drawing_color.blue()
            new_green = default_drawing_color.green()
            new_color = QtGui.QColor()
            new_color.setRgb(new_red, new_blue, new_green)
            new_color.setAlphaF(intensivity)
            drawing_pen.setColor(new_color)

            #self.scene.addLine(prev_x, prev_y, x, y, drawing_pen)
            self.scene.addRect(x,y,1,1,drawing_pen)
            prev_x = x
            prev_y = y

    def drawSpectre(self, spectreLines, method):
        for line in spectreLines:
            if (method == "brezSmoothSpectre" or method == "VuSpectre"):
                self.drawLineIntensivityByPoints(line)
            elif (method == "defaultAlgoSpectre"):
                self.drawLine(*line[0], *line[1])
            else:
                self.drawLineByPoints(line)
        self.update()

    def changePenColor(self, color):
        self.pen.setColor(color)

    def clearCanvas(self):
        self.scene.clear()
        self.scene.update()
