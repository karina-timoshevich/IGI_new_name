def task_a(text):
    """Определить, сколько слов имеют минимальную длину"""

    try:
        text = ''.join(char if char.isalpha() else ' ' for char in text)

        words = text.split()
        min_length = min(len(word) for word in words)
        min_length_words = [word for word in words if len(word) == min_length]
        print(f"Количество слов с минимальной длиной: {len(min_length_words)}")
        print("Слова с минимальной длиной: " + ', '.join(min_length_words))
    except IndexError:
        print("\nОшибка: вероятно ваша строка пуста.\n")
    except ValueError:
        print("\nОшибка: вероятно ваша строка не содержит слов.\n")


def task_b(text):
    """Вывести все слова, за которыми следует точка"""

    try:
        sentences = text.split('.')
        words_before_dot = [sentence.rstrip().split()[-1] for sentence in sentences[:-1] if sentence.strip()]
        if sentences[-1].strip().endswith('.'):
            words_before_dot.append(sentences[-1].rstrip().split()[-1])
        print("Слова, за которыми следует точка: " + ', '.join(words_before_dot))

    except IndexError:
        print("\nОшибка: вероятно ваша строка пуста.\n")
    except ValueError:
        print("\nОшибка: вероятно ваша строка не содержит слов.\n")


def task_c(text):
    """Найти самое длинное слово, которое заканчивается на 'r'"""
    try:
        words = text.replace(',', '').split()
        r_words = [word for word in words if word.endswith('r') or word.endswith('R')]
        longest_r_word = max(r_words, key=len, default='')
        print(f"Самое длинное слово, заканчивающееся на 'r': {longest_r_word}")
    except IndexError:
        print("\nОшибка: вероятно ваша строка пуста.\n")
    except ValueError:
        print("\nОшибка: вероятно ваша строка не содержит слов.\n")


def task4():
    """Анализирует текст по заданным критериям"""

    print("Задание №4. Анализ текста по заданным критериям\n")
    print("a) Определить, сколько слов имеют минимальную длину")
    print("b) Вывести все слова, за которыми следует точка")
    print("c) Найти самое длинное слово, которое заканчивается на 'r'\n")

    print("Хотите ввести текст вручную или использовать тестовый?")
    print("1. Ввести текст вручную")
    print("2. Использовать тестовый текст")
    choice = input()
    if choice == '1':
        text = input("Введите текст: ")
    elif choice == '2':
        text = '''«So she was considering in her own mind, as well as she could, for the hot day made her feel 
                     very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of 
                     getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
                     There was nothing...'''
        text = text.strip().replace('   ', ' ')
        print(f"Текст: {text}")
    else:
        print("Нужно быть чуточку внимательнее, есть только вариант 1 либо 2")
        return
    task_a(text)
    task_b(text)
    task_c(text)
