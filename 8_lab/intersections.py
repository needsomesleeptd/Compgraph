import time

from PyQt5.QtCore import QPoint, QPointF
from drawing_algos import get_rect_points

EPS = 1e-9

from math import isclose


def get_vect(dot_1, dot_2):
    return QPointF(dot_2.x() - dot_1.x(), dot_2.y() - dot_1.y())


def get_vect_scalar_dot(vect_1, vect_2):
    return (vect_2.x() * vect_1.x()) + (vect_1.y() + vect_2.y())


def is_polygon_valid(polygon):  # polygon lines
    if (len(polygon) < 3):
        return False
    first_dot = polygon[0]
    second_dot = polygon[1]
    third_dot = polygon[2]
    vect_1 = get_vect(first_dot, second_dot)
    vect_2 = get_vect(second_dot, third_dot)
    scalar_dot = get_vect_scalar_dot(vect_1, vect_2)
    turn_sign = 1

    if (scalar_dot < 0):
        turn_sign -= 1

    for i in range(len(polygon)):
        first_dot = polygon[i]
        second_dot = polygon[i - 1]
        third_dot = polygon[i - 2]
        vect_1 = get_vect(first_dot, second_dot)
        vect_2 = get_vect(second_dot, third_dot)
        scalar_dot = get_vect_scalar_dot(vect_1, vect_2)
        if scalar_dot * turn_sign < 0:  # Многоугольник не выпуклый
            return False
    return True


def get_perpendicular(line, dot_outside):
    vect = get_vect(*line)

    if vect.y() != 0:
        normal = QPointF(1, - vect.x() / vect.y())
    else:
        normal = QPointF(0, 1)

    if get_vect_scalar_dot(get_vect(line[1], dot_outside), normal) < 0:
        normal.setX(-normal.x())
        normal.setY(-normal.y())

    return normal


def cyrus_beck_algo(polygon, line):
    t_down = 0
    t_up = 1
    D = line[1] - line[0]
    for i in range(-2, len(polygon) - 2):
        perpendicular = get_perpendicular([polygon[i], polygon[i + 1]], polygon[i + 2])
        w = line[0] - polygon[i]
        d_scalar_dot = get_vect_scalar_dot(D, perpendicular)
        w_scalar_dot = get_vect_scalar_dot(w, perpendicular)

        if d_scalar_dot == 0:
            if w_scalar_dot < 0:
                return [False, [line[0], line[1]]]
            else:
                continue

        t = -w_scalar_dot / d_scalar_dot

        if (d_scalar_dot > 0):
            if (t <= 1):
                t_down = max(t_down, t)
            else:
                return [False, [line[0], line[1]]]

        elif (d_scalar_dot < 0):
            if (t >= 0):
                t_up = min(t_up, t)
            else:
                return [False, [line[0], line[1]]]
        R1 = None
        R2 = None
        if t_down <= t_up:
            R1 = line[0] + D * t_down
            R2 = line[0] + D * t_up
            return [True, [R1, R2]]
        return [False, [line[0], line[1]]]


def find_intersections(polygon, lines):
    ans = []
    for i in range(len(lines)):
        ans.append(cyrus_beck_algo(polygon, lines[i]))
    return ans
