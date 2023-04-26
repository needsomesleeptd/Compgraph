from main import Qcolor_to_stylesheet

from intersections import *
from drawing_algos import *

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent

from copy import deepcopy
from PyQt5.QtWidgets import QMessageBox


def QLine_to_line(Qline: [QPointF, QPointF]):
    return [[Qline[0].x(), Qline[0].y()], [Qline[1].x(), Qline[1].y()]]


def QLines_to_line(Qlines):
    lines = []
    for Qline in Qlines:
        lines.append(QLine_to_line(Qline))
    return lines


def QPoint_to_point(Qpoint: QPointF):
    return [Qpoint.x(), Qpoint.y()]


class Canvas(QtWidgets.QGraphicsView):
    dotsPrintSignal = QtCore.pyqtSignal(float, float)
    clearSignal = QtCore.pyqtSignal()
    displayRectCoordsSignal = QtCore.pyqtSignal(float, float, float, float)

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
        self.cur_rect = []
        self.lines = []
        self.cur_line = []
        self.pan_mode = False
        self.rect = None
        self.cut_off_color = QColor(0, 0, 0)
        self.line_color = QColor(12, 123, 56)
        self.background_color = QColor(255, 255, 255)
        self.save_color = QColor(255, 255, 255)
        self.saved_state = [self.cur_line.copy(), self.lines.copy(), self.cur_rect.copy()]

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def drawLine(self, fr, to, color):
        return self.scene.addLine(*fr, *to, color)

    def drawRect(self, left_point, right_point, color):

        w = right_point[0] - left_point[0]
        h = right_point[1] - left_point[1]
        return self.scene.addRect(*left_point, w, h, color)

    def clear_cur_rect(self):
        self.scene.removeItem(self.rect)
        self.rect = None

    def add_dot_rect(self, pos):
        self.save_state()
        if (len(self.cur_rect) >= 1):
            self.clear_cur_rect()
        if (len(self.cur_rect) >= 2):
            self.cur_rect = []

        if len(self.cur_rect) == 0:
            self.rect = self.drawLine([pos.x(), pos.y()], [pos.x(), pos.y()], self.pen.color())
            self.cur_rect.append([pos.x(), pos.y()])
        else:
            left_up_point = [min(pos.x(), self.cur_rect[0][0]), min(pos.y(), self.cur_rect[0][1])]
            right_down_point = [max(pos.x(), self.cur_rect[0][0]), max(pos.y(), self.cur_rect[0][1])]
            self.cur_rect = [left_up_point, right_down_point]
            self.rect = self.drawRect(*self.cur_rect, self.pen.color())
            self.displayRectCoordsSignal.emit(*self.cur_rect[0], *self.cur_rect[1])

        self.update()

    def add_dot_line(self, pos):
        if (len(self.cur_line) == 0):
            self.cur_line.append([pos.x(), pos.y()])
        else:
            self.cur_line.append([pos.x(), pos.y()])
            self.drawLine(*self.cur_line, self.line_color)
            self.cur_line.sort(key=lambda x: x[0])
            self.lines.append(self.cur_line)
            self.cur_line = []

        self.dotsPrintSignal.emit(pos.x(), pos.y())
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.pan_mode:

            pos = self.mapToScene(event.pos())
            self.save_state()
            if event.buttons() == QtCore.Qt.LeftButton:
                self.add_dot_rect(pos)

            if event.buttons() == QtCore.Qt.RightButton:
                self.add_dot_line(pos)

            self.update()

    def DisplayIntersections(self):
        if (len(self.cur_line) != 0):
            self.show_message("Линия не была проведена", "Вторая точка прямой не была определена")
            return
        lines_with_points = [[QPointF(*line[0]), QPointF(*line[1])] for line in self.lines]
        rect_with_points = [QPointF(*self.cur_rect[0]), QPointF(*self.cur_rect[1])]
        intersected_lines = find_intersections(lines_with_points, rect_with_points)
        for i, results in enumerate(intersected_lines):
            flag, inter_line = results[0], QLine_to_line(results[1])
            if flag == 0:  # invisible
                self.drawLine(*self.lines[i], self.cut_off_color)
            if flag == 1:  # visible
                self.drawLine(*inter_line, self.line_color)
                # print(inter_line,self.lines[i])
                if (inter_line[0] != self.lines[i][0]):
                    self.drawLine(inter_line[0], self.lines[i][0], self.cut_off_color)
                if (inter_line[1] != self.lines[i][1]):
                    self.drawLine(inter_line[1], self.lines[i][1], self.cut_off_color)

        self.update()

    def CreateGraphicsScene(self):
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        # scene.setSceneRect(-self.width() / 2, -self.height() / 2,self.width(),self.height())
        return scene

    def changePenColor(self, color):
        self.pen.setColor(color)

    def changeCutOffColor(self, color):
        self.cut_off_color = color

    def changeLineColor(self, color):
        self.line_color = color

    def clearCanvas(self):
        self.scene.clear()
        self.update()

    def get_params(self):
        # canvas_copy = self.image.copy()
        return [self, self.pen.color(), self.fill_color, self.seed_point, self.polygons]

    def save_state(self):
        self.saved_state = [self.cur_line.copy(), self.lines.copy(), self.cur_rect.copy()]

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()
