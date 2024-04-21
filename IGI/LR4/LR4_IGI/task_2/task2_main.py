from task_2.text_analyzer import TextAnalyzer


def task2():
    analyzer = TextAnalyzer('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/text.txt',
                            'D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/result.txt')
    analyzer.analyze()
    with open('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/result.txt', 'r', encoding='utf-8') as f:
        print(f.read())


task2()
