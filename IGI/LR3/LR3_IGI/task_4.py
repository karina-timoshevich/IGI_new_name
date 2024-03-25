import string


def task_a(text):
    """Определить, сколько слов имеют минимальную длину"""

    # Заменяем все символы, кроме букв, на пробелы
    text = ''.join(char if char.isalpha() else ' ' for char in text)

    words = text.split()
    min_length = min(len(word) for word in words)
    min_length_words = [word for word in words if len(word) == min_length]
    print(f"Количество слов с минимальной длиной: {len(min_length_words)}")
    print(f"Слова с минимальной длиной: {min_length_words}")


def task_b(text):
    """Вывести все слова, за которыми следует точка"""

    sentences = text.split('.')
    words_before_dot = [sentence.rstrip().split()[-1] for sentence in sentences[:-1] if sentence.strip()]
    if sentences[-1].strip().endswith('.'):
        words_before_dot.append(sentences[-1].rstrip().split()[-1])
    print(f"Слова, за которыми следует точка: {words_before_dot}")


def task_c(text):
    """Найти самое длинное слово, которое заканчивается на 'r'"""

    words = text.replace(',', '').split()
    r_words = [word for word in words if word.endswith('r') or word.endswith('R')]
    longest_r_word = max(r_words, key=len, default='')
    print(f"Самое длинное слово, заканчивающееся на 'r': {longest_r_word}")


def analyze_text(text):
    """Анализирует текст по заданным критериям"""

    task_a(text)
    task_b(text)
    task_c(text)