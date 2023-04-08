from algos_ellipses import *
from canvas import *
from controller import *
from matplotlib import pyplot as plt
import time
from PyQt5 import QtCore, QtWidgets, uic
import timeit


def timing(f):
    def wrap(spectre_line_len, dots, min_angle, count=10):
        sum = 0
        for i in range(count):
            time_start = timeit.default_timer()
            spectre_coords = get_spectre_coords(spectre_line_len, dots, min_angle)
            values = getSpectreDots(spectre_coords, f)
            time_end = timeit.default_timer()
            sum += time_end - time_start

        return sum / count

    return wrap


def timing_default_function(spectre_line_len, dots, min_angle, canvas, count=10):
    spectre_coords = get_spectre_coords(spectre_line_len, dots, min_angle)
    sum = 0
    for i in range(count):
        time_1 = timeit.default_timer()
        for i in range(len(spectre_coords)):
            canvas.addLine(*spectre_coords[i][0], *spectre_coords[i][1])
        time_2 = timeit.default_timer()
        sum += time_2 - time_1

    return sum / count


def plot_bars_timing(spectre_line_len=500, dots=[0, 0], min_angle=12):
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
    time_lib = timing_default_function(spectre_line_len, dots, min_angle, fake_scene)

    labels = ["1.Алгоритм Брезенхема с дробными числами", "2.Алгоритм Брезенхема с целыми числами",
              "3.Алгоритм Брезенхема со сглаживаем", "4.Алгоритм ЦДА", "5.Алгоритм Ву", "6.Стадартная библиотека"]
    x = [i + 1 for i in range(6)]

    times = [time_brez_float, time_brez_int, time_brez_smooth, time_cda, time_vu, time_lib]

    for i in range(len(times)):
        plt.bar(x[i], times[i], label=labels[i])

    # plt.bar(x, times,labels = labels)
    plt.xlabel("Выбранный алгоритм")
    plt.ylabel("Затраченное время на построение(ms)")
    plt.title(
        '''Зависимость времени исполнения от выбора алгоритма
        (Замер производился при вычислении координат и интесивностей точек спектра с длиной прямых:{0} и расстоянием между прямыми в градусах:{1})'''.format(
            spectre_line_len, min_angle))
    plt.legend()
    plt.grid()
    plt.show()


# ______________________________STEPS_COMPARATION_________________________________________________


def plot_graph_steps(spectre_line_len=100, min_angle=12):

    steps = [[], [], [], [], []]

    angles = [i for i in range(0,360, min_angle)]
    spectre_coords = get_spectre_coords(spectre_line_len, [0, 0], min_angle)
    vu_steps = getSpectreDots(spectre_coords, VU, True)
    brez_float_steps = getSpectreDots(spectre_coords, bresenhamAlogorithmFloat, True)
    brez_int_steps = getSpectreDots(spectre_coords, bresenhamAlogorithmInt, True)
    cda_steps = getSpectreDots(spectre_coords, CDA, True)
    brez_smooth_steps = getSpectreDots(spectre_coords, bresenhamAlogorithmSmooth, stepmode=True)

    steps[0].append(brez_float_steps)
    steps[1].append(brez_int_steps)
    steps[2].append(brez_smooth_steps)
    steps[3].append(cda_steps)
    steps[4].append(vu_steps)


    labels = ["Алгоритм Брезенхема с дробными числами", "Алгоритм Брезенхема с целыми числами",
              "Алгоритм Брезенхема со сглаживаем", "Алгоритм ЦДА", "Алгоритм Ву"]
    for i in range(len(labels)):
        plt.plot(angles, *steps[i], label=labels[i])

    plt.title(
        '''Зависимость количества ступеней  от угла под которым идет прямая(длина прямых:{0}, шаг угла:{1})'''.format(spectre_line_len, min_angle))
    plt.xlabel("Угол поворота прямой")
    plt.ylabel("Количество ступеней")
    plt.legend()
    plt.grid()
    plt.show()

