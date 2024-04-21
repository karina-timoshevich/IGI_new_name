class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def get_color(self):
        return self._color

    def __repr__(self):  # строковое представление объекта
        return self._color
