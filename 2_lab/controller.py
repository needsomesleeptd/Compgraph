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
        self.min_angle = 10
        self.spectre_line_len = 100

    def setMinAngle(self, angle):
        self.min_angle = angle

    def setSpectreLen(self, len):
        self.spectre_line_len = len


def recursive_len(item):
    if type(item) == list or type(item) == QPolygonF:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def handle_request(req: request):
    if (req.request_type == "defaultAlgo"):
        len_obj = req.canvas.drawLine(*req.dots)
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
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmSmooth)
        len_obj = req.canvas.drawSpectre(all_lines, req.request_type)
        req.canvas.figure_items_count.append(len_obj)
    elif (req.request_type == "brezIntSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmInt)
        len_obj = req.canvas.drawSpectre(all_lines, req.request_type)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "brezFloatSpectre"):
        # spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        # all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmFloat)
        # len_obj = req.canvas.drawSpectre(all_lines, req.request_type)
        # req.canvas.figure_items_count.append(len_obj)
        all_lines = cannonicalEllipse(*req.dots, req.spectre_line_len, req.min_angle)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "defaultAlgoSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)

        len_obj = req.canvas.drawSpectre(spectre_coords, req.request_type)
        req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "CDASpectre"):
        all_lines = parameterEllipse(*req.dots, req.spectre_line_len, req.min_angle)
        len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "VuSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, VU)
        len_obj = req.canvas.drawSpectre(all_lines, req.request_type)
        req.canvas.figure_items_count.append(len_obj)
