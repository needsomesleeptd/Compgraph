from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF
import numpy as np

from math import *


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
        new_coord[0][0] += point_center[0]
        new_coord[0][1] += point_center[1]
        new_coord[1][0] += point_center[0]
        new_coord[1][1] += point_center[1]
        spectre_coords.append(new_coord)
        angle += min_angle_diff
    return spectre_coords


def bresenhamAlogorithmFloat(xFr: float, yFr: float, xTo: float, yTo: float, stepmode=False):
    pointsList = QPolygonF()
    xTo = ceil(xTo)
    yTo = ceil(yTo)
    xFr = floor(xFr)
    yFr = floor(yFr)
    steps = 0
    if isclose(xFr, xTo) and isclose(yFr, yTo):
        pointsList.append(QPoint(xFr, yFr))
    else:

        dx = xTo - xFr
        dy = yTo - yFr
        exchange = 0
        if (abs(dy) > abs(dx)):
            xFr, yFr = yFr, xFr
            xTo, yTo = yTo, xTo
            dx, dy = dy, dx
            exchange = 1

        steps = 1
        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        tg = dy / dx
        e = tg
        x = xFr
        y = yFr

        xb = x
        yb = y

        for x in range(xFr, xTo + 1, sx):
            if exchange:
                pointsList.append(QPoint(y, x))
            else:
                pointsList.append(QPoint(x, y))

            e += tg
            if (e > 0.5):
                y += sy
                e = e - 1

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

    if stepmode:
        return steps
    return pointsList


def bresenhamAlogorithmInt(x1, y1, x2, y2, stepmode=False):
    pointsList = QPolygonF()
    x2 = ceil(x2)
    y2 = ceil(y2)
    x1 = floor(x1)
    y1 = floor(y1)
    if isclose(x1, x2) and isclose(y1, y2):
        pointsList.append(QPoint(x1, y1))
    else:
        dx = x2 - x1
        dy = y2 - y1

        exchange = 0
        if (abs(dy) > abs(dx)):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
            exchange = 1

        steps = 1
        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        e = 2 * dy - dx
        x = x1
        y = y1

        xb = x
        yb = y

        for x in range(x1, x2 + 1, sx):
            if exchange:
                pointsList.append(QPoint(y, x))
            else:
                pointsList.append(QPoint(x, y))

            e += 2 * dy
            if (e >= 0):
                y += sy
                e = e - 2 * dx

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

    if stepmode:
        return steps
    return pointsList


def bresenhamAlogorithmSmooth(x1, y1, x2, y2, maxIntensivity=7, stepmode=False):
    # x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
    x2 = ceil(x2)
    y2 = ceil(y2)
    x1 = floor(x1)
    y1 = floor(y1)
    coloredPoints = []
    if isclose(x1, x2) and isclose(y1, y2):
        coloredPoints.append([x1, y1, 1])
        return coloredPoints

    colors_intersinty = np.linspace(0, maxIntensivity, num=maxIntensivity)

    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)

    if dy >= dx:
        dx, dy = dy, dx
        swap = 1  #
    else:
        swap = 0  #
    tg = dy / dx * maxIntensivity  # тангенс угла наклона (умножаем на инт., чтобы не приходилось умножать внутри цикла
    e = maxIntensivity / 2  # интенсивность для высвечивания начального пикселя
    w = maxIntensivity - tg  # пороговое значение
    x = x1
    y = y1

    xb = x
    yb = y
    steps = 0

    # i <= dx i = 0
    # for i in range(0, dx + 1):
    # i = 0
    # while i <= dx:
    while not (my_isclose(x, x2) and my_isclose(y, y2)):
        if not stepmode:
            if (e >= 2):
                coloredPoints.append([x, y, colors_intersinty[round(e) - 1] / maxIntensivity])
        # canvas.create_oval(x, y, x, y, outline=fill[round(e) - 1])
        if e < w:
            if swap == 0:  # dy < dx
                x += sx  # -1 if dx < 0, 0 if dx = 0, 1 if dx > 0
            else:  # dy >= dx
                y += sy  # -1 if dy < 0, 0 if dy = 0, 1 if dy > 0
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w

        if stepmode:
            if xb != x and yb != y:
                steps += 1
            xb = x
            yb = y
    # print(x,y,x2,y2)

    if stepmode:
        return steps
    return coloredPoints


def CDA(x1, y1, x2, y2, stepmode=False):
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
        for i in range(0, int(length) + 1):
            if not stepmode:
                pointsList.append((QPoint(round(x), round(y))))
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1
            x += dx
            y += dy
    if stepmode:
        return steps
    return pointsList


def f_part(x):
    return abs(x - int(x))


def VU(x1, y1, x2, y2, step_count=False):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [[x1, y1, 1]]

    m = 1

    step = 1
    steps = 0
    points = []

    if abs(dy) >= abs(dx):
        if dy != 0:
            m = dx / dy

        m1 = m

        if y1 > y2:
            m1 *= -1
            step *= -1

        bord = round(y2) - 1 if dy < dx else round(y2) + 1

        for y in range(round(y1), bord, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            if step_count == False:
                points.append([int(x1) + 1, y, fabs(d2)])
                points.append([int(x1), y, fabs(d1)])

            elif y < round(y2) and int(x1) != int(x1 + m):
                steps += 1

            x1 += m1
    else:
        if dx != 0:
            m = dy / dx

        m1 = m

        if x1 > x2:
            step *= -1
            m1 *= -1

        bord = round(x2) - 1 if dy > dx else round(x2) + 1

        for x in range(round(x1), bord, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            if step_count == False:
                points.append([x, int(y1) + 1, fabs(d2)])
                points.append([x, int(y1), fabs(d1)])

            elif x < round(x2) and int(y1) != int(y1 + m):
                steps += 1

            y1 += m1

    if step_count:
        return steps
    else:
        return points
