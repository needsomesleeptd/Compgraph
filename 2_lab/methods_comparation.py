from algos_ellipses import *
from canvas import *
from controller import *
from matplotlib import pyplot as plt
import time
from PyQt5 import QtCore, QtWidgets, uic
import timeit


def timingCircles(f, dots=[0, 0], R=10, spectreStep=10, spectreLen=100, count=10):
    fake_method = None
    fake_canvas = None
    req = request(dots, fake_method, fake_canvas)
    req.setR(R)
    req.setSpectreParams(spectreStep, spectreLen)
    timings = []
    for j in range(spectreLen):
        sum = 0
        for i in range(count):
            time_start = timeit.default_timer()
            values = f(*req.dots, req.R)
            time_end = timeit.default_timer()
            sum += time_end - time_start

        timings.append(sum / count)
        req.R += spectreStep
    return timings


def timingEllipses(f, dots=[0, 0], A=10, B=10, spectreStep=10, spectreLen=100, count=10):
    fake_method = None
    fake_canvas = None
    req = request(dots, fake_method, fake_canvas)
    req.setEllipseDim(A, B)
    req.setSpectreParams(spectreStep, spectreLen)
    timings = []
    for j in range(spectreLen):
        sum = 0
        for i in range(count):
            time_start = timeit.default_timer()
            values = f(*req.dots, req.A_ellipse, req.B_ellipse)
            time_end = timeit.default_timer()
            sum += time_end - time_start

        timings.append(sum / count)
        req.A_ellipse += spectreStep
        req.B_ellipse += spectreStep
    return timings


def timingEllipsesDefault(dots=[0, 0], A=10, B=32, spectreStep=10, spectreLen=100, count=1):
    fake_scene = QtWidgets.QGraphicsScene()
    fake_method = None
    fake_canvas = None
    req = request(dots, fake_method, fake_canvas)
    req.setEllipseDim(A, B)
    req.setSpectreParams(spectreStep, spectreLen)
    timings = []
    for j in range(spectreLen):
        sum = 0
        for i in range(count):
            time_start = timeit.default_timer()
            fake_scene.addEllipse(*dots, req.A_ellipse, req.B_ellipse)
            time_end = timeit.default_timer()
            sum += time_end - time_start

        timings.append(sum / count)
        req.A_ellipse += spectreStep
        req.B_ellipse += spectreStep

    return timings


def plot_graphs_timing(dots=[0, 0], R=10, spectre_step=10, spectreLen=10, count=10):
    fig, (axs) = plt.subplots(1, 2)
    fig.set_size_inches((30, 8))
    timeBrezCircles = timingCircles(bresenhamCircle, dots, R, spectre_step, spectreLen, count)
    timeMidCircles = timingCircles(midpointCircle, dots, R, spectre_step, spectreLen, count)
    timeCanonicalCircles = timingCircles(cannonicalCircle, dots, R, spectre_step, spectreLen, count)
    timeParametricCircles = timingCircles(parametricCircle, dots, R, spectre_step, spectreLen, count)
    timeDefaultCircles = timingEllipsesDefault(dots, R, R, spectre_step, spectreLen, count)

    timeBrezEllipses = timingEllipses(bresenhamEllipse, dots, R, R, spectre_step, spectreLen, count)
    timeMidEllipses = timingEllipses(midpointEllipse, dots, R, R, spectre_step, spectreLen, count)
    timeCanonicalEllipses = timingEllipses(cannonicalEllipse, dots, R, R, spectre_step, spectreLen, count)
    timeParametricEllipses = timingEllipses(parameterEllipse, dots, R, R, spectre_step, spectreLen, count)
    timeDefaultEllipses = timingEllipsesDefault(dots, R, R, spectre_step, spectreLen, count)

    labels = ["1.Алгоритм Брезенхема", "2.Алгоритм средней точки",
              "3.Использование параметрического уравнения", "4.Использование канонического уравнения",
              "5.Использование библиотеки"]
    x = [R * i for i in range(1, spectreLen + 1)]

    timesCircles = [timeBrezCircles, timeMidCircles,  timeParametricCircles,timeCanonicalCircles, timeDefaultCircles]
    timesEllipses = [timeBrezEllipses, timeMidEllipses, timeParametricEllipses,timeCanonicalEllipses,
                     timeDefaultEllipses]

    for i in range(len(timesCircles)):
        axs[0].plot(x, timesCircles[i], label=labels[i])
    for i in range(len(timesCircles)):
        axs[1].plot(x, timesEllipses[i], label=labels[i])

    titleCircles ='''
        Зависимость времени построения окружности от выбора алгоритма\n(Количество прогонок:{0})
    '''.format(count)
    titleEllipse = '''
     Зависимость времени построения эллипса от выбора алгоритма\n(Количество прогонок:{0})
    '''.format(count)
    axs[0].set_title(titleCircles)
    axs[1].set_title(titleEllipse)
    for ax in axs.flat:
        ax.legend()
        ax.grid()
        ax.set_xlabel("Радиус фигуры")
        ax.set_ylabel("Время затраченное на вычисление(ms)")
    fig.show()


# ______________________________STEPS_COMPARATION_________________________________________________


def plot_graph_steps(spectre_line_len=100, min_angle=12):
    steps = [[], [], [], [], []]

    '''angles = [i for i in range(0, 360, min_angle)]
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

    
    plt.xlabel("Угол поворота прямой")
    plt.ylabel("Количество ступеней")
    plt.legend()
    plt.grid()
    plt.show()'''
