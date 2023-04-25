import time

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QPolygonF, QColor
import numpy as np
from PyQt5 import QtTest

from math import *

EPS = 1e-9

def is_fully_visible(line_point_left, line_point_right, rect_point_left, rect_point_right):  # [0] -x, [1] - y
    if (line_point_left[0] < rect_point_left[0] or line_point_left[0] > rect_point_right[0]):
        return False
    elif (line_point_right[0] < rect_point_left[0] or line_point_right[0] > rect_point_right[0]):
        return False
    elif (line_point_right[1] < rect_point_left[1] or line_point_right[1] > rect_point_right[1]):
        return False
    elif (line_point_left[1] < rect_point_left[1] or line_point_left[1] > rect_point_right[1]):
        return False
    return True


def is_fully_invisible(line_point_left, line_point_right, rect_point_left, rect_point_right):  # [0] -x, [1] - y
    if (line_point_left[0] < rect_point_left[0] and line_point_right[0] < rect_point_left[0]):
        return True
    elif (line_point_left[0] > rect_point_right[0] and line_point_right[0] > rect_point_right[0]):
        return True
    elif (line_point_left[1] < rect_point_left[1] and line_point_right[0] < rect_point_left[1]):
        return True
    elif (line_point_left[1] > rect_point_right[1] and line_point_right[0] > rect_point_right[1]):
        return True
    return False


def get_bin_visibility(point, rect_point_left, rect_point_right):
    bin_visibility = [0, 0, 0, 0]
    if point.x() < rect_point_left.x():
        bin_visibility[3] = 1
    if point.x() > rect_point_right.x():
        bin_visibility[2] = 1
    if point.y() > rect_point_right.y():
        bin_visibility[1] = 1
    if point.y() < rect_point_left.y():
        bin_visibility[0] = 1
    return bin_visibility



def find_intersection(line, rect): # flag shows whether it is visible or not
    T1 = get_bin_visibility(line[0], rect[0], rect[1])
    T2 = get_bin_visibility(line[1], rect[0], rect[1])
    sum1 = sum(T1)
    sum2 = sum(T2)
    P1 = line[0]
    P2 = line[1]
    if sum1 == 0 and  sum2 == 0:
        return [1,[P1,P2]]
    if sum1 ^ sum2 != 0:
        return [0, [P1, P2]]

    R1 = P1
    R2 = P2
    flag = 1
    if (sum1 != 0):
        R1,flag = get_visible_coords(flag,P1,P2,rect,is_first=True)

    if (sum2 != 0):
        R2, flag = get_visible_coords(flag, P1, P2, rect, is_first=False)

    return [flag,[R1,R2]]








def get_visible_coords(flag,  P1, P2, rect, is_first):
    m = 1e30
    P = None
    if (is_first):
        P = P1
    else:
        P = P2

    if (P1.x() != P2.x()):
        m = (P2.y() - P1.y()) / (P1.x() - P2.x())
        #left_check
        if rect[0].x() >= P.x():
            y = m * (rect[0].x() - P.x()) + P.y()
            if y <= rect[1].y() and y >= rect[0].y():
                return [QPointF(rect[0].x(), y),flag]
        #up_check
        if rect[0].x() <= P.x():
            y = m * (rect[1].x() - P.x()) + P.y()
            if y <= rect[1].y() and y >= rect[0].y():
                return [QPointF(rect[1].x(), y),flag]

    if (abs(m) <= EPS):
        flag = 0
        return [P,flag]

    #lower_bound_check
    if rect[1].y() >= P.y():
        x = (1 / m) * (rect[1].y() - P.y()) + P.x()
        if (x >= rect[0].x() and x <= rect[1].x()):
            return [QPointF(x, rect[1].y()),flag]

    #up_bound_check
    if rect[0].y() <= P.y():
        x = (1 / m) * (rect[0].y() - P.y()) + P.x()
        if (x >= rect[0].x() and x <= rect[1].x()):
            return [QPointF(x, rect[0].y()),flag]
    flag = 0
    return [P,flag]


def find_intersections(lines,rect):
    intersections = []
    for line in lines:
        intersections.append(find_intersection(line,rect))
    return intersections




'''
def l_bound_check(index, P1, P2, P, rect)
    x1 = P1.x()
    x2 = P2.x()
    y1 = P1.y()
    y2 = P2.y()
    if P2.x() - P1.x() == 0:
        return
    m = (y1 - y1) / (x2 - x1)
    if (rect[0].x() < P.x()):
        return 'not_found'
    y = m * (rect[0].x() - P.x()) + P.y()
    if y > rect[1].y():
        return 'not_found'
    elif y < rect[0].y():
        return 'not_found'
    else:
        P = QPointF(rect[0].x, y)
        return cuttting(index, P1, P2, P, rect)


def r_bound_check(index, P1, P2, P, rect)
    x1 = P1.x()
    x2 = P2.x()
    y1 = P1.y()
    y2 = P2.y()
    m = (y1 - y1) / (x2 - x1)
    if rect[1].x() > P.x():
        return '4'
    y = m * (rect[1].x() - P.x()) + P.y()
    if y > rect[1].y():
        return '4'
    if y < rect[0].y():
        return '4'

    P = QPointF(rect[1].x, y)
    return '1'


def up_bound_check(index, P1, P2, P, rect):
    x1 = P1.x()
    x2 = P2.x()
    y1 = P1.y()
    y2 = P2.y()
    m = (y1 - y1) / (x2 - x1)
    if m == 0:
        return 'horizontal'
    if rect[1].y() > P.y():
        return '5'
    x = (1 / m) * (rect[0].y() - P.y()) + P.x()
    if x < rect[0].x():
        return '5'
    if x > rect[1].x():
        return '5'


def low_bound_check(index, P1, P2, P, rect):
    x1 = P1.x()
    x2 = P2.x()
    y1 = P1.y()
    y2 = P2.y()
    m = (y1 - y1) / (x2 - x1)
    if rect[0].y() < P.y():
        return 'error'

    x = (1 / m) * (rect[1].y() - P.y()) + P.x()
    if x < rect[0].x():
        return '6'

    if x > rect[1].x():
        return '6'

    P = QPointF(x, rect[1].y())
    return '1'
'''

