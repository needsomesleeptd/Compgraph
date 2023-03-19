from canvas import *
from drawing_algorithms import *
class request:
    def __init__(self,dots,request_type,canvas:Canvas):
        self.dots = dots
        self.request_type = request_type
        self.canvas = canvas



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
