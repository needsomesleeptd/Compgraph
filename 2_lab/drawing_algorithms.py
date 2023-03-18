from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF

def bresenhamAlogorithmFloat(xFr:int,yFr:int,xTo:int,yTo:int):
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
    return points




