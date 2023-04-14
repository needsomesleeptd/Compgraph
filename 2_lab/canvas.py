from main import Qcolor_to_stylesheet

from drawing_algos import *

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent

from copy import deepcopy


class Canvas(QtWidgets.QGraphicsView):
    dotsPrintSignal = QtCore.pyqtSignal(float, float)
    clearSignal = QtCore.pyqtSignal()

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
        self.polygons = []
        self.seed_point = [0,0]
        self.pan_mode = False
        self.fill_color = QColor(0, 0, 0)
        self.seed_color = QColor(0, 0, 255)
        self.fitInView(self.pixmap_on_canvas, Qt.KeepAspectRatio)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        #self.fitInView(self.pixmap_on_canvas, Qt.KeepAspectRatio)

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
        super().mousePressEvent(event)
        if not self.pan_mode:
            pos = self.mapToScene(event.pos())
            if event.buttons() == QtCore.Qt.LeftButton:
                if (len(self.cur_polygon) == 0):
                    self.image.setPixelColor(pos.x(), pos.y(), self.pen.color())
                else:
                    self.drawLine(self.cur_polygon[-1], [pos.x(), pos.y()])
                self.cur_polygon.append([pos.x(), pos.y()])
                self.dotsPrintSignal.emit(pos.x(), pos.y())

            if event.buttons() == QtCore.Qt.RightButton and len(self.cur_polygon) > 0:
                self.drawLine(self.cur_polygon[0], self.cur_polygon[-1])
                self.polygons.append(self.cur_polygon)
                self.cur_polygon = []

            if event.buttons() == QtCore.Qt.MouseButton.MidButton:
                # print(self.filled_dot)

                self.seed_point = [pos.x(), pos.y()]

            self.updatePixmap()

    def fill_line_by_line(self, delay=0):
        # print(self.filled_dot)
        line_by_line_filling_algorithm_with_seed(self, self.pen.color(), self.fill_color, self.seed_point, delay)
        self.updatePixmap()

    def CreateGraphicsScene(self):
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        # scene.setSceneRect(-self.width() / 2, -self.height() / 2,self.width(),self.height())
        return scene

    def changePenColor(self, color):
        self.save_request = [self.pen.color(), "PenColor"]
        self.pen.setColor(color)

    def changeFillColor(self, color):
        self.save_request = [self.pen.color(), "PenColor"]
        self.fill_color = color

    def clearCanvas(self):
        self.image.fill(QColor(255, 255, 255))  # getting white color
        self.polygons = []
        self.cur_polygon = []
        self.clearSignal.emit()
        self.updatePixmap()

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

    def get_copied_params(self):
        canvas_copy = Canvas(self)
        return [canvas_copy, canvas_copy.pen.color(), canvas_copy.fill_color, canvas_copy.seed_point]
