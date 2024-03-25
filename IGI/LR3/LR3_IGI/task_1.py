# exp_calculator.py
import math
import check_input


def calculate_exp():
    """Вычисляет значение экспоненты в степени х с помощью ряда Тейлора."""

    print("Введите значение x:")
    x = check_input.input_float()
    print("Введите точность вычислений eps:")
    eps = check_input.input_positive_float()
    n = 0
    term = 1
    sum = term
    print(f"| {'x':^10} | {'n':^10} | {'F(x)':^20} | {'Math F(x)':^20} | {'eps':^10} |")
    while abs(term) > eps and n < 500:
        n += 1
        term *= x / n
        sum += term
        print(f"| {x:^10.2f} | {n:^10} | {sum:^20.10f} | {math.exp(x):^20.10f} | {eps:^10.2e} |")
    return sum