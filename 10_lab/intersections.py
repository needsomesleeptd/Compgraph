import time
import numpy as np

from PyQt5.QtCore import QPoint, QPointF
from drawing_algos import get_rect_points

EPS = 1e-9

from math import *

def f1(x, z):
    return 5 * x + 3 * z - 7


def f2(x, z):
    return x ** 2 + z ** 2


def f3(x, z):
    return sin(x * z)


def f4(x, z):
    return sin(x * z)


def f5(x, z):
    return x ** 2 * z


def f6(x, z):
    return (x * z) ** 2


def f7(x, z):
    return sin(x) * cos(z)


def funcs(ind):
    func_arr = [f1, f2, f3, f4, f5, f6, f7]
    return func_arr[ind]