# Main file for the 3rd lab work of Python course
# Program was created by Timoshevich Karina, group 253503
# Date: 2024.25.03
# Version: 1.0

import os
from colorama import Fore, Style   # print(Style.RESET_ALL) - сброс стилей
from task_1 import task1
from task_2 import task2
from task_3 import task3
from task_4 import task4
from task_5 import task5


def menu():
    print(Style.BRIGHT)
    print(Fore.MAGENTA + "Добро пожаловать в пространство 3 лабораторной работы!")
    print("Выполнила студентка группы 253503, Тимошевич Карина, вариант 25")
    while True:
        print(Style.BRIGHT)
        print(Fore.MAGENTA)
        print("Хотите взглянуть на какое-нибудь задание? Просто выберите понравившийся пункт:")
        print("1. Выполнить 1 задание (вычисление экспоненты в степени х с помощью ряда Тейлора)")
        print("2. Выполнить 2 задание (сумма каждого второго числа, пока не введется 1)")
        print("3. Выполнить 3 задание (подсчет слов, начинающихся со строчной согласной буквы)")
        print("4. Выполнить 4 задание (анализ текста по заданным параметрам)")
        print("5. Выполнить 5 задание (обработка списка)")
        print("6. Выход")

        choice = input("Введите номер выбранной задачи: ")

        if choice == '1':
            print(Fore.CYAN + "\nВы выбрали 1 задание, начнем его выполнение!" + Style.RESET_ALL)
            task1()
        elif choice == '2':
            print(Fore.CYAN + "\nВы выбрали 2 задание, начнем его выполнение!" + Style.RESET_ALL)
            task2()
        elif choice == '3':
            print(Fore.CYAN + "\nВы выбрали 3 задание, начнем его выполнение!" + Style.RESET_ALL)
            task3()
        elif choice == '4':
            print(Fore.CYAN + "\nВы выбрали 4 задание, начнем его выполнение!" + Style.RESET_ALL)
            task4()
        elif choice == '5':
            print(Fore.CYAN + "\nВы выбрали 5 задание, начнем его выполнение!" + Style.RESET_ALL)
            task5()
        elif choice == '6':
            print(Fore.CYAN + "\nЭх, уже уходите, было приятно провести с вами время, до новых встреч :)")
            break
        else:
            print("\nОй-ой-ой, кажется, вы ввели что-то не то, попробуйте еще раз и всё получится!")


if __name__ == '__main__':
    # print(task4.__doc__)
    menu()
