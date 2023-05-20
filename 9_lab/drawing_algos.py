import time

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QPolygonF, QColor
import numpy as np
from PyQt5 import QtTest

from math import *


def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1


def CDA(x1: float, y1: float, x2: float, y2: float, stepmode=False):
    x2 = ceil(x2)
    y2 = ceil(y2)
    x1 = floor(x1)
    y1 = floor(y1)
    pointsList = QPolygonF()
    steps = 0

    if x1 == x2 and y1 == y2:
        pointsList.append(QPoint(round(x1), round(y1)))
    else:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # steep - max growth
        if dx >= dy:
            length = dx
        else:
            length = dy
        dx = (x2 - x1) / length  # step of x
        dy = (y2 - y1) / length  # step of y

        # set line to start
        x = x1
        y = y1

        # i <= lenght i = 0
        # while abs(x - x2) > 1 or abs(y - y2) > 1:
        for i in range(0, round(length) + 1):

            if not stepmode:
                pointsList.append((QPoint(x, y)))
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1

            x += dx
            y += dy
    if stepmode:
        return steps
    return pointsList


def get_pixel_color(canvas, x, y):
    return QColor(canvas.image.pixel(x, y))


def get_rect_points(x_l, y_u, x_r, y_d):
    #pointsList = QPolygonF()
    #pointsList += CDA(x_l, y_u, x_r, y_u)
    #pointsList += CDA(x_r, y_u, x_r, y_d)
    #pointsList += CDA(x_l, y_d, x_r, y_u)
    #pointsList += CDA(x_l, y_u, x_l, y_d)
    return [[x_l, y_u], [x_r, y_u], [x_r, y_d], [x_l, y_d]]


