import math
import statistics
import matplotlib.pyplot as plt
from prettytable import PrettyTable


class ExpCalculations:
    def __init__(self, x, eps):
        self.x = x
        self.eps = eps
        self.sequence = []
        self.exp_value = self.calculate_exp()

    def calculate_exp(self):
        """Вычисляет значение экспоненты в степени х с помощью ряда Тейлора."""
        try:
            n = 0
            term = 1
            sum_of_series = term
            self.sequence.append(term)
            while abs(term) > self.eps and n < 500:
                n += 1
                term *= self.x / n
                sum_of_series += term
                self.sequence.append(sum_of_series)
            return sum_of_series
        except OverflowError:
            print("Ошибка: введенные значения слишком большие.")

    def mean(self):
        """Среднее значение последовательности."""
        return statistics.mean(self.sequence)

    def median(self):
        """Медиана последовательности."""
        return statistics.median(self.sequence)

    def mode(self):
        """Мода последовательности."""
        try:
            return statistics.mode(self.sequence)
        except statistics.StatisticsError:
            print("Ошибка: все значения уникальны, моды не существует.")
            return None

    def variance(self):
        """Дисперсия последовательности."""
        return statistics.variance(self.sequence)

    def stdev(self):
        """Стандартное отклонение последовательности."""
        return statistics.stdev(self.sequence)

    def plot(self):
        # Создаем новую фигуру
        plt.figure()

        # Рисуем график разложения функции в ряд
        plt.plot(range(len(self.sequence)), self.sequence, label='Разложение в ряд')

        # Рисуем график функции, вычисленной с помощью модуля math
        plt.plot(range(len(self.sequence)), [math.exp(self.x)] * len(self.sequence), label='Функция math.exp')

        # Добавляем легенду
        plt.legend()

        # Добавляем названия осей
        plt.xlabel('n')
        plt.ylabel('F(x)')

        # Сохраняем график в файл
        plt.savefig('graph.png')

        # Отображаем график
        plt.show()

    def print_table(self):
        # Создаем объект PrettyTable
        table = PrettyTable()

        # Добавляем заголовки столбцов
        table.field_names = ["x", "F(x)", "n", "Math F(x)", "eps"]

        # Добавляем строки в таблицу
        for i in range(len(self.sequence)):
            table.add_row([self.x, self.sequence[i], i, math.exp(self.x), self.eps])

        # Выводим таблицу
        print(table)
