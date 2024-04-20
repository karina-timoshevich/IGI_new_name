from task_4.triangle import Triangle


class TriangleWithName(Triangle):
    def __init__(self, a, b, C, color, name):
        super().__init__(a, b, C, color)
        self.name = name

    def print_details(self):
        print(super().__str__())
        print(f"Name: {self.name}")