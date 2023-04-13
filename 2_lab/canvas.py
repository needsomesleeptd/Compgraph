import sys
import random
import numpy
import numpy as np

from drawing_algos import *

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
        self.save_request = []
        self.flag_has_started = False
        self.points = []
        self.image = QtGui.QImage(self.width() * 2, self.height() * 2, QtGui.QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        # temp_pixmap = QtGui.QPixmap.convertFromImage(self.image)
        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(self.image)
        self.pixmap_on_canvas = self.scene.addPixmap(self.pixmap)
        self.fitInView(self.pixmap_on_canvas)
        self.cur_polygon = []

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)
        newPos = self.mapToScene(event.pos())
        # self.image = self.image.scaled(self.width(), self.height())
        # self.updatePixmap()
        # self.fitInView(self.pixmap_on_canvas)

    '''def mousePressEvent(self, event):
        oldPos = self.mapToScene(self.viewport().rect().center())

        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        newPos = self.mapToScene(event.pos())
        delta = oldPos - newPos
        self.translate(delta.x(), delta.y())

        # super().mousePressEvent(event)'''

    def drawLine(self, fr, to):
        points = bresenhamAlogorithmFloat(*fr, *to)
        for point in points:
            self.image.setPixelColor(point.x(), point.y(), self.pen.color())
        self.updatePixmap()

    def updatePixmap(self):
        # super().fitInView(self.pixmap_on_canvas)
        self.image = self.image.scaled(self.width(), self.height())
        self.pixmap.convertFromImage(self.image)
        self.pixmap_on_canvas.setPixmap(self.pixmap)

    def mousePressEvent(self, event):

        # if not self.flag_has_started:
        pos = self.mapToScene(event.pos())
        if event.buttons() == QtCore.Qt.LeftButton:
            if (len(self.cur_polygon) == 0):
                self.image.setPixelColor(pos.x(), pos.y(), self.pen.color())
            else:
                self.drawLine(self.cur_polygon[-1], [pos.x(), pos.y()])


        if event.buttons() == QtCore.Qt.RightButton:
            self.drawLine(self.cur_polygon[0],self.cur_polygon[-1])
            self.cur_polygon = []

        self.cur_polygon.append([pos.x(), pos.y()])
        self.updatePixmap()



    def CreateGraphicsScene(self):
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        # scene.setSceneRect(-self.width() / 2, -self.height() / 2,self.width(),self.height())
        return scene

    def drawEllipseStandard(self, xc, yc, A, B):

        self.scene.addEllipse(xc - A / 2, yc - B / 2, A, B, self.pen)
        return 1  # one object

    def drawEllipsesStandard(self, reqs):
        overall_len = 0
        for req in reqs:
            overall_len += self.drawEllipseStandard(*req.dots, req.B_ellipse, req.A_ellipse)
        return overall_len

    def drawCircleStandard(self, xc, yc, r):
        # print(xc,yc,r)
        self.scene.addEllipse(xc - (r) / 2, yc - (r) / 2, r, r, self.pen)
        return 1  # one object

    def drawCirclesStadard(self, reqs):
        overall_len = 0
        for req in reqs:
            overall_len += self.drawCircleStandard(*req.dots, req.R)
        return overall_len

    def drawLineByPoints(self, points):

        for point in points:
            x, y = point.x(), point.y()
            self.scene.addRect(x, y, 1, 1, self.pen)
        return len(points)

    def drawLinesByPoints(self, lines):
        overall_len = 0
        for i in range(len(lines)):
            points = lines[i]
            overall_len += self.drawLineByPoints(points)
        return overall_len

    def drawLineIntensivityByPoints(self, coloredPoints):

        default_drawing_color = self.pen.color()
        drawing_pen = QtGui.QPen(default_drawing_color)
        drawing_pen.setJoinStyle(Qt.MiterJoin)

        for point in coloredPoints:
            x, y = point[0], point[1]
            if (len(point) >= 3):
                intensivity = point[2]
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
        self.save_request = [self.pen.color(), "PenColor"]
        self.pen.setColor(color)

    def changeCanvasBackGroundColor(self):

        background_color = QtWidgets.QColorDialog.getColor()
        if (background_color.isValid()):
            self.save_request = [self.backgroundColor, "BackgroundColor"]
            brush = QtGui.QBrush(background_color)
            self.backgroundColor = background_color
            self.setBackgroundBrush(brush)

    def clearCanvas(self):
        self.save_request = []
        items = self.scene.items()
        self.saved_scene = QtWidgets.QGraphicsScene()
        if (len(items) > 0):
            for i in range(len(items) - 1, 0, -1):
                self.saved_scene.addItem(items[i])
            self.curr_state_saved_len = len(self.figure_items_count)
        self.scene.clear()
        self.scene.update()

    def undo_action(self):
        if (len(self.save_request) > 0):
            if (self.save_request[1] == "BackgroundColor"):
                background_color = self.save_request[0]
                brush = QtGui.QBrush(background_color)
                self.backgroundColor = background_color
                self.setBackgroundBrush(brush)
            else:
                pen_color = self.save_request[0]
                self.pen.setColor(pen_color)
        else:
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
                self.figure_items_count = []
            self.curr_state_saved_len = -1
