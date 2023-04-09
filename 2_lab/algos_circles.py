from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF
import numpy as np

from math import *

EPS = 1e-7


def reflect_by_x(xc, yc, dots):
    reflected = QPolygonF()
    for i in range(len(dots)):
        reflected.append(QPoint(2 * xc - dots[i].x(), dots[i].y()))
    return reflected


def reflect_by_y(xc, yc, dots):
    reflected = QPolygonF()
    for i in range(len(dots)):
        reflected.append(QPoint(dots[i].x(), 2 * yc - dots[i].y()))
    return reflected


def circle_symmetric_pixels(xc,yc,dots):
    symmetric = QPolygonF()
    for i in range(len(dots)):
        symmetric.append(QPoint(-dots[i].y() + yc + xc, -dots[i].x() + xc + yc))

    return symmetric

def cannonicalCircle(xc, yc, r):
    pointsList = QPolygonF()

    sqr_r = r ** 2

    border = round(xc + r)

    for x in range(xc, border + 1):
        y = yc + sqrt(sqr_r - (x - xc) ** 2)
        pointsList.append(QPoint(x, round(y)))

    pointsList += circle_symmetric_pixels(xc, yc, pointsList)
    pointsList += reflect_by_x(xc, yc, pointsList)
    pointsList += reflect_by_y(xc, yc, pointsList)
    return pointsList


def bresenhamCircle(xc, yc, r):
    pointsList = QPolygonF()
    x = 0
    y = r

    pointsList.append(QPoint(x + xc, y + yc))

    delta = 2 * (1 - r)

    while y >= 0:
        if delta < 0:
            d1 = 2 * delta + 2 * y - 1
            if d1 <= 0:
                x += 1
                delta += 2 * x + 1
            elif d1 > 0:
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
        elif delta > 0:
            d2 = 2 * delta - 2 * x - 1
            if d2 <= 0:
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
            elif d2 > 0:
                y -= 1
                delta -= 2 * y + 1
        else:
            x += 1
            y -= 1
            delta += 2 * (x - y + 1)

        pointsList.append(QPoint(x + xc, y + yc))

    pointsList += reflect_by_x(xc, yc, pointsList)
    pointsList += reflect_by_y(xc, yc, pointsList)
    return pointsList


def midpointCircle(xc, yc, r):
    pointsList = QPolygonF()

    x = 0
    y = r

    delta = 1 - r

    while (x <= y):

        pointsList.append(QPoint(x,y))

        x += 1

        if (delta < 0):
            delta = delta + 2 * x + 1
        else:
            y -= 1
            delta = delta + 2 * (x - y) + 1

    pointsList += circle_symmetric_pixels(xc, yc, pointsList)
    pointsList += reflect_by_x(xc, yc, pointsList)
    pointsList += reflect_by_y(xc, yc, pointsList)


    return pointsList


def parametricCircle(xc, yc, r):
    pointsList = QPolygonF()
    step = 1 / r
    cur_angle = 0
    while cur_angle <= pi / 2 + step:
        x = xc + round(r * cos(cur_angle))
        y = yc + round(r * sin(cur_angle))

        pointsList.append(QPoint(x, y))

        cur_angle += step
    pointsList += reflect_by_x(xc, yc, pointsList)
    pointsList += reflect_by_y(xc, yc, pointsList)
    return pointsList
