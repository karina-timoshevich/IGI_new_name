import math
import statistics
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


class ExpCalculations:
    def __init__(self):
        self.sequence = []

    def calculate_exp(self, x, eps):
        """Вычисляет значение экспоненты в степени х с помощью ряда Тейлора."""
        self.sequence = []
        try:
            n = 0
            term = 1
            sum_of_series = term
            self.sequence.append(term)
            while abs(term) > eps and n < 500:
                n += 1
                term *= x / n
                sum_of_series += term
                self.sequence.append(sum_of_series)
            return sum_of_series
        except OverflowError:
            print("Ошибка: введенные значения слишком большие.")
            return None

    def mean(self):
        """Среднее значение последовательности."""
        if not self.sequence:
            print("Ошибка: метод calculate_exp() еще не был вызван.")
            return None
        return statistics.mean(self.sequence)

    def median(self):
        """Медиана последовательности."""
        if not self.sequence:
            print("Ошибка: метод calculate_exp() еще не был вызван.")
            return None
        return statistics.median(self.sequence)

    def mode(self):
        """Мода последовательности."""
        if not self.sequence:
            print("Ошибка: метод calculate_exp() еще не был вызван.")
            return None
        try:
            return statistics.mode(self.sequence)
        except statistics.StatisticsError:
            print("Ошибка: все значения уникальны, моды не существует.")
            return None

    def variance(self):
        """Дисперсия последовательности."""
        if not self.sequence:
            print("Ошибка: метод calculate_exp() еще не был вызван.")
            return None
        return statistics.variance(self.sequence)

    def stdev(self):
        """Стандартное отклонение последовательности."""
        if not self.sequence:
            print("Ошибка: метод calculate_exp() еще не был вызван.")
            return None
        return statistics.stdev(self.sequence)

    def plot(self, x, eps):
        """Рисует график последовательности и функции math.exp."""
        self.calculate_exp(x, eps)
        plt.figure()
        plt.plot(range(len(self.sequence)), self.sequence, label='Разложение в ряд')

        # с помощью модуля math
        plt.plot(range(len(self.sequence)), [math.exp(x)] * len(self.sequence), label='Функция math.exp')

        plt.legend()
        # названия осей
        plt.xlabel('n')
        plt.ylabel('F(x)')

        plt.savefig('graph.png')
        plt.show()

    def print_table(self, x, eps):
        self.calculate_exp(x, eps)
        table = PrettyTable()
        table.field_names = ["x", "F(x)", "n", "Math F(x)", "eps"]
        # строки в таблицу
        for i in range(len(self.sequence)):
            table.add_row([x, self.sequence[i], i, math.exp(x), eps])

        print(table)

    def plot_approximation(self, x_values, eps):
        plt.figure()
        exp_values_calculated = []
        for x in x_values:
            exp_values_calculated.append(self.calculate_exp(x, eps))

        exp_values_numpy = np.exp(x_values)

        plt.plot(x_values, exp_values_calculated, label='Разложение в ряд')
        plt.plot(x_values, exp_values_numpy, label='Функция numpy.exp')
        plt.legend()

        # названия осей
        plt.xlabel('x')
        plt.ylabel('F(x)')

        plt.savefig('approximation_graph.png')
        plt.show()

    def plot_approximation_sec(self, x_values, eps):
        plt.figure()
        exp_values_calculated = []
        for x in x_values:
            exp_values_calculated.append(self.calculate_exp(x, eps))

        exp_values_numpy = np.exp(x_values)
        plt.plot(x_values, np.array(exp_values_calculated) + 1.5, label='Разложение в ряд')
        plt.plot(x_values, exp_values_numpy, label='Функция numpy.exp')

        plt.legend()

        # названия осей
        plt.xlabel('x')
        plt.ylabel('F(x)')

        plt.savefig('approximation_graph.png')
        plt.show()
