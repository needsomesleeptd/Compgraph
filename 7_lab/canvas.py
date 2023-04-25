from main import Qcolor_to_stylesheet

from drawing_algos import *

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent

from copy import deepcopy
from PyQt5.QtWidgets import QMessageBox


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
        self.image = QtGui.QImage(self.width() * 5, self.height() * 5, QtGui.QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        # temp_pixmap = QtGui.QPixmap.convertFromImage(self.image)
        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(self.image)
        self.pixmap_on_canvas = self.scene.addPixmap(self.pixmap)
        self.fitInView(self.pixmap_on_canvas)
        self.cur_rect = []
        self.lines = []
        self.cur_line = []
        self.pan_mode = False
        self.cut_off_color = QColor(0, 0, 0)
        self.line_color = QColor(12, 123, 56)
        self.background_color = QColor(255,255,255)
        self.fitInView(self.pixmap_on_canvas, Qt.KeepAspectRatio)
        self.save_color = QColor(255, 255, 255)
        self.saved_state = [self.image.copy(), self.lines.copy(), self.cur_rect.copy()]

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)
        # newPos = self.mapToScene(event.pos())
        # self.image = self.image.scaled(self.width(), self.height())
        # self.updatePixmap()
        # self.fitInView(self.pixmap_on_canvas)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # self.fitInView(self.pixmap_on_canvas, Qt.KeepAspectRatio)

    def drawLine(self, fr, to, color):
        points = CDA(*fr, *to)
        for point in points:
            self.image.setPixelColor(point.x(), point.y(), color)
        self.updatePixmap()

    def drawRect(self, left_point, right_point, color):
        points = get_rect_points(*left_point,
                                 *right_point)  # RectPoints возвращает точки в порядке обхода по часовой стрелке
        for i in range(len(points)):
            self.drawLine(points[i], points[(i + 1) % len(points)], color)

    def updatePixmap(self, is_reverting=False):
        # print(self.saved_state)
        # if (not is_reverting):
        #    self.saved_state[0] = self.pixmap.toImage().copy()
        # super().fitInView(self.pixmap_on_canvas)
        self.image = self.image.scaled(self.width(), self.height())
        self.pixmap.convertFromImage(self.image)
        self.pixmap_on_canvas.setPixmap(self.pixmap)

    def clear_cur_rect(self):
        self.drawRect(*self.cur_rect,self.background_color)
        self.cur_rect = []

    def add_dot_rect(self, pos):
        self.save_state()
        if (len(self.cur_rect) >= 2):
            self.clear_cur_rect()


        if (len(self.cur_rect) == 0):
            self.image.setPixelColor(pos.x(), pos.y(), self.pen.color())
        else:
            self.drawRect(self.cur_rect[0], [pos.x(), pos.y()],self.pen.color())
        self.cur_rect.append([pos.x(), pos.y()])
        self.dotsPrintSignal.emit(pos.x(), pos.y())

    def add_dot_line(self, pos):
        if (len(self.cur_line) == 0):
            self.cur_line.append([pos.x(), pos.y()])
        else:
            self.cur_line.append([pos.x(), pos.y()])
            self.drawLine(*self.cur_line,self.line_color)
            self.lines.append(self.cur_line)
            self.cur_line = []
        self.updatePixmap()

    def update_seed_point(self, x, y):
        self.saved_state[3] = self.seed_point.copy()
        self.image.setPixelColor(*self.seed_point, self.save_color)
        self.seed_point = [x, y]
        self.save_color = get_pixel_color(self, *self.seed_point)
        self.image.setPixelColor(*self.seed_point, self.seed_color)
        self.updatePixmap()

    def mousePressEvent(self, event):
        title_str = "Ошибка"
        warning_str = "Попытка поставить точку вне  рабочей поверхности"
        super().mousePressEvent(event)
        if not self.pan_mode:

            pos = self.mapToScene(event.pos())
            if pos.x() <= 0 or pos.x() >= self.width():
                self.show_message(title_str, warning_str)
                return

            if pos.y() <= 0 or pos.y() >= self.height():
                self.show_message(title_str, warning_str)
                return
            self.save_state()
            if event.buttons() == QtCore.Qt.LeftButton:
                self.add_dot_rect(pos)

            if event.buttons() == QtCore.Qt.RightButton:
                self.add_dot_line(pos)

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
        self.save_state()
        self.image.fill(QColor(255, 255, 255))  # getting white color
        self.polygons = []
        self.cur_rect = []
        self.clearSignal.emit()
        self.updatePixmap()

    def get_params(self):
        # canvas_copy = self.image.copy()
        return [self, self.pen.color(), self.fill_color, self.seed_point, self.polygons]

    def save_state(self):
        self.saved_state = [self.image.copy(), self.lines.copy(), self.cur_rect.copy()]

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()
