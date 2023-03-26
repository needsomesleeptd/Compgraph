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


'''def bresenhamAlogorithmFloat(xFr:int,yFr:int,xTo:int,yTo:int):
	points = QPolygonF()
	deltaX =  abs(xFr - xTo)
	deltaY = abs(yFr - yTo)
	error = 0
	deltaError = (deltaY + 1) / (deltaX + 1)
	y = yFr
	dirY = yTo - yFr
	if dirY > 0:
		dirY = 1
	if dirY < 0:
		dirY = -1
		
	
	for x in range(xFr,yTo + 1):
		point = QPoint(x,y)
		points.append(point)
		error = error + deltaError
		if error >= 1.0:
			y = y + dirY
			error = error - 1.0
	return points'''


def bresenhamAlogorithmFloat(xFr: float, yFr: float, xTo: float, yTo: float):
    pointsList = QPolygonF()
    xTo = round(xTo)
    yTo = round(yTo)

    if isclose(xFr, xTo) and isclose(yFr, yTo):
        pointsList.append(QPoint(xFr, yFr))
    else:
        dx = xTo - xFr
        dy = yTo - yFr

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        tg = dy / dx
        e = tg - 0.5
        x = xFr
        y = yFr

        while not isclose(x, xTo) or not isclose(y, yTo):
            pointsList.append(QPoint(x, y))

            if e >= 0:
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 1

            if e <= 0:
                if exchange == 0:
                    x += sx
                else:
                    y += sy
                e += tg

    return pointsList


def bresenhamAlogorithmInt(x1, y1, x2, y2, colour='black', stepmode=False):
    pointsList = QPolygonF()
    x2 = round(x2)
    y2 = round(y2)
    if isclose(x1, x2) and isclose(y1, y2):
        pointsList.append(QPoint(x1, y1))
    else:
        dx = x2 - x1
        dy = y2 - y1

        sx = sign(dx)
        sy = sign(dy)

        dy = abs(dy)
        dx = abs(dx)

        if dy > dx:
            dx, dy = dy, dx
            exchange = 1
        else:
            exchange = 0

        e = 2 * dy - dx
        x = x1
        y = y1

        xb = x
        yb = y
        steps = 0

        while not isclose(x, x2) or not isclose(y, y2):
            if stepmode == False:
                pointsList.append(QPoint(x, y))

            if e >= 0:
                if exchange == 1:
                    x += sx
                else:
                    y += sy
                e -= 2 * dx  # отличие от вещественного (e -= 1)
            if e <= 0:
                if exchange == 0:
                    x += sx
                else:
                    y += sy
                e += 2 * dy  # difference (e += tg)

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

        if stepmode:
            return steps
    return pointsList


def bresenhamAlogorithmSmooth(x1, y1, x2, y2, maxIntensivity=7, stepmode=False):
    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
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


def VU(x1, y1, x2, y2, stepmode=False):
    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
    if (x1 > x2):
        x1, x2 = x2, x1
    if (y1 > y2):
        y1, y2 = y2, y1

    coloredPoints = []

    if (isclose(x1, x2)):
        for y_cur in range(int(y1), round(y2)):
            coloredPoints.append([x1, y_cur, 1])

    elif (isclose(y1, y2)):
        for x_cur in range(int(x1), round(x2)):
            coloredPoints.append([x_cur, y1, 1])

    if (x1 == x2 or y1 == y2):  # if the line is straight
        return coloredPoints

    if isclose(x1, x2) and isclose(y1, y2):
        coloredPoints.append([x1, y1, 1])  # 100 percent
        return coloredPoints

    swapped = abs(y2 - y1) > abs(x2 - x1)

    if swapped:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x2, x1 = x1, x2

    dx = x2 - x1
    dy = y2 - y1
    tg = dy / dx
    xend = round(x1)
    yend = y1 + tg * (xend - x1)
    xpx1 = xend
    y = yend + tg

    xend = int(x2 + 0.5)
    xpx2 = xend
    st = 0
    if swapped:
        for x in range(xpx1, xpx2):
            point_from = [int(y), x + 1]
            point_to = [int(y) + 1, x + 2]
            point_from_another = [int(y) + 1, x + 1]
            point_to_another = [int(y) + 2, x + 2]
            coloredPoints.append([*point_from, abs(1 - y + int(y))])
            coloredPoints.append([*point_to, abs(y + int(y))])
            coloredPoints.append([*point_from_another, abs(1 - y + int(y))])
            coloredPoints.append([*point_to_another, abs(y + int(y))])


    else:
        for x in range(xpx1, xpx2):
            point_from = [x + 1, int(y)]
            point_to = [x + 2, int(y) + 1]
            point_from_another = [x + 1, int(y) + 1]
            point_to_another = [x + 2, int(y) + 2]
            coloredPoints.append([*point_from, abs(1 - y + int(y))])
            coloredPoints.append([*point_to, abs(y + int(y))])
            coloredPoints.append([*point_from_another, abs(1 - y + int(y))])
            coloredPoints.append([*point_to_another, abs(y + int(y))])
    y += tg
    return coloredPoints
