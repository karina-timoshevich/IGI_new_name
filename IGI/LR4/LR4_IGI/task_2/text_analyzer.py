import re
import zipfile


class TextAnalyzer:
    def __init__(self, source_file, result_file):
        self.source_file = source_file
        self.result_file = result_file
        self.text = None

    def read_text(self):
        with open(self.source_file, 'r') as f:
            self.text = f.read()

    def analyze_text(self):
        sentences = re.split(r'(?<=[.!?])\s+', self.text)
        declarative_sentences = [s for s in sentences if s.endswith('.')]
        interrogative_sentences = [s for s in sentences if s.endswith('?')]
        imperative_sentences = [s for s in sentences if s.endswith('!')]
        words = re.findall(r'\b\w+\b', self.text)
        emoticons = re.findall(r'[:;]-*[()\[\]]+', self.text)
        sentences_with_apostrophes = [s for s in sentences if "'" in s]
        time_replaced_text = re.sub(r'\b([01]\d|2[0-3]):([0-5]\d)(:[0-5]\d)?\b', '(TBD)', self.text)
        words_ending_with_vowel = [w for w in words if w[-1] in 'aeiouAEIOU']
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)
        words_with_avg_length = [w for w in words if len(w) == round(avg_word_length)]
        return sentences, declarative_sentences, interrogative_sentences, imperative_sentences, words, emoticons, sentences_with_apostrophes, time_replaced_text, words_ending_with_vowel, avg_sentence_length, avg_word_length, words_with_avg_length

    def save_results(self, results):
        with open(self.result_file, 'w', encoding='utf-8') as f:
            f.write(f"Количество предложений: {len(results[0])}\n")
            f.write(f"Количество повествовательных предложений: {len(results[1])}\n")
            f.write(f"Количество вопросительных предложений: {len(results[2])}\n")
            f.write(f"Количество побудительных предложений: {len(results[3])}\n")
            f.write(f"Средняя длина предложения: {round(results[9])}\n")
            f.write(f"Средняя длина слова: {round(results[10])}\n")
            f.write(f"Количество смайликов: {len(results[5])}\n")
            f.write(f"Предложения с апострофами: {results[6]}\n")
            f.write(f"Текст со замененным временем:\n{results[7]}\n")
            f.write(f"Количество слов, заканчивающихся на гласную: {len(results[8])}\n")
            f.write(f"Слова со средней длиной: {results[11] if results[11] else 'Слов со средней длиной нет'}\n")

    def archive_results(self, file_path="D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/result.txt"):
        with zipfile.ZipFile('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/la4_igi.zip', mode='a',
                             compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname='new_result')
        print("Результаты анализа текста сохранены в архиве result.zip")

    def get_archive_info(self):
        with zipfile.ZipFile('D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/la4_igi.zip', 'r') as zipf:
            info = zipf.getinfo('new_result')
            print(f"Размер сжатого файла: {info.compress_size} байт")
            print(f"Размер несжатого файла: {info.file_size} байт")

    def analyze(self):
        self.read_text()
        results = self.analyze_text()
        self.save_results(results)
        self.archive_results()
        self.get_archive_info()
        pass



