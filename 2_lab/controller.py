from canvas import *
from algos_ellipses import *
from algos_circles import *


def getSpectreDots(spectreDots, method, stepmode=False):
    allLines = []
    for line in spectreDots:
        allLines.append(method(*line[0], *line[1], stepmode=stepmode))
    return allLines


class request:
    def __init__(self, dots: list, request_type, canvas: Canvas):
        self.dots = dots
        self.request_type = request_type
        self.canvas = canvas
        self.A_ellipse = 10
        self.B_ellipse = 10
        self.R = 10
        self.spectreStep = 100
        self.spectreLen = 10

    def setEllipseDim(self, A,B):
        self.A_ellipse = A
        self.B_ellipse = B
    def setR(self,R):
        self.R = R

    def setSpectreParams(self, spectreStep,spectreLen):
        self.spectreStep = spectreStep
        self.spectreLen = spectreLen


def recursive_len(item):
    if type(item) == list or type(item) == QPolygonF:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def handle_request(req: request):

    if (req.request_type == "midPointEllipse"):
        all_lines = midpointEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "canonicEllipse"):

        all_lines = cannonicalEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "standardEllipse"):

        len_obj = req.canvas.drawEllipseStandard(*req.dots, req.B_ellipse, req.A_ellipse)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "parametricEllipse"):
        all_lines = parameterEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "brezEllipse"):
        all_lines = bresenhamEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    #here cicrcles start
    elif (req.request_type == "midPointCircle"):
        all_lines = midpointCircle(*req.dots, req.R)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "canonicCircle"):

        all_lines = cannonicalCircle(*req.dots,  req.R)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "standardCircle"):

        len_obj = req.canvas.drawCircleStandard(*req.dots,  req.R)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "parametricCircle"):
        all_lines = parametricCircle(*req.dots,  req.R)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "brezCircle"):
        all_lines = bresenhamCircle(*req.dots,  req.R)
        len_obj = req.canvas.drawLineByPoints(all_lines)



