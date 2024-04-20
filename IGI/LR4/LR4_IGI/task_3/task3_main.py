from task_3.calculations import ExpCalculations


def task3():
    # Создаем экземпляр класса ExpCalculations
    exp_calc = ExpCalculations(1, 0.0001)

    # Вызываем методы и выводим результаты
    print(f"Среднее арифметическое: {exp_calc.mean()}")
    print(f"Медиана: {exp_calc.median()}")
    mode = exp_calc.mode()
    if mode is not None:
        print(f"Мода: {mode}")
    print(f"Дисперсия: {exp_calc.variance()}")
    print(f"Стандартное отклонение: {exp_calc.stdev()}")
    print(f"Значение функции: {exp_calc.exp_value}")
    # Строим графики
    exp_calc.plot()
    exp_calc.print_table()
task3()