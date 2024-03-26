import check_input


def input_list_by_user(lst):
    """Ввод элементов списка пользователем"""

    print("Введите размер списка: ")
    size = check_input.input_positive_integer()
    for _ in range(size):
        print("Введите элемент списка: ")
        num = check_input.input_float()
        lst.append(num)
    return lst


def input_list_by_generator(generator1):
    """Генерация списка с помощью генератора"""

    return [i for i in generator1]


def generator(size):
    """Генератор, который создает последовательность чисел от 0 до size"""

    for i in range(size):
        yield i+10


def init(lst):
    print("Введите размер списка: ")
    size = check_input.input_positive_integer()
    lst = list(input_list_by_generator(generator(size)))
