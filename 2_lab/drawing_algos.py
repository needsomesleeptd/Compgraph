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


def apply(polygons, func):
    target = polygons[0][0][1]
    for polygon in polygons:
        for dot in polygon:
            target = func(target, dot[1])
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

def rastr_algo_separated(canvas, fill_color, background_color, polygons):
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

        # for i in range(x_inter, x_)
    # left_side
    '''for j in range(min_y, max_y):
        for i in range(canvas.image.width()):
            if (pixel_is_active(canvas, i, j, background_color)):
                if (j < x_splitter):
                    for k in range(j + 1,x_splitter):
                        canvas.image.setPixelColor(i, k, fill_color)
                else:
                    for k in range(x_splitter,j + 1):
                        canvas.image.setPixelColor(i, k, fill_color)'''
