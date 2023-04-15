import time

from PyQt5.QtCore import QPoint
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
                pointsList.append((QPoint(round(x), round(y))))
            elif round(x + dx) != round(x) and round(y + dy) != round(y):
                steps += 1

            x += dx
            y += dy
    if stepmode:
        return steps
    return pointsList


def get_pixel_color(canvas, x, y):
    return QColor(canvas.image.pixel(x, y))


def line_by_line_filling_algorithm_with_seed(canvas, border_colour, fill_colour, seed_point, delay=0):
    stack = [seed_point]
    while stack:

        seed_pixel = stack.pop()
        x = seed_pixel[0]
        y = seed_pixel[1]

        canvas.image.setPixelColor(x, y, fill_colour)
        tx = x
        ty = y

        # заполняем интервал справа от затравки

        x += 1

        while get_pixel_color(canvas, x, y) != fill_colour and \
                get_pixel_color(canvas, x, y) != border_colour and x < canvas.image.width():
            canvas.image.setPixelColor(x, y, fill_colour)
            x += 1
        # print(get_pixel_color(canvas,x,y).Rgb ,fill_colour.Rgb)

        xr = x - 1

        # заполняем интервал слева от затравки

        x = tx - 1
        while get_pixel_color(canvas, x, y) != fill_colour and \
                get_pixel_color(canvas, x, y) != border_colour and x > 0:
            canvas.image.setPixelColor(x, y, fill_colour)
            x -= 1

        xl = x + 1

        # Проход по верхней строке

        x = xl
        if ty < canvas.image.height():
            y = ty + 1

            while x <= xr:
                flag = False

                while get_pixel_color(canvas, x, y) != fill_colour and \
                        get_pixel_color(canvas, x, y) != border_colour and x <= xr:
                    flag = True
                    x += 1

                # Помещаем в стек крайний справа пиксель

                if flag:
                    if x == xr and get_pixel_color(canvas, x, y) != fill_colour and \
                            get_pixel_color(canvas, x, y) != border_colour:
                        if y < canvas.image.height():
                            stack.append([x, y])
                    else:
                        if y < canvas.image.height():
                            stack.append([x - 1, y])

                    flag = False

                # Продолжаем проверку, если интервал был прерван

                x_in = x
                while (get_pixel_color(canvas, x, y) == fill_colour or
                       get_pixel_color(canvas, x, y) == border_colour) and x < xr:
                    x = x + 1

                if x == x_in:
                    x += 1

        # Проход по нижней строке

        x = xl
        y = ty - 1

        while x <= xr:
            flag = False

            while get_pixel_color(canvas, x, y) != fill_colour and \
                    get_pixel_color(canvas, x, y) != border_colour and x <= xr:
                flag = True
                x += 1

            # Помещаем в стек крайний справа пиксель

            if flag:

                if x == xr and get_pixel_color(canvas, x, y) != fill_colour and \
                        get_pixel_color(canvas, x, y) != border_colour:
                    if y > 0:
                        stack.append([x, y])
                else:
                    if y > 0:
                        stack.append([x - 1, y])

                flag = False

            # Продолжаем проверку, если интервал был прерван

            x_in = x
            while (get_pixel_color(canvas, x, y) == fill_colour or
                   get_pixel_color(canvas, x, y) == border_colour) and x < xr:
                x = x + 1

            if x == x_in:
                x += 1

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


def get_intersections(edges):
    intersections = []

    for i in range(len(edges)):
        for j in range(len(edges[i])):
            x1 = edges[i][j][0]
            y1 = edges[i][j][1]
            x2 = edges[i][(j + 1) % len(edges[i])][0]
            y2 = edges[i][(j + 1) % len(edges[i])][1]

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


# Алгоритм для закрашивания с перегородкой
'''def rastr_algo_separated(canvas, fill_color, background_color, polygons):
    x_splitter = int(x_mass(polygons))
    min_y = int(apply(polygons, min))
    max_y = ceil(apply(polygons, max))
    intersactions = get_intersections(polygons)
    #print([[intersaction[0], intersaction[1]] for intersaction in intersactions])
    #print(x_splitter)
    for intersaction in intersactions:
        x_inter = int(intersaction[0])
        y_inter = int(intersaction[1])
        if (x_inter <= x_splitter):
            for k in range(x_inter, x_splitter):
                canvas.image.setPixelColor(k, y_inter, fill_color)
        else:
            for k in range(x_splitter, x_inter + 1):
                canvas.image.setPixelColor(k, y_inter, fill_color)
'''

def rastr_algo_flag(canvas,fill_color, background_color, polygons):
    if (len(polygons) == 0):
        min_y = 0
        min_x = 0
        max_x = canvas.image.width()
        max_y = canvas.image.height()
    else:
        min_y = int(apply_to_dots(polygons, lambda tar,dots:min(tar,dots[1])))
        max_y = ceil(apply_to_dots(polygons, lambda tar,dots:max(tar,dots[1])))

        min_x = int(apply_to_dots(polygons, lambda tar, dots: min(tar, dots[0])))
        max_x = ceil(apply_to_dots(polygons, lambda tar, dots: max(tar, dots[0])))


    for y in range(min_y, max_y):
        flag = False

        for x in range(min_x, max_x + 2):

            if (get_pixel_color(canvas,x, y) == canvas.pen.color()):
                flag = not flag

            if flag:
                canvas.image.setPixelColor(x,y,fill_color)
            else:
                canvas.image.setPixelColor(x, y, background_color)


