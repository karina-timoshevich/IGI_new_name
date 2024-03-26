def input_positive_integer():
    """Запрашивает у пользователя ввод целого числа"""

    while True:
        num = input()
        if num.isdigit():
            return int(num)
        else:
            print("Введенные данные некорректны. Пожалуйста, введите положительное целое число.")


def input_float():
    """Запрашивает у пользователя ввод дробного числа"""
    while True:
        num = input()
        if num.lstrip('-').replace('.', '', 1).isdigit():
            return float(num)
        else:
            print("Введенные данные некорректны. Пожалуйста, введите число.")


def input_positive_float():
    """Запрашивает у пользователя ввод положительного дробного числа"""
    while True:
        num = input()
        if num.replace('.', '', 1).isdigit():
            return float(num)
        else:
            print("Введенные данные некорректны. Пожалуйста, введите положительно целое/дробное число.")