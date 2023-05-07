import time

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

    for i in range(-2, len(polygon) - 2): # идем по вершинам n-угольника
        perpendicular = get_perpendicular(polygon[i], polygon[i + 1], polygon[i + 2]) #получаем нормаль

        W = dot_begin - polygon[i] #Получаеем директриссу

        d_scalar = get_vect_scalar_dot(D, perpendicular) #Получение скалярных произведений
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
        return [True, [R1, R2]] # точки начала/конца видимой части
    return [False, line]


def find_intersections(polygon, lines):
    ans = []
    for i in range(len(lines)):
        ans.append(cyrus_beck_algo(polygon, lines[i]))
    return ans
