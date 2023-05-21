from main import show_warning_message, show_info_message

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

from math import *


def frange(a, b, step=1):
    arr = []
    while (a <= b + EPS):
        arr.append(a)
        a += step
    return arr


def QLine_to_line(Qline: [QPointF, QPointF]):
    return [[Qline[0].x(), Qline[0].y()], [Qline[1].x(), Qline[1].y()]]


def QLines_to_line(Qlines):
    lines = []
    for Qline in Qlines:
        lines.append(QLine_to_line(Qline))
    return lines


def QPoint_to_point(Qpoint: QPointF):
    return [Qpoint.x(), Qpoint.y()]


def points_eq(point1, point2, eps=1e-2):
    if isclose(point1.x(), point2[0], abs_tol=eps) and isclose(point1.y(), point2[1], abs_tol=eps):
        return True
    else:
        return False


EPS = 1e-5
MAX_NUM = 1e5
MIN_NUM = -1e5


class Canvas(QtWidgets.QGraphicsView):
    dotsPrintSignal = QtCore.pyqtSignal(float, float, QColor)
    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = self.CreateGraphicsScene()
        self.pen = QtGui.QPen(Qt.red)
        #self.pen.setJoinStyle(Qt.MiterJoin)
        # self.pen.setMiterLimit(0)
        self.backgroundColor = QtGui.QColor(Qt.white)
        self._zoom = 3  # times which picture is zoomed
        self.figure_items_count = []
        self.saved_scene = QtWidgets.QGraphicsScene()
        self.save_request = []
        self.cut_off_color = QColor(0, 0, 0)
        self.line_color = QColor(12, 123, 56)
        self.background_color = QColor(255, 255, 255)
        self.save_color = QColor(255, 255, 255)
        self.saved_state = []
        self.pan_mode =False
        self.size_x = self.width()
        self.size_y = self.height()
        self.up_arr = []
        self.down_arr = []
        self.angles = [0,0,0]
        self.scale_factor = 1

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        if self._zoom > 0:
            #self.scale(factor, factor)
            super().scale(factor, factor)
        else:
            self._zoom = 0

    def resizeEvent(self, event):
        super().resizeEvent(event)
        #self.size_x = event.size().width()
        #self.size_y = event.size().height()


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
            if not points_eq(pos, polygon[-1]):  # Возможно стоит пробегаться по всем вершинам и искать похожую
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





    def DisplayIntersections(self):

        self.save_state(is_itersected=True)

        data_x = [-50,50,2]
        data_z =[-50,50,2]
        self.create_surface(data_x, data_z, f2)

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

    # ________________________________________________________________

    def draw_cut(self, x1, y1, x2, y2):
        self.scene.addLine(x1, y1, x2, y2, self.pen.color())

    def transform_points(self, x, y, z):  # think about it
        super().transform()
        x, y, z = self.rotate_point([x, y, z])

        #x = (x - data_x[0]) / (data_x[1] - data_x[0])
        #x = 20 + x * (self.size_x - 40)

        #y = (y - data_y[0]) / (data_y[1] - data_y[0])
        #y = 20 + y * (self.size_y - 40)
        x *= self.scale_factor
        y *= self.scale_factor


        return int(x), int(y)

    def find_min_max_y(self, data_x, data_z, f):
        x_min, x_max, x_step = data_x
        y_min, y_max = MAX_NUM, MIN_NUM
        x_min_scale, x_max_scale = MAX_NUM, MIN_NUM
        z_min, z_max, z_step = data_z

        for z in frange(z_min, z_max + 1, z_step):
            for x in frange(x_min, x_max, x_step):
                y = f(x, z)
                temp_x, y, temp_z = self.rotate_point([x, y, z])

                y_min = min(y, y_min)
                y_max = max(y, y_max)

                x_min_scale = min(x_min_scale, temp_x)
                x_max_scale = max(x_max_scale, temp_x)

        return (x_min_scale, x_max_scale), (y_min, y_max)

    def rotate_point(self, point):
        point = self.rotate_x(point)
        point = self.rotate_y(point)
        point = self.rotate_z(point)

        return point[0], point[1], point[2]

    def rotate_x(self, point):
        al = radians(self.angles[0])

        temp = point[1]
        point[1] = cos(al) * point[1] - sin(al) * point[2]
        point[2] = cos(al) * point[2] + sin(al) * temp
        return point

    def rotate_y(self, point):
        al = radians(self.angles[1])

        temp = point[0]
        point[0] = cos(al) * point[0] - sin(al) * point[2]
        point[2] = cos(al) * point[2] + sin(al) * temp
        return point

    def rotate_z(self, point):
        al = radians(self.angles[2])

        temp = point[0]
        point[0] = cos(al) * point[0] - sin(al) * point[1]
        point[1] = cos(al) * point[1] + sin(al) * temp
        return point

    def clean_screen(self):
        self.scene.clear()
        self.up_arr = []
        self.down_arr = []

    def do_task(self):
        self.clean_screen()

        x_min, x_max, x_step = float(self.XStart.text()), float(self.XEnd.text()), float(self.DX.text())
        z_min, z_max, z_step = float(self.ZStart.text()), float(self.ZEnd.text()), float(self.DZ.text())

        self.angles = self.get_angles()

        self.create_surface((x_min, x_max, x_step), (z_min, z_max, z_step), funcs(self.Funcs.currentIndex()))

    def get_angles(self):
        return (float(self.angle_ox.value()), float(self.angle_oy.value()),
                float(self.angle_oz.value()))

    def create_surface(self, data_x, data_z, f):
        data_x0, data_y = self.find_min_max_y(data_x, data_z, f)

        self.up_arr = [0] * self.width() * 2
        self.down_arr = [self.height()] * self.width() * 2

        x_left = y_left = -1
        x_right = y_right = -1

        x_min, x_max, x_step = data_x
        z_min, z_max, z_step = data_z

        for z in frange(z_min, z_max, z_step):
            x_prev, y_prev = data_x[0], f(data_x[0], z)
            x_prev, y_prev = self.transform_points(x_prev, y_prev, z)

            x_left, y_left = self.side_edge(x_prev, y_prev, x_left, y_left)
            prev_flag = self.is_visible(x_prev, y_prev)

            for x in frange(x_min, x_max, x_step):
                y = f(x, z)
                x, y = self.transform_points(x, y, z)

                flag = self.is_visible(x, y)
                if (flag == prev_flag):
                    if (flag != 0):
                        self.draw_cut(x_prev, y_prev, x, y)
                        self.make_horizons(x_prev, y_prev, x, y)
                else:
                    if (flag == 0):
                        if (prev_flag == 1):
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.up_arr)
                        else:
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.down_arr)

                        self.draw_cut(x_prev, y_prev, x_cross, y_cross)
                        self.make_horizons(x_prev, y_prev, x_cross, y_cross)
                    elif (flag == 1):
                        if (prev_flag == 0):
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.up_arr)
                            self.draw_cut(x_cross, y_cross, x, y)
                            self.make_horizons(x_cross, y_cross, x, y)
                        else:
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.down_arr)
                            self.draw_cut(x_prev, y_prev, x_cross, y_cross)
                            self.make_horizons(x_prev, y_prev, x_cross, y_cross)

                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.up_arr)
                            self.draw_cut(x_cross, y_cross, x, y)
                            self.make_horizons(x_cross, y_cross, x, y)
                    else:
                        if (prev_flag == 0):
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.down_arr)
                            self.draw_cut(x, y, x_cross, y_cross)
                            self.make_horizons(x_cross, y_cross, x, y)
                        else:
                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.up_arr)
                            self.draw_cut(x_prev, y_prev, x_cross, y_cross)
                            self.make_horizons(x_prev, y_prev, x_cross, y_cross)

                            x_cross, y_cross = self.find_cross(x_prev, y_prev, x, y, self.down_arr)
                            self.draw_cut(x_cross, y_cross, x, y)
                            self.make_horizons(x_cross, y_cross, x, y)
                prev_flag = flag
                x_prev, y_prev = x, y

            x_right, y_right = self.side_edge(x, y, x_right, y_right)

    def side_edge(self, x, y, x_edge, y_edge):
        if (x_edge != -1):
            self.make_horizons(x_edge, y_edge, x, y)
            #self.draw_cut(x_edge, y_edge, x, y)
        return x, y

    def make_horizons(self, x1, y1, x2, y2):
        x1, x2 = int(x1), int(x2)
        if (x1 == x2):
            self.up_arr[x2] = max(self.up_arr[x2], y2)
            self.down_arr[x2] = min(self.down_arr[x2], y2)
        else:
            k = (y2 - y1) / (x2 - x1)
            for x in range(x1, x2 + 1):
                y = k * (x - x1) + y1
                self.up_arr[x] = max(self.up_arr[x], y)
                self.down_arr[x] = min(self.down_arr[x], y)

    def is_visible(self, x, y):
        x = int(x)
        if (x > len(self.down_arr) or x > len(self.up_arr)):
            return 0
        if (self.down_arr[x] < y and y < self.up_arr[x]):
            flag = 0
        elif (y >= self.up_arr[x]):
            flag = 1
        else:
            flag = -1

        return flag

    def find_cross(self, x1, y1, x2, y2, hor_arr):
        x1, x2 = int(x1), int(x2)
        if (x1 == x2):
            xi, yi = x2, hor_arr[x2]
        else:
            k = (y2 - y1) / (x2 - x1)
            y_sign = sign(round(y1 + k - hor_arr[x1 + 1]))
            c_sign = y_sign
            xi, yi = x1 + 1, y1 + k

            while (c_sign == y_sign and xi < x2):
                yi += k
                xi += 1
                c_sign = sign(round(yi - hor_arr[xi]))

            if (fabs(yi - k - hor_arr[xi - 1]) <= fabs(yi - hor_arr[xi - 1])):
                yi -= k
                xi -= 1

        return xi, yi

def f1(x, z):
    return 5 * x + 3 * z - 7

def f2(x, z):
    return x ** 2 + z ** 2

def f3(x, z):
    return x ** 2 - 2 * z ** 2

def f4(x, z):
    return sin(x * z)

def f5(x, z):
    return x ** 2 * z

def f6(x, z):
    return (x * z) ** 2

def funcs(ind):
    func_arr = [f1, f2, f3, f4, f5, f6]
    return func_arr[ind]

def frange(a, b, step=1):
    arr = []
    while (a <= b + EPS):
        arr.append(a)
        a += step
    return arr

def sign(x):
    if (not x): return 0
    if (x > 0): return 1
    if (x < 0): return -1
