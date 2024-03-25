def count_words_starting_with_consonant():
    input_string = input("Введите строку: ")
    consonants = 'bcdfghjklmnpqrstvwxyz'
    words = input_string.split()
    count = 0

    for word in words:
        if word[0].lower() in consonants:
            count += 1

    print("Количество слов, начинающихся со строчной согласной буквы: ", count)
    return count