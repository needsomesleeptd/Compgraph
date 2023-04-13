
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

        for x in range(xFr, xTo + sx, sx):
            if exchange:
                pointsList.append(QPoint(y, x))
            else:
                pointsList.append(QPoint(x, y))

            if (e > 0.5):
                y += sy
                e = e - 1
            e += tg

            if stepmode:
                if xb != x and yb != y:
                    steps += 1
                xb = x
                yb = y

    if stepmode:
        return steps
    return pointsList
