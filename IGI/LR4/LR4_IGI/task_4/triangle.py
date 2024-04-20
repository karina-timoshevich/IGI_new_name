import math
from geometric_figure import GeometricFigure
from figure_color import FigureColor


class Triangle(GeometricFigure):
    figure_type = "Triangle"

    def __init__(self, a, b, C, color):
        self.a = a
        self.b = b
        self.C = math.radians(C)  # Convert degrees to radians
        self.color = FigureColor(color)

    def calculate_area(self):
        return 0.5 * self.a * self.b * math.sin(self.C)

    def __str__(self):
        return "Figure: {0}\nColor: {1}\nSides: {2}, {3}\nAngle: {4}\nArea: {5}".format(
            self.figure_type,
            self.color._color,
            self.a,
            self.b,
            math.degrees(self.C),
            self.calculate_area()
        )