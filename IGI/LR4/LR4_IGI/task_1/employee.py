from datetime import datetime


class Employee:
    employees_dict = {}  # static variable

    def __init__(self, name, vacation_start, vacation_end):
        self.name = name
        self.vacation_start = datetime.strptime(vacation_start, "%d-%m-%Y")
        self.vacation_end = datetime.strptime(vacation_end, "%d-%m-%Y")
        Employee.employees_dict[self.name] = (self.vacation_start, self.vacation_end)
