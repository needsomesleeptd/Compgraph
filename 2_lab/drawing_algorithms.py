from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF
import numpy as np

def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1



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

def bresenhamAlogorithmFloat(xFr:int,yFr:int,xTo:int,yTo:int):
    pointsList = QPolygonF()

    if xFr == xTo and yFr == yTo:
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



        while x != xTo or y != yTo:
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
    if x1 == x2 and y1 == y2:
        pointsList.append([x1, y1, colour])
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

        while x != x2 or y != y2:
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
    while x != x2 or y != y2:
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

