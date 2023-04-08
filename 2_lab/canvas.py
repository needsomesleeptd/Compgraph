import sys
import random
import numpy
import numpy as np
from algos_ellipses import *

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent

from copy import deepcopy
matplotlib.use('QT5Agg')


class Canvas(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = self.CreateGraphicsScene()
        self.pen = QtGui.QPen(Qt.red)
        self.pen.setJoinStyle(Qt.MiterJoin)
        # self.pen.setMiterLimit(0)
        self.backgroundColor = QtGui.QColor(Qt.white)
        self._zoom = 2  # times which picture is zoomed
        self.figure_items_count = []
        self.saved_scene = QtWidgets.QGraphicsScene()
        self.curr_state_saved_len = -1

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

    def drawEllipseStandard(self, xc, yc, A, B):

        self.scene.addEllipse(xc,yc,A,B,self.pen)
        return 1 #one object
    def drawCircleStandard(self,xc,yc,r):
        self.scene.addEllipse(xc, yc, r, r, self.pen)
        return 1  # one object


    def drawLineByPoints(self, points):

        for point in points:
            x, y = point.x(), point.y()
            self.scene.addRect(x, y, 1, 1, self.pen)
        return len(points)

    def drawLineIntensivityByPoints(self, coloredPoints):

        default_drawing_color = self.pen.color()
        drawing_pen = QtGui.QPen(default_drawing_color)
        drawing_pen.setJoinStyle(Qt.MiterJoin)

        for point in coloredPoints:
            x, y = point[0], point[1]
            if (len(point) >=3):
                intensivity =point[2]
                new_red = default_drawing_color.red()
                new_blue = default_drawing_color.blue()
                new_green = default_drawing_color.green()
                new_color = QtGui.QColor()
                new_color.setRgb(new_red, new_blue, new_green)
                new_color.setAlphaF(intensivity)
                drawing_pen.setColor(new_color)

                self.scene.addRect(x, y, 1, 1, drawing_pen)
            else:
                self.scene.addRect(x, y, 1, 1, drawing_pen)

        return len(coloredPoints)




    def drawSpectre(self, spectreLines, method, undo=False):


        len_obj = 0
        for line in spectreLines:
            if (method == "brezSmoothSpectre" or method == "VuSpectre"):
                len_obj += self.drawLineIntensivityByPoints(line)
            elif (method == "defaultAlgoSpectre"):
                len_obj += self.drawLine(*line[0], *line[1])

            else:
                len_obj += self.drawLineByPoints(line)

        self.update()
        return len_obj

    def changePenColor(self, color):

        self.pen.setColor(color)

    def changeCanvasBackGroundColor(self):

        background_color = QtWidgets.QColorDialog.getColor()
        if (background_color.isValid()):
            brush = QtGui.QBrush(background_color)
            self.backgroundColor = background_color
            self.setBackgroundBrush(brush)

    def clearCanvas(self):
        for item in self.scene.items():
            self.saved_scene.addItem(item)
        self.curr_state_saved_len = len(self.figure_items_count)
        self.scene.clear()
        self.scene.update()

    def undo_action(self):
        if (self.curr_state_saved_len != len(self.figure_items_count)):
            items = self.scene.items()
            if (len(self.figure_items_count) > 0 and len(items) != 0):
                for items_added_count in range(self.figure_items_count[-1]):
                    self.scene.removeItem(items[items_added_count])
                self.figure_items_count = self.figure_items_count[:-1]
        else:
            self.scene = self.saved_scene
            self.setScene(self.scene)
            self.scene.update()
            self.update()
            self.saved_scene = QtWidgets.QGraphicsScene()
        self.curr_state_saved_len  = -1

