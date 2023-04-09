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


def my_isclose(x, y, EPS=0.1):
    return isclose(x, y, abs_tol=EPS)


def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1


def to_radians(angle_degrees):
    return angle_degrees * pi / 180.0


def rotate_OZ(x, y, angle_degrees):
    cos_val = cos(to_radians(angle_degrees))
    sin_val = sin(to_radians(angle_degrees))

    save_x = x

    x = (x) * cos_val + (y) * sin_val
    y = (save_x) * -sin_val + (y) * cos_val
    return [x, y]


def get_spectre_coords(line_len, point_center, min_angle_diff):
    spectre_coords = []
    point_1 = [0, 0]
    point_2 = [0, line_len]
    angle = 0
    while (angle < 360):
        new_coord = [rotate_OZ(*point_1, angle), rotate_OZ(*point_2, angle)]
        if (fabs(new_coord[1][0]) < EPS):  # Убираем погрешность при повороте
            new_coord[1][0] = 0

        new_coord[0][0] += point_center[0]
        new_coord[0][1] += point_center[1]
        new_coord[1][0] += point_center[0]
        new_coord[1][1] += point_center[1]

        spectre_coords.append(new_coord)
        angle += min_angle_diff
    return spectre_coords


def cannonicalEllipse(xc, yc, A, B):
    points = QPolygonF()
    sqr_ra = A * A
    sqr_rb = B * B

    border_x = round(xc + A / sqrt(1 + sqr_rb / sqr_ra))
    border_y = round(yc + B / sqrt(1 + sqr_ra / sqr_rb))

    for x in range(round(xc), border_x + 1):
        y = yc + sqrt(sqr_ra * sqr_rb - (x - xc) ** 2 * sqr_rb) / A

        points.append(QPoint(x, round(y)))

    for y in range(border_y, round(yc) - 1, -1):
        x = xc + sqrt(sqr_ra * sqr_rb - (y - yc) ** 2 * sqr_ra) / B
        points.append(QPoint(round(x), y))

    points += reflect_by_x(xc, yc, points)
    points += reflect_by_y(xc, yc, points)
    return points


def parameterEllipse(xc, yc, A, B):
    points = QPolygonF()
    if A > B:
        step = 1 / A
    else:
        step = 1 / B

    i = 0
    while i <= pi / 2 + step:
        x = xc + round(A * cos(i))
        y = yc + round(B * sin(i))

        points.append(QPoint(x, y))

        i += step
    points += reflect_by_x(xc, yc, points)
    points += reflect_by_y(xc, yc, points)
    return points


def bresenhamEllipse(xc, yc, A, B):
    points = QPolygonF()
    x = 0
    y = B

    sqr_ra = A * A
    sqr_rb = B * B
    delta = 4 * sqr_rb * ((x + 1) * (x + 1)) + sqr_ra * ((2 * y - 1) * (2 * y - 1)) - 4 * sqr_ra * sqr_rb
    # Теперь рассматриваем функцию от (x + 1, y - 1 / 2)
    while sqr_ra * (2 * y - 1) > 2 * sqr_rb * (x + 1):

        points.append(QPoint(x + xc, y + yc))
        if (delta < 0):
            x += 1
            delta += 4 * sqr_rb * (2 * x + 3)
        else:
            x += 1
            delta = delta - 8 * sqr_ra * (y - 1) + 4 * sqr_rb * (2 * x + 3)
            y -= 1

    delta = sqr_rb * ((2 * x + 1) * (2 * x + 1)) + 4 * sqr_ra * ((y + 1) * (y + 1)) - 4 * sqr_ra * sqr_rb
    # Теперь рассматриваем функцию от (x + 1/2, y - 1)

    while (y + 1 > 0):
        points.append(QPoint(x + xc, y + yc))
        if (delta < 0):
            y -= 1
            delta += 4 * sqr_ra * (2 * y + 3)
        else:
            y -= 1
            delta = delta - 8 * sqr_rb * (x + 1) + 4 * sqr_ra * (2 * y + 3)
            x += 1


    points += reflect_by_x(xc, yc, points)
    points += reflect_by_y(xc, yc, points)
    return points


def midpointEllipse(xc, yc, A, B):
    pointsList = QPolygonF()
    sqr_ra = A * A
    sqr_rb = B * B

    x = 0
    y = B

    pointsList.append(QPoint(x + xc, y + yc))

    border = round(A / sqrt(1 + sqr_rb / sqr_ra))
    delta = sqr_rb - round(sqr_ra * (B - 1 / 4))

    while x <= border:
        if delta < 0:
            x += 1
            delta += 2 * sqr_rb * x + 1
        else:
            x += 1
            y -= 1
            delta += 2 * sqr_rb * x - 2 * sqr_ra * y + 1

        pointsList.append(QPoint(x + xc, y + yc))

    x = A
    y = 0

    pointsList.append(QPoint(x + xc, y + yc))

    border = round(B / sqrt(1 + sqr_ra / sqr_rb))
    delta = sqr_ra - round(sqr_rb * (A - 1 / 4))

    while y <= border:
        if delta < 0:
            y += 1
            delta += 2 * sqr_ra * y + 1
        else:
            x -= 1
            y += 1
            delta += 2 * sqr_ra * y - 2 * sqr_rb * x + 1

        pointsList.append(QPoint(x + xc, y + yc))
    pointsList += reflect_by_x(xc, yc, pointsList)
    pointsList += reflect_by_y(xc, yc, pointsList)
    return pointsList
