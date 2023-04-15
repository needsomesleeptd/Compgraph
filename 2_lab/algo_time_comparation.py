from canvas import *
from drawing_algos import *
from matplotlib import pyplot as plt
import time
from PyQt5 import QtCore, QtWidgets, uic
import timeit

from canvas import *


def timingSeedAlgo(canvas, border_colour, fill_colour, seed_point, delay=0, count=10):
    overall_time = 0
    save_q_image = canvas.image.copy()
    for i in range(count):
        canvas.image = save_q_image.copy()
        time_start = timeit.default_timer()
        line_by_line_filling_algorithm_with_seed(canvas, border_colour, fill_colour, seed_point, delay)
        time_end = timeit.default_timer()
        overall_time += time_end - time_start
    canvas.image =   save_q_image.copy()
    return overall_time / count


def timingRastrAlgo(canvas, fill_color, background_color, polygons, count=10):
    overall_time = 0
    save_q_image = canvas.image.copy()
    for i in range(count):
        canvas.image = save_q_image.copy()
        time_start = timeit.default_timer()
        rastr_algo_flag(canvas, fill_color, background_color,
                        polygons)
        time_end = timeit.default_timer()
        overall_time += time_end - time_start
    canvas.image =   save_q_image.copy()
    return overall_time / count


def plot_bars_timing(canvas, border_colour, fill_colour, seed_point, polygons, delay=0, count=10):
    background_colour = QColor(255, 255, 255)  # White color
    time_rastr = timingRastrAlgo(canvas, fill_colour, background_colour, polygons)
    time_seed = timingSeedAlgo(canvas, border_colour, fill_colour, seed_point, delay, count)

    labels = ["1.Алгоритм растрового заполнения", "2.Алгоритм заполнения с затравкой"]
    x = [i + 1 for i in range(2)]

    times = [time_rastr, time_seed]

    for i in range(len(times)):
        plt.bar(x[i], times[i], label=labels[i])

    # plt.bar(x, times,labels = labels)
    plt.xlabel("Выбранный алгоритм")
    plt.ylabel("Затраченное время на построение(ms)")
    plt.title(
        '''Зависимость времени исполнения от выбора Алгоритма и текущих параметров(количество прогонов: {0})'''.format(
            count))
    plt.legend()
    plt.grid()
    plt.show()
