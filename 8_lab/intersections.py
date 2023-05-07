import time

from PyQt5.QtCore import QPoint, QPointF
from drawing_algos import get_rect_points

EPS = 1e-9

from math import isclose


def get_vect(dot_1, dot_2):
    return QPointF(dot_2.x() - dot_1.x(), dot_2.y() - dot_1.y())


def get_vect_scalar_dot(vect_1, vect_2):
    return (vect_1.x() * vect_2.x()) + (vect_1.y() * vect_2.y())


def get_vect_mul(fvector, svector):
    return fvector.x() * svector.y() - fvector.y() * svector.x()


def is_polygon_valid(polygon):  # polygon lines
    if len(polygon) < 3:
        return False

    vect1 = get_vect(polygon[0], polygon[1])
    vect2 = get_vect(polygon[1], polygon[2])

    sign = None
    if get_vect_mul(vect1, vect2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(len(polygon)):
        vecti = get_vect(polygon[i - 2], polygon[i - 1])
        vectj = get_vect(polygon[i - 1], polygon[i])

        if sign * get_vect_mul(vecti, vectj) < 0:
            return False

    if sign < 0:
        polygon.reverse()

    return True


def get_perpendicular(dot_1, dot_2, pos):
    vect = get_vect(dot_1, dot_2)
    pos_vect = get_vect(dot_2, pos)

    if vect.y() != 0:
        normal = QPointF(1, - vect.x() / vect.y())
    else:
        normal = QPointF(0, 1)

    if get_vect_scalar_dot(pos_vect, normal) < 0:
        normal.setX(-normal.x())
        normal.setY(-normal.y())

    return normal


def cyrus_beck_algo(polygon, line):  # Флаг показывает видимость отрезка
    t_down = 0
    t_up = 1

    dot1 = line[0]
    dot2 = line[1]

    d = dot2 - dot1  #

    for i in range(-2, len(polygon) - 2):
        normal = get_perpendicular(polygon[i], polygon[i + 1], polygon[i + 2])

        w = dot1 - polygon[i]

        d_scalar = get_vect_scalar_dot(d, normal)
        w_scalar = get_vect_scalar_dot(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return [False, line]
            else:
                continue

        t = - w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_down = max(t_down, t)
            else:
                return [False, line]

        elif d_scalar < 0:
            if t >= 0:
                t_up = min(t_up, t)
            else:
                return [False, line]

        if t_down > t_up:
            break

    if t_down <= t_up:
        dot1_res = dot1 + d * t_down
        dot2_res = dot1 + d * t_up
        return [True, [dot1_res, dot2_res]]
    return [False, line]


def find_intersections(polygon, lines):
    ans = []
    for i in range(len(lines)):
        ans.append(cyrus_beck_algo(polygon, lines[i]))
    return ans
