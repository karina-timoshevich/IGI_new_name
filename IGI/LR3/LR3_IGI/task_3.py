def count_words_starting_with_consonant(string):
    try:
        consonants = 'bcdfghjklmnpqrstvwxz'
        words = string.split()
        count = 0

        for word in words:
            if word[0].lower() in consonants:
                count += 1

        return count
    except IndexError:
        print("Ошибка: вероятно ваша строка пуста.")


def task3():
    """Главная функция для задания 3, которая объединяет все остальные функции"""

    print("Задание №3. Подсчет слов, начинающихся со строчной согласной буквы.")
    input_string = input("Введите строку: ")
    print("Количество слов, начинающихся со строчной согласной буквы: ",
          count_words_starting_with_consonant(input_string))
