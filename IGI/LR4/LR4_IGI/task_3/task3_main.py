from task_3.calculations import ExpCalculations
import numpy as np

def task3():
    x_values = np.arange(0, 5, 0.1)
    eps = 0.1
    exp_calc = ExpCalculations()
    # print("Введите x:")
    # x = float(input())
    # print("Введите точность:")
    # eps = float(input())
    result = exp_calc.calculate_exp(2, 0.0001)
    print(f"Результат: {result}")
    print(f"Среднее арифметическое: {exp_calc.mean()}")
    print(f"Медиана: {exp_calc.median()}")
    mode = exp_calc.mode()
    if mode is not None:
        print(f"Мода: {mode}")
    print(f"Дисперсия: {exp_calc.variance()}")
    print(f"Стандартное отклонение: {exp_calc.stdev()}")
    exp_calc.plot_approximation_sec(x_values, eps)
    exp_calc.plot(1, 0.1)
    exp_calc.print_table(2, 0.1)
task3()