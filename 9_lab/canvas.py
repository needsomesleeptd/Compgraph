from main import show_warning_message,show_info_message

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

from math import  isclose

def QLine_to_line(Qline: [QPointF, QPointF]):
    return [[Qline[0].x(), Qline[0].y()], [Qline[1].x(), Qline[1].y()]]


def QLines_to_line(Qlines):
    lines = []
    for Qline in Qlines:
        lines.append(QLine_to_line(Qline))
    return lines


def QPoint_to_point(Qpoint: QPointF):
    return [Qpoint.x(), Qpoint.y()]

def points_eq(point1,point2,eps=1e-2):
    if isclose(point1.x(), point2[0], abs_tol=eps) and isclose(point1.y(), point2[1], abs_tol=eps):
        return True
    else:
        return False

class Canvas(QtWidgets.QGraphicsView):
    dotsPrintSignal = QtCore.pyqtSignal(float, float, QColor)
    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = self.CreateGraphicsScene()
        self.pen = QtGui.QPen(Qt.red)
        self.pen.setJoinStyle(Qt.MiterJoin)
        # self.pen.setMiterLimit(0)
        self.backgroundColor = QtGui.QColor(Qt.white)
        self._zoom = 3  # times which picture is zoomed
        self.figure_items_count = []
        self.saved_scene = QtWidgets.QGraphicsScene()
        self.curr_state_saved_len = -1
        self.save_request = []
        self.flag_has_started = False
        self.points = []
        self.cutter = []
        self.polygon = []
        self.is_cutter_closed = False
        self.is_polygon_closed = False
        self.lines = []
        self.cur_line = []
        self.pan_mode = False
        self.rect = None
        self.cut_off_color = QColor(0, 0, 0)
        self.line_color = QColor(12, 123, 56)
        self.background_color = QColor(255, 255, 255)
        self.save_color = QColor(255, 255, 255)
        self.saved_state = []

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

    def drawPoint(self, pos, color):
        self.scene.addEllipse(*pos, 1, 1, color)

    def drawLines(self, lines, color):
        lines_drawings = []
        for line in lines:
            lines_drawings.append(self.drawLine(*line, color))
        return lines_drawings

    def drawRect(self, left_point, right_point, color):

        w = right_point[0] - left_point[0]
        h = right_point[1] - left_point[1]
        return self.scene.addRect(*left_point, w, h, color)

    def clear_cur_rect(self):
        if (self.rect != None):
            self.scene.removeItem(self.rect)
        self.rect = None

    def add_dot_polygon(self, pos, polygon, color, add_to_table=True, append_dot=True, skip_state=False):
        if (skip_state == False):
            self.save_state()

        if len(polygon) == 0:
            self.drawPoint([pos.x(), pos.y()], color)
            if append_dot:
                polygon.append([pos.x(), pos.y()])
            if add_to_table:
                self.dotsPrintSignal.emit(pos.x(), pos.y(), color)

        else:
            if not points_eq(pos,polygon[-1]):# Возможно стоит пробегаться по всем вершинам и искать похожую
                self.drawLine([pos.x(), pos.y()], polygon[-1], color)
                self.drawPoint([pos.x(), pos.y()], color)
                if append_dot:
                    polygon.append([pos.x(), pos.y()])
                if add_to_table:
                    self.dotsPrintSignal.emit(pos.x(), pos.y(), color)
        self.update()

    def close_cutter(self, skip_state=False):
        if (len(self.cutter) > 2):
            if not skip_state:
                self.save_state()
            self.drawLine(self.cutter[-1], self.cutter[0], color=self.pen.color())
            self.is_cutter_closed = True
            self.update()
        else:
            show_warning_message('У введенного отсекателя недостаточно сторон',
                         'У введенного отсекателя недостаточно сторон для его завершения')

    def close_polygon(self, skip_state=False):
        if (len(self.polygon) > 2):
            if not skip_state:
                self.save_state()
            self.drawLine(self.polygon[-1], self.polygon[0], color=self.line_color)
            self.is_polygon_closed = True
            self.update()
        else:
            show_warning_message('У введенного многоугольника недостаточно сторон',
                         'У введенного многоугольника недостаточно сторон для его завершения')

    def add_dot_line(self, pos):
        self.save_state()
        if (len(self.cur_line) == 0):
            self.cur_line.append([pos.x(), pos.y()])
        else:
            self.cur_line.append([pos.x(), pos.y()])
            self.drawLine(*self.cur_line, self.line_color)
            self.cur_line.sort(key=lambda x: x[0])
            self.lines.append(self.cur_line)
            self.cur_line = []

        self.dotsPrintSignal.emit(pos.x(), pos.y(), self.line_color)
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.pan_mode:

            pos = self.mapToScene(event.pos())


            if event.buttons() == QtCore.Qt.LeftButton:
                if not self.is_cutter_closed:
                    self.add_dot_polygon(pos, self.cutter, self.pen.color())
                else:
                    show_info_message('Фигура замкнута', 'Многоугольник замкнут, невозможно ставить его точки')



            if event.buttons() == QtCore.Qt.RightButton:
                if not self.is_polygon_closed:
                    self.add_dot_polygon(pos, self.polygon, self.line_color)
                else:
                    show_info_message('Фигура замкнута', 'Отсекатель замкнут, невозможно ставить его точки')

                # if (event.buttons() == QtCore.Qt.MouseButton.MidButton):
                #   self.close_polygon()

            self.update()

    def DisplayIntersections(self):
        if (not self.is_polygon_closed):
            self.show_message("Многоугольник не был замкнут", "Введенный многоугольник не был замкнут")
            return

        cutter_with_points = [QPointF(*dot) for dot in self.cutter]
        polygon_with_points = [QPointF(*dot) for dot in self.polygon]
        if not is_polygon_valid(cutter_with_points):
            self.show_message("Введенный отсекатель не валиден",
                              "Введенный отсекатель  не является выпуклым многоугольником")
            return

        # make_rotation_clockwise(polygon_with_points)

        self.save_state(is_itersected=True)

        p, np = sutherland_hodgman(polygon_with_points, cutter_with_points)
        for i in range(np):
            self.drawLine(QPoint_to_point(p[i - 1]), QPoint_to_point(p[i]), color=self.cut_off_color)
            # c.create_line(p[i - 1][0], p[i - 1][1], p[i][0], p[i][1], fill=result_colour)
        # self.drawLines()

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

    def reset_values(self):
        self.lines = []
        self.cutter = []
        self.polygon = []
        self.cur_line = []
        self.is_cutter_closed = False
        self.is_polygon_closed = False

    def drawPolygon(self, polygon, color):
        temp_polygon = polygon.copy()
        polygon = []
        for dot in temp_polygon:
            self.add_dot_polygon(QPointF(*dot), polygon, color=color, add_to_table=False, skip_state=True)

    def display_reverted_figures(self):
        self.scene.clear()
        self.drawPolygon(self.polygon, color=self.line_color)
        self.drawPolygon(self.cutter, color=self.pen.color())

        self.update()

    def clearCanvasAndData(self):
        self.scene.clear()
        self.reset_values()
        self.clearSignal.emit()
        self.update()

    def get_params(self):
        # canvas_copy = self.image.copy()
        return [self, self.pen.color(), self.fill_color, self.seed_point, self.polygons]

    def save_state(self, is_itersected=False):
        self.saved_state.append(
            [self.polygon.copy(), self.cutter.copy(), self.is_polygon_closed, self.is_cutter_closed, is_itersected])

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()
