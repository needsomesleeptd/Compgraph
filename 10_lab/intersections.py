import time
import numpy as np

from PyQt5.QtCore import QPoint, QPointF
from drawing_algos import get_rect_points

EPS = 1e-9

from math import isclose


def get_vect(dot_1, dot_2):
    return QPointF(dot_2.x() - dot_1.x(), dot_2.y() - dot_1.y())


def get_vect_scalar_dot(vect_1, vect_2):
    return (vect_1.x() * vect_2.x()) + (vect_1.y() * vect_2.y())


def get_vect_vector_dot(vect_1, vect_2):
    return vect_1.x() * vect_2.y() - vect_1.y() * vect_2.x()


def visibility(point, begin, end):
    tmp1 = (point.x() - begin.x()) * (end.y() - begin.y())
    tmp2 = (point.y() - begin.y()) * (end.x() - begin.x())
    res = tmp1 - tmp2

    if -1e-7 < res < 1e-7:
        res = 0
    return np.sign(res)


def check_lines_crossing(begin1, end1, begin2, end2):
    vis1 = visibility(begin1, begin2, end2)
    vis2 = visibility(end1, begin2, end2)

    if (vis1 < 0 and vis2 > 0) or (vis1 > 0 and vis2 < 0):
        return True
    else:
        return False


def make_identity(matrix):
    # перебор строк в обратном порядке
    for nrow in range(len(matrix) - 1, 0, -1):
        row = matrix[nrow]
        for upper_row in matrix[:nrow]:
            factor = upper_row[nrow]
            upper_row -= factor * row
    return matrix


def solve_by_gauss(matrix):
    for nrow in range(len(matrix)):
        # nrow равен номеру строки
        # np.argmax возвращает номер строки с максимальным элементом в уменьшенной матрице
        # которая начинается со строки nrow. Поэтому нужно прибавить nrow к результату
        pivot = nrow + np.argmax(abs(matrix[nrow:, nrow]))
        if pivot != nrow:
            # swap
            # matrix[nrow], matrix[pivot] = matrix[pivot], matrix[nrow] - не работает.
            # нужно переставлять строки именно так, как написано ниже
            matrix[[nrow, pivot]] = matrix[[pivot, nrow]]
        row = matrix[nrow]
        divider = row[nrow]  # диагональный элемент
        if abs(divider) < 1e-20:
            # почти нуль на диагонали. Продолжать не имеет смысла, результат счёта неустойчив
            raise ValueError(f"Матрица несовместна. Максимальный элемент в столбце {nrow}: {divider:.3g}")

        # делим на диагональный элемент.
        row /= divider
        # теперь надо вычесть приведённую строку из всех нижележащих строчек
        for lower_row in matrix[nrow + 1:]:
            factor = lower_row[nrow]  # элемент строки в колонке nrow
            lower_row -= factor * row  # вычитаем, чтобы получить ноль в колонке nrow
        # приводим к диагональному виду
    make_identity(matrix)
    return matrix[:, -1]


def get_cross_point(begin1, end1, begin2, end2):
    coef = []
    coef.append([end1.x() - begin1.x(), begin2.x() - end2.x()])
    coef.append([end1.y() - begin1.y(), begin2.y() - end2.y()])

    rights = []
    rights.append([begin2.x() - begin1.x()])
    rights.append([begin2.y() - begin1.y()])

    coef_tmp = np.matrix(coef)
    coef_tmp = coef_tmp.I
    coef = [[coef_tmp.item(0), coef_tmp.item(1)], [coef_tmp.item(2), coef_tmp.item(3)]]

    coef_tmp = np.matrix(coef)
    param = coef_tmp.__mul__(rights)

    x, y = begin1.x() + (end1.x() - begin1.x()) * param.item(0), begin1.y() + (end1.y() - begin1.y()) * param.item(0)

    return QPointF(x, y)


def sutherland_hodgman(polygon, clipper):
    p = polygon.copy()
    q = []
    w = clipper.copy()
    w.append(clipper[0])
    np = len(p)
    nw = len(w)

    s = []
    f = []
    for i in range(nw - 1):
        nq = 0
        q = []
        for j in range(np):
            if j != 0:
                is_crossing = check_lines_crossing(s, p[j], w[i], w[i + 1])
                if is_crossing == True:
                    q.append(get_cross_point(s, p[j], w[i], w[i + 1]))
                    nq += 1
                else:
                    if visibility(s, w[i], w[i + 1]) == 0:
                        q.append(s)
                        nq += 1
                    elif visibility(p[j], w[i], w[i + 1]) == 0:
                        q.append(p[j])
                        nq += 1
            else:
                f = p[j]
            s = p[j]
            if visibility(s, w[i], w[i + 1]) > 0:
                continue
            q.append(s)
            nq += 1
        if nq == 0:
            p = q
            np = nq
            continue

        is_crossing = check_lines_crossing(s, f, w[i], w[i + 1])
        if is_crossing == False:
            p = q
            np = nq
            continue

        q.append(get_cross_point(s, f, w[i], w[i + 1]))
        nq += 1
        p = q
        np = nq

    return p, np


def is_polygon_valid(polygon):  # Проверят валидность и выпуклость многоугольника
    if len(polygon) < 3:  # У многоугольника точно больше 2 вершин
        return False

    vect1 = get_vect(polygon[0], polygon[1])
    vect2 = get_vect(polygon[1], polygon[2])

    sign_rot = 1
    if get_vect_vector_dot(vect1,
                           vect2) <= 0:  # Получаем значение знака поворота векторов граней относительно друг друга
        sign_rot = -1
    su = 0

    for i in range(
            len(polygon)):  # Расчитываем знак векторного произведения пары ребер, сравниваем со знаком первого произведения
        vect1 = get_vect(polygon[i - 2], polygon[i - 1])
        vect2 = get_vect(polygon[i - 1], polygon[i])
        su += get_vect_vector_dot(vect1, vect2)
        if sign_rot * get_vect_vector_dot(vect1, vect2) < 0:
            return False
    if su == 0:  # Проверка для вырождения многоугольника в прямую
        return False

    if sign_rot < 0:  # Для нас важно направление векторов сторон для получения внутренних нормалей
        polygon.reverse()

    return True


def make_rotation_clockwise(polygon):
    vect1 = get_vect(polygon[0], polygon[1])
    vect2 = get_vect(polygon[1], polygon[2])
    sign_rot = 1
    if get_vect_vector_dot(vect1,
                           vect2) <= 0:  # Получаем значение знака поворота векторов граней относительно друг друга
        sign_rot = -1
    su = 0
    for i in range(
            len(polygon)):  # Расчитываем знак векторного произведения пары ребер, сравниваем со знаком первого произведения
        vect1 = get_vect(polygon[i - 2], polygon[i - 1])
        vect2 = get_vect(polygon[i - 1], polygon[i])
        su += get_vect_vector_dot(vect1, vect2)

    if sign_rot < 0:  # Для нас важно направление векторов сторон для получения внутренних нормалей
        polygon.reverse()


def get_perpendicular(dot_1, dot_2, pos):
    vect = get_vect(dot_1, dot_2)
    pos_vect = get_vect(dot_2, pos)

    if vect.y() != 0:
        normal = QPointF(1, - vect.x() / vect.y())
    else:
        normal = QPointF(0, 1)

    if get_vect_scalar_dot(pos_vect, normal) < 0:  # Необходмо выбрать такую нормаль чтобы скалярное
        normal.setX(-normal.x())  # Произведение было положительным
        normal.setY(-normal.y())

    return normal


def cyrus_beck_algo(polygon, line):  # Флаг показывает видимость отрезка
    t_down = 0
    t_up = 1

    dot_begin = line[0]
    dot_end = line[1]

    D = dot_end - dot_begin

    for i in range(-2, len(polygon) - 2):  # идем по вершинам n-угольника
        perpendicular = get_perpendicular(polygon[i], polygon[i + 1], polygon[i + 2])  # получаем нормаль

        W = dot_begin - polygon[i]  # Получаеем директриссу

        d_scalar = get_vect_scalar_dot(D, perpendicular)  # Получение скалярных произведений
        w_scalar = get_vect_scalar_dot(W, perpendicular)

        if d_scalar == 0:  # Если D и нормаль перпендикулярны
            if w_scalar < 0:  # То необхрдимо посмотреть на w
                return [False, line]
            else:
                continue

        t = - w_scalar / d_scalar

        if d_scalar > 0:  # Ищем начало видимого отрезка
            if t <= 1:
                t_down = max(t_down, t)
            else:
                return [False, line]

        elif d_scalar < 0:  # Ищем конец видимого отрезка
            if t >= 0:
                t_up = min(t_up, t)
            else:
                return [False, line]

        if t_down > t_up:  # Обрабатываем ситуацию отображения невидимого отрезка
            break

    if t_down <= t_up:
        R1 = dot_begin + D * t_down
        R2 = dot_begin + D * t_up
        return [True, [R1, R2]]  # точки начала/конца видимой части
    return [False, line]


def find_intersections(polygon, lines):
    ans = []
    for i in range(len(lines)):
        ans.append(cyrus_beck_algo(polygon, lines[i]))
    return ans


