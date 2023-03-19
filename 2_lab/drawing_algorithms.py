from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF
import numpy as np

from math import *

def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1

def to_radians(angle_degrees):
	return angle_degrees*pi/180.0

def rotate_OZ(x,y,angle_degrees):
    cos_val = cos(to_radians(angle_degrees));
    sin_val = sin(to_radians(angle_degrees));

    save_x = x

    x = (x) * cos_val + (y) * sin_val;
    y = (save_x) * -sin_val + (y) * cos_val;
    return x,y

def get_spectre_coords(line_len,min_angle_diff):
    spectre_coords = []
    point_1 = [0,0]
    point_2 = [0,line_len]
    angle = 0
    while(angle < 360):
        spectre_coords.append([rotate_OZ(*point_1,angle),rotate_OZ(*point_2,angle)])
        angle +=min_angle_diff
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

def bresenhamAlogorithmFloat(xFr:float,yFr:float,xTo:float,yTo:float):
    pointsList = QPolygonF()
    xTo = round(xTo)
    yTo = round(yTo)

    if isclose(xFr,xTo) and isclose(yFr,yTo):
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



        while not isclose(x,xTo) or not isclose(y,yTo):
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
    if isclose(x1, y1) and isclose(y2, y2):
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


def bresenhamAlogorithmSmooth(x1, y1, x2, y2, maxIntensivity=100, stepmode=False):
    coloredPoints = []
    if isclose(x1, y1) and isclose(y2, y2):
        coloredPoints.append([x1, y1,maxIntensivity / 2])
        return coloredPoints


    colors_intersinty = np.linspace(0,100,num=maxIntensivity)

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
    while not isclose(x, x2) and not isclose(y, y2):
        if not stepmode:
            coloredPoints.append([x, y, colors_intersinty[round(e) - 1] / maxIntensivity])
        # canvas.create_oval(x, y, x, y, outline=fill[round(e) - 1])
        if e < w:
            if swap == 0:  # dy < dx
                x += sx     # -1 if dx < 0, 0 if dx = 0, 1 if dx > 0
            else:           # dy >= dx
                y += sy     # -1 if dy < 0, 0 if dy = 0, 1 if dy > 0
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

    if stepmode:
        return steps
    return coloredPoints

