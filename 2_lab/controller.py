from canvas import *
from drawing_algorithms import *


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

    def setSpectreParams(self, spectreStep,spectreLen):
        self.spectreStep = spectreStep
        self.spectreLen = spectreLen


def recursive_len(item):
    if type(item) == list or type(item) == QPolygonF:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def handle_request(req: request):
    if (req.request_type == "defaultAlgo"):
        len_obj = req.canvas.drawEllipseStandard(*req.dots)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "brezFloat"):
        points = bresenhamAlogorithmFloat(*req.dots)
        len_obj = req.canvas.drawLineByPoints(points)
        req.canvas.figure_items_count.append(len_obj)
    elif (req.request_type == "brezInt"):
        points = bresenhamAlogorithmInt(*req.dots)
        len_obj = req.canvas.drawLineByPoints(points)
        req.canvas.figure_items_count.append(len_obj)
    elif (req.request_type == "brezSmooth"):
        coloredPoints = bresenhamAlogorithmSmooth(*req.dots)
        len_obj = req.canvas.drawLineIntensivityByPoints(coloredPoints)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "CDA"):
        points = CDA(*req.dots)
        len_obj = req.canvas.drawLineByPoints(points)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "Vu"):
        coloredPoints = VU(*req.dots)
        len_obj = req.canvas.drawLineIntensivityByPoints(coloredPoints)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "brezSmoothSpectre"):
        spectre_coords = get_spectre_coords(req.B_ellipse, req.dots, req.A_ellipse)
        all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmSmooth)
        len_obj = req.canvas.drawSpectre(all_lines, req.request_type)
        req.canvas.figure_items_count.append(len_obj)
    elif (req.request_type == "brezIntSpectre"):
        all_lines = midpointEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "brezFloatSpectre"):

        all_lines = cannonicalEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "defaultAlgoSpectre"):

        len_obj = req.canvas.drawEllipseStandard(*req.dots, req.B_ellipse, req.A_ellipse)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "CDASpectre"):
        all_lines = parameterEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "VuSpectre"):
        all_lines = bresenhamEllipse(*req.dots, req.B_ellipse, req.A_ellipse)

        len_obj = req.canvas.drawLineByPoints(all_lines)
