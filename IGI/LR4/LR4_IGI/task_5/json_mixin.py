import json
from task_4.figure_color import FigureColor


class JsonSerializable:
    def to_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__ if isinstance(o, FigureColor) else str(o))