import check_input


def input_list():
    """Ввод элементов списка пользователем"""
    lst = []
    print("Введите размер списка: ")
    size = check_input.input_positive_integer()
    for _ in range(size):
        print("Введите элемент списка: ")
        num = check_input.input_float()
        lst.append(num)
    return lst


def is_valid(lst):
    """Проверка корректности вводимых данных"""
    return all(isinstance(num, float) for num in lst)


def process_list(lst):
    """Реализация основного задания с выводом результатов"""
    min_abs = min(lst, key=abs)
    first_positive = next(i for i, num in enumerate(lst) if num > 0)
    last_positive = len(lst) - 1 - next(i for i, num in enumerate(reversed(lst)) if num > 0)
    sum_between = sum(lst[first_positive+1:last_positive])
    print(f"Минимальный по модулю элемент списка: {min_abs}")
    print(f"Сумма элементов списка, расположенных между первым и последним положительными элементами: {sum_between}")


def print_list(lst):
    """Вывод списка на экран"""
    print(lst)


def main_task_5():
    """Главная функция для задания 5, которая объединяет все остальные функции"""
    lst = input_list()
    if is_valid(lst):
        process_list(lst)
        print_list(lst)
    else:
        print("Введенные данные некорректны.")