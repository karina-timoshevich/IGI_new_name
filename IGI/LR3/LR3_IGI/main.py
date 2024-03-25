import os
from task_1 import calculate_exp
from task_2 import sum_every_second
from task_3 import count_words_starting_with_consonant
from task_4 import analyze_text
from task_5 import main_task_5


if __name__ == '__main__':
    calculate_exp()
    sum_every_second()
    count_words_starting_with_consonant()

    text = '''«So she was considering in her own mind, as well as she could, for the hot day made her feel very 
    sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and 
    picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.  . .ф,,  There was nothing...'''
    analyze_text(text)
    main_task_5()
