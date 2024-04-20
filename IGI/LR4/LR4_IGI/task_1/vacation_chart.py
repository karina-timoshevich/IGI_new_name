import csv
import pickle
from datetime import datetime
from task_1.employee import Employee
from task_1.files_service import save_to_csv, load_from_csv, save_to_pickle, load_from_pickle


class VacationChart:
    def __init__(self):
        self._employees = Employee.employees_dict

    @property
    def employees(self):
        return self._employees

    @employees.setter
    def employees(self, value):
        self._employees = value

    def save_to_csv(self, filename):
        save_to_csv(self.employees, filename)

    def load_from_csv(self, filename):
        self.employees = load_from_csv(filename)

    def save_to_pickle(self, filename):
        save_to_pickle(self.employees, filename)

    def load_from_pickle(self, filename):
        self.employees = load_from_pickle(filename)

    def find_employee(self, name):
        return self.employees.get(name, None)

    def sort_by_vacation_start(self):
        return sorted(self.employees.items(), key=lambda x: x[1][0])

    def vacation_statistics(self):
        statistics = [0]*12
        for dates in self.employees.values():
            for month in range(dates[0].month, dates[1].month + 1):
                statistics[month - 1] += 1
        total = len(self.employees)
        for i in range(12):
            statistics[i] = (statistics[i], statistics[i] / total * 100)
        return statistics

