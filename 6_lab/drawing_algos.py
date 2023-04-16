import time

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QPolygonF, QColor
import numpy as np
from PyQt5 import QtTest

from math import *


def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    else:
        return -1


def CDA(x1: float, y1: float, x2: float, y2: float, stepmode=False):
    x2 = ceil(x2)
    y2 = ceil(y2)
    x1 = floor(x1)
    y1 = floor(y1)
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
        for i in range(0, round(length) + 1):

            if not stepmode:
                pointsList.append((QPoint(x, y)))
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1

            x += dx
            y += dy
    if stepmode:
        return steps
    return pointsList


def get_pixel_color(canvas, x, y):
    return QColor(canvas.image.pixel(x, y))


def check_line(canvas, stack, cur_pixel, xr, fill_colour, border_colour, dy):
    x = cur_pixel[0]
    y = cur_pixel[1]
    y = y + dy
    while x <= xr:
        flag = False  # Флаг показыващий что мы нашли пиксель для добавления в стэк

        while get_pixel_color(canvas, x, y) != fill_colour and \
                get_pixel_color(canvas, x,
                                y) != border_colour and x <= xr:  # Идем пока наш интервал незакрашенных пикселей не прерван
            flag = True
            x += 1

        # Помещаем в стек крайний справа пиксель

        if flag:  # Нашли правый незакрашенный пиксель
            if x == xr and get_pixel_color(canvas, x, y) != fill_colour and \
                    get_pixel_color(canvas, x, y) != border_colour:
                if y < canvas.image.height():  # Если и есть наш пиксель (самый правый то берем его)
                    stack.append([x, y])
            else:
                if y < canvas.image.height():
                    stack.append([x - 1, y])  # Иначе берем пиксель левее его(наш флаг говорит о том что он точно есть)

            flag = False

        # Продолжаем проверку, если интервал был прерван

        x_in = x
        while (get_pixel_color(canvas, x, y) == fill_colour or
               get_pixel_color(canvas, x, y) == border_colour) and x < xr:  # Идем направо по пикселям которые
            x = x + 1  # Прерывают незакрашенные

        if x == x_in:  # Проверяем что координата пикселя точно увеличена
            x += 1


def line_by_line_filling_algorithm_with_seed(canvas, border_colour, fill_colour, seed_point, delay=0):
    stack = [seed_point]
    while stack:

        seed_pixel = stack.pop()
        x = seed_pixel[0]
        y = seed_pixel[1]

        canvas.image.setPixelColor(x, y, fill_colour)
        save_x = x
        save_y = y

        # Заполняем интервал справа от затравки
        x += 1

        while get_pixel_color(canvas, x, y) != fill_colour and \
                get_pixel_color(canvas, x, y) != border_colour and x < canvas.image.width():
            canvas.image.setPixelColor(x, y, fill_colour)
            x += 1

        xr = x - 1

        # Заполняем интервал слева от затравки

        x = save_x - 1
        while get_pixel_color(canvas, x, y) != fill_colour and \
                get_pixel_color(canvas, x, y) != border_colour and x > 0:
            canvas.image.setPixelColor(x, y, fill_colour)
            x -= 1

        xl = x + 1

        if save_y < canvas.image.height():
            check_line(canvas, stack, [xl, save_y], xr, fill_colour, border_colour,
                       1)  # Проходим по строке снизу y = y +1
        if (save_y > 0):
            check_line(canvas, stack, [xl, save_y], xr, fill_colour, border_colour,
                       -1)  # Проходим по строке сверху y = y - 1

        if delay != 0:
            QtTest.QTest.qWait(delay)
            canvas.updatePixmap()


def x_mass(polygons):
    su = 0
    count = 0
    for polygon in polygons:
        for dot in polygon:
            count += 1
            su += dot[0]
    if (count == 0):
        return 0
    return su / count


def pixel_is_active(canvas, x, y, background_color):
    if (background_color == get_pixel_color(canvas, x, y)):
        return 0
    else:
        return 1


def apply_to_dots(polygons, func):
    if (len(polygons) == 0):
        return None
    target = polygons[0][0][1]
    for polygon in polygons:
        for dot in polygon:
            target = func(target, dot)
    return target


def get_intersections(polygons):
    intersections = []

    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            x1 = polygons[i][j][0]
            y1 = polygons[i][j][1]
            x2 = polygons[i][(j + 1) % len(polygons[i])][0]
            y2 = polygons[i][(j + 1) % len(polygons[i])][1]

            len_x = abs(int(x2) - int(x1))
            len_y = abs(int(y2) - int(y1))

            if len_y != 0:
                dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
                dy = (y2 > y1) - (y2 < y1)

                x1 += dx / 2
                y1 += dy / 2

            for k in range(len_y):
                intersections.append([x1, y1])
                x1 += dx
                y1 += dy

    return intersections


def revert_color(start_color, end_color, cur_color):
    if (cur_color != start_color):
        return start_color
    else:
        return end_color


# Алгоритм для закрашивания с перегородкой
'''def rastr_algo_splitter(canvas, fill_color, background_color, polygons):
    x_splitter = int(x_mass(polygons))
    # min_y = int(apply_to_dots(polygons, lambda tar, dots: min(tar, dots[1])))
    # max_y = ceil(apply_to_dots(polygons, lambda tar, dots: max(tar, dots[1])))
    # intersactions = get_intersections(polygons)
    # print([[intersaction[0], intersaction[1]] for intersaction in intersactions])
    # print(x_splitter)
    check_color = rastr_algo_flag_preproc(canvas, canvas.pen.color(), polygons)
    intersections = get_intersections(polygons)
    cur_fill_color = fill_color
    for intersaction in intersections:
        x_inter = int(intersaction[0])
        y_inter = round(intersaction[1] + 1 / 2)

        if (x_inter <= x_splitter):

            for k in range(x_inter + 1, x_splitter):
                cur_color = get_pixel_color(canvas, x_inter, y_inter)
                cur_fill_color = revert_color(fill_color, background_color, cur_color)

                canvas.image.setPixelColor(k, y_inter, cur_fill_color)
        else:
            for k in range(x_splitter, x_inter):
                cur_color = get_pixel_color(canvas, x_inter, y_inter)

                cur_fill_color = revert_color(fill_color, background_color, cur_color)

                canvas.image.setPixelColor(k, y_inter, cur_fill_color)

'''
def get_color_flags(border_color):
    r = border_color.red()
    g = border_color.blue()
    b = border_color.green()
    r_new = r + 1 if r < 255 else r - 1
    g_new = g + 1 if g < 255 else g - 1
    b_new = b + 1 if b < 255 else b - 1
    return QColor(r_new, g_new, b_new)


# def restore_polygons(canvas):

def rastr_algo_flag_preproc(canvas, border_color, polygons):
    color_change = get_color_flags(border_color)
    intersections = get_intersections(polygons)
    for intersection in intersections:
        x = intersection[0]
        y = intersection[1]
        if (get_pixel_color(canvas, round(x + 1 / 2), round(y)) == color_change):
            canvas.image.setPixelColor(round(x + 1 / 2) - 1, round(y), color_change)
        else:
            canvas.image.setPixelColor(round(x + 1 / 2), round(y), color_change)

    return color_change


def rastr_algo_flag(canvas, fill_color, background_color, polygons):
    if (len(polygons) == 0):
        min_y = 0
        min_x = 0
        max_x = canvas.image.width()
        max_y = canvas.image.height()
    else:
        min_y = int(apply_to_dots(polygons, lambda tar, dots: min(tar, dots[1])))
        max_y = ceil(apply_to_dots(polygons, lambda tar, dots: max(tar, dots[1])))

        min_x = int(apply_to_dots(polygons, lambda tar, dots: min(tar, dots[0])))
        max_x = ceil(apply_to_dots(polygons, lambda tar, dots: max(tar, dots[0])))

    check_color = rastr_algo_flag_preproc(canvas, canvas.pen.color(), polygons)
    for y in range(min_y + 1, max_y):
        flag = False
        x = min_x + 1
        while x < max_x:

            if (get_pixel_color(canvas, x, y) == check_color):
                flag = not flag
            #while (get_pixel_color(canvas, x, y) == check_color):
            #    x += 1

            if flag:
                canvas.image.setPixelColor(x, y, fill_color)
            else:
                canvas.image.setPixelColor(x, y, background_color)
            x += 1


