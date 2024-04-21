import math
from task_4.geometric_figure import GeometricFigure
from task_4.figure_color import FigureColor
from task_5.json_mixin import JsonSerializable
import numpy as np


class Triangle(GeometricFigure, JsonSerializable):
    figure_type = "Triangle"

    def __init__(self, a, b, C, color):
        self.a = a
        self.b = b
        self.C = math.radians(C)
        self.color = FigureColor(color)

    def print_details_json(self):
        print(self.to_json())
    def calculate_area(self):
        return 0.5 * self.a * self.b * math.sin(self.C)

    def calculate_c(self):
        return np.sqrt(self.a ** 2 + self.b ** 2 - 2 * self.a * self.b * np.cos(self.C))

    def __str__(self):
        return "Figure: {0}\nColor: {1}\nSides: {2}, {3}, {4} \nAngle: {5}\nArea: {6}".format(
            self.figure_type,
            self.color._color,
            self.a,
            self.b,
            self.calculate_c(),
            math.degrees(self.C),
            self.calculate_area()
        )