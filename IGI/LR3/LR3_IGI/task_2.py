import check_input


def sum_every_second_number():
    """Считает сумму каждого второго числа, пока не введется 1."""

    sum_of_elements = 0
    counter = 0

    while True:
        print("Введите число: ")
        number = check_input.input_float()
        if number == 1:
            break
        if counter % 2 != 0:
            sum_of_elements += number
        counter += 1

    return sum_of_elements


def task2():
    """Считает сумму каждого второго числа, пока не введется 1."""

    print("Задание №2. Сумма каждого второго числа, пока не введется 1.")
    sum_of_elements = sum_every_second_number()
    print("Сумма каждого второго числа: ", sum_of_elements)
