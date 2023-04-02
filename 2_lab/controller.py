from canvas import *
from drawing_algorithms import *


def getSpectreDots(spectreDots, method):
    allLines = []
    for line in spectreDots:
       allLines.append(method(*line[0], *line[1]))
    return allLines


class request:
    def __init__(self,dots:list,request_type,canvas:Canvas):
        self.dots = dots
        self.request_type = request_type
        self.canvas = canvas
        self.min_angle = 10
        self.spectre_line_len = 100

    def setMinAngle(self,angle):
        self.min_angle = angle
    def setSpectreLen(self,len):
        self.spectre_line_len = len




def handle_request(req:request):
    if (req.request_type == "defaultAlgo"):
        req.canvas.drawLine(*req.dots)
    elif (req.request_type == "brezFloat"):
        points = bresenhamAlogorithmFloat(*req.dots)
        req.canvas.drawLineByPoints(points)
    elif (req.request_type == "brezInt"):
        points = bresenhamAlogorithmInt(*req.dots)
        req.canvas.drawLineByPoints(points)
    elif (req.request_type == "brezSmooth"):
        coloredPoints = bresenhamAlogorithmSmooth(*req.dots)
        req.canvas.drawLineIntensivityByPoints(coloredPoints)

    elif (req.request_type == "CDA"):
        points = CDA(*req.dots)
        req.canvas.drawLineByPoints(points)
    elif (req.request_type == "Vu"):
        coloredPoints = VU(*req.dots)
        req.canvas.drawLineIntensivityByPoints(coloredPoints)

    elif (req.request_type== "brezSmoothSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmSmooth)
        req.canvas.drawSpectre(all_lines,req.request_type)
    elif (req.request_type == "brezIntSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, bresenhamAlogorithmInt)
        req.canvas.drawSpectre(all_lines,req.request_type)

    elif (req.request_type == "brezFloatSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords,bresenhamAlogorithmFloat)
        req.canvas.drawSpectre(all_lines,req.request_type)

    elif (req.request_type == "defaultAlgoSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        req.canvas.drawSpectre(spectre_coords, req.request_type)

    elif (req.request_type == "CDASpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, CDA)
        req.canvas.drawSpectre(all_lines, req.request_type)

    elif (req.request_type == "VuSpectre"):
        spectre_coords = get_spectre_coords(req.spectre_line_len, req.dots, req.min_angle)
        all_lines = getSpectreDots(spectre_coords, VU)
        req.canvas.drawSpectre(all_lines, req.request_type)







