from canvas import *
from algos_ellipses import *
from algos_circles import *


def getSpectrePolygons(spectreRequests, method):
    allLines = []
    if (spectreRequests[0].A_ellipse > 0):
        for req in spectreRequests:
            allLines.append(method(*req.dots, req.B_ellipse, req.A_ellipse))
    else:
        for req in spectreRequests:
            allLines.append(method(*req.dots, req.R))

    return allLines


def getSpectreRequests(init_req, step, count):
    requests = []
    if init_req.R > 0:
        R = init_req.R
        for i in range(int(count)):
            req = request(init_req.dots, init_req.request_type, init_req.canvas)
            req.setR(R)
            requests.append(req)
            R += step
    else:
        A = init_req.A_ellipse
        B = init_req.B_ellipse
        step_A = step[0]
        step_B = step[1]
        for i in range(int(count)):
            req = request(init_req.dots, init_req.request_type, init_req.canvas)
            req.setEllipseDim(A, B)
            requests.append(req)
            A += step_A
            B += step_B

    return requests


class request:
    def __init__(self, dots: list, request_type, canvas: Canvas):
        self.dots = dots
        self.request_type = request_type
        self.canvas = canvas
        self.A_ellipse = -1
        self.B_ellipse = -1
        self.R = -1
        self.spectreStep = 0
        self.spectreLen = 0
        self.ellipseStepA = 0
        self.ellipsestepB = 0

    def setEllipseDim(self, A, B):
        self.A_ellipse = A
        self.B_ellipse = B

    def setR(self, R):
        self.R = R

    def setSpectreParams(self, spectreStep, spectreLen):
        self.spectreStep = spectreStep
        self.spectreLen = spectreLen


def recursive_len(item):
    if type(item) == list or type(item) == QPolygonF:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def handle_request(req: request):
    len_obj = 0
    if (req.request_type == "midPointEllipse"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Ellipses = getSpectrePolygons(requests, midpointEllipse)
            len_obj = req.canvas.drawLinesByPoints(Ellipses)
        else:
            all_lines = midpointCircle(*req.dots, req.R)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "canonicEllipse"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Ellipses = getSpectrePolygons(requests, cannonicalEllipse)
            len_obj = req.canvas.drawLinesByPoints(Ellipses)
        else:
            all_lines = cannonicalEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "standardEllipse"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            len_obj = req.canvas.drawEllipsesStandard(requests)
        else:
            len_obj = req.canvas.drawEllipseStandard(*req.dots, req.B_ellipse, req.A_ellipse)
            req.canvas.figure_items_count.append(len_obj)

    elif (req.request_type == "parametricEllipse"):

        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Ellipses = getSpectrePolygons(requests, parameterEllipse)
            len_obj = req.canvas.drawLinesByPoints(Ellipses)
        else:
            all_lines = parameterEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "brezEllipse"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Ellipses = getSpectrePolygons(requests, bresenhamEllipse)
            len_obj = req.canvas.drawLinesByPoints(Ellipses)
        else:
            all_lines = bresenhamEllipse(*req.dots, req.B_ellipse, req.A_ellipse)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    # here cicrcles start
    elif (req.request_type == "midPointCircle"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Circles = getSpectrePolygons(requests, midpointCircle)
            len_obj = req.canvas.drawLinesByPoints(Circles)
        else:
            all_lines = midpointCircle(*req.dots, req.R)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "canonicCircle"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Circles = getSpectrePolygons(requests, cannonicalCircle)
            len_obj = req.canvas.drawLinesByPoints(Circles)
        else:
            all_lines = cannonicalCircle(*req.dots, req.R)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "standardCircle"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            len_obj = req.canvas.drawCirclesStadard(requests)
        else:
            len_obj = req.canvas.drawCircleStandard(*req.dots, req.R)


    elif (req.request_type == "parametricCircle"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Circles = getSpectrePolygons(requests, parametricCircle)
            len_obj = req.canvas.drawLinesByPoints(Circles)
        else:
            all_lines = parametricCircle(*req.dots, req.R)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    elif (req.request_type == "brezCircle"):
        if (req.spectreLen != 0):
            requests = getSpectreRequests(req, req.spectreStep, req.spectreLen)
            Circles = getSpectrePolygons(requests, bresenhamCircle)
            len_obj = req.canvas.drawLinesByPoints(Circles)
        else:
            all_lines = bresenhamCircle(*req.dots, req.R)
            len_obj = req.canvas.drawLineByPoints(all_lines)

    req.canvas.figure_items_count.append(len_obj)
