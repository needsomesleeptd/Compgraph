from drawing_algorithms import *
from canvas import *
from controller import *
from matplotlib import pyplot as plt
import time
from PyQt5 import QtCore, QtWidgets, uic
import timeit


def timing(f):
    def wrap(spectre_line_len, dots, min_angle):
        spectre_coords = get_spectre_coords(spectre_line_len, dots, min_angle)
        time = timeit.timeit(stmt=lambda: getSpectreDots(spectre_coords, f), number=10)
        return time / 10

    return wrap


def timing_default_function(spectre_line_len, dots, min_angle, canvas):
    spectre_coords = get_spectre_coords(spectre_line_len, dots, min_angle)
    time_1 = timeit.default_timer()
    for i in range(len(spectre_coords)):
        canvas.addLine(*spectre_coords[i][0], *spectre_coords[i][1])
    time_2 = timeit.default_timer()
    return (time_2 - time_1)


def plot_bars_timing(spectre_line_len=100, dots=[0, 0], min_angle=12):
    time_BrezFloat = timing(bresenhamAlogorithmFloat)
    time_brez_float = time_BrezFloat(spectre_line_len, dots, min_angle)

    time_BrezInt = timing(bresenhamAlogorithmInt)
    time_brez_int = time_BrezInt(spectre_line_len, dots, min_angle)

    time_BrezSmooth = timing(bresenhamAlogorithmSmooth)
    time_brez_smooth = time_BrezSmooth(spectre_line_len, dots, min_angle)

    time_CDA = timing(CDA)
    time_cda = time_CDA(spectre_line_len, dots, min_angle)

    time_VU = timing(VU)
    time_vu = time_VU(spectre_line_len, dots, min_angle)
    fake_scene = QtWidgets.QGraphicsScene()
    time_lib = timing_default_function(spectre_line_len, dots, min_angle,fake_scene)

    labels = ["1.Алгоритм Брезенхема с дробными числами", "2.Алгоритм Брезенхема с целыми числами",
              "3.Алгоритм Брезенхема со сглаживаем", "4.Алгоритм ЦДА", "5.Алгоритм Ву", "6.Стадартная библиотека"]
    x = [i + 1 for i in range(6)]

    times = [time_brez_float, time_brez_int, time_brez_smooth, time_cda, time_vu, time_lib]

    for i in range(len(times)):
        plt.bar(x[i], times[i], label=labels[i])

    # plt.bar(x, times,labels = labels)
    plt.xlabel("Выбранный алгоритм")
    plt.ylabel("Затраченное время на построение(ms)")
    plt.legend()
    plt.grid()
    plt.show()
