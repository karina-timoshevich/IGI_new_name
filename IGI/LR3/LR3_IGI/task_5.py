import check_input
import initialisation


def process_list(lst):
    """Реализация основного задания с выводом результатов"""
    try:
        min_abs = min(lst, key=abs)
        first_positive = next(i for i, num in enumerate(lst) if num > 0)
        last_positive = len(lst) - 1 - next(i for i, num in enumerate(reversed(lst)) if num > 0)
        sum_between = sum(lst[first_positive+1:last_positive])
        print(f"Минимальный по модулю элемент списка: {min_abs}")
        print(f"Сумма элементов списка, расположенных между первым и последним положительными элементами: {sum_between}")
    except StopIteration:
        print("В списке нет положительных элементов или только один положительный элемент.")


def print_list(lst):
    """Вывод списка на экран"""
    print(lst)


def task5():
    """Главная функция для задания 5, которая объединяет все остальные функции"""
    print("Задание №5. Обработка списка. Вывод минимального по модулю элемента и суммы элементов между первым и последним положительными элементами.")
    lst = []
    print("Вы хотите заполнить список сами или использовать генератор?")
    print("1. Самостоятельно")
    print("2. Генератор")
    choice = check_input.input_positive_integer()
    if choice == 1:
        initialisation.input_list_by_user(lst)
    elif choice == 2:
        print("Введите размер списка: ")
        size = check_input.input_positive_integer()
        lst = list(initialisation.input_list_by_generator(initialisation.generator(size)))
    else:
        print("Некорректный ввод.")
        return
    # print(lst)
    # initialisation.input_list_by_user(lst)
    process_list(lst)
    print_list(lst)
