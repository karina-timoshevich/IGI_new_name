from task_2.text_analyzer import TextAnalyzer


# Создайте экземпляр класса TextAnalyzer
def task2():
    analyzer = TextAnalyzer('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/text.txt',
                            'D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/result.txt')

    # Вызовите метод analyze для анализа текста
    analyzer.analyze()
    # Вывод содержимого файла result.txt в консоль
    with open('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/result.txt', 'r', encoding='utf-8') as f:
        print(f.read())

task2()
