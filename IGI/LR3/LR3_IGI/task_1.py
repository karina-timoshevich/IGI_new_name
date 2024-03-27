# exp_calculator.py
import math
import check_input


def time_func_dec(func):
    import time

    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print('Время выполнения функции: {} секунд.'.format(end - start))

    return wrapper


def calculate_exp(x, eps):
    """Вычисляет значение экспоненты в степени х с помощью ряда Тейлора."""

    try:
        n = 0
        term = 1
        sum_of_series = term
        print(f"| {'x':^10} | {'n':^10} | {'F(x)':^20} | {'Math F(x)':^20} | {'eps':^10} |")
        while abs(term) > eps and n < 500:
            n += 1
            term *= x / n
            sum_of_series += term
            print(f"| {x:^10.2f} | {n:^10} | {sum_of_series:^20.10f} | {math.exp(x):^20.10f} | {eps:^10.2e} |")
        return sum_of_series
    except OverflowError:
        print("Ошибка: введенные значения слишком большие.")


@time_func_dec
def task1():
    """Главная функция для задания 1, которая объединяет все остальные функции."""

    print("Задание №1. Вычисление экспоненты с помощью ряда Тейлора.")
    print("Введите значение x:")
    x = check_input.input_float()
    print("Введите точность вычислений eps:")
    eps = check_input.input_positive_float()
    return calculate_exp(x, eps)
