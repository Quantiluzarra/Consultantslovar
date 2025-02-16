# game.py

import random
import nltk
from nltk.corpus import words, stopwords, wordnet
from collections import defaultdict

# Загрузка ресурсов NLTK
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('words')

class Game:
    def __init__(self):
        self.word_lists = {
            'en': set(words.words()),
            'ru': self.load_russian_words()
        }
        self.stopwords = {
            'en': set(stopwords.words('english')),
            'ru': set(stopwords.words('russian'))
        }
        self.current_words = defaultdict(dict)
        self.statistics = defaultdict(lambda: {'wins': 0, 'games': 0})

    def load_russian_words(self):
        # Загрузка русского словаря
        # Используем wordnet или собственный список
        # Так как NLTK не содержит русского словаря, мы создадим небольшой набор популярных слов
        return set(['кот', 'собака', 'дом', 'человек', 'машина', 'город', 'река', 'лес', 'небо', 'звезда'])

    def start_game(self, user_id, language, difficulty):
        word = self.get_random_word(language, difficulty)
        self.current_words[user_id]['word'] = word
        self.current_words[user_id]['language'] = language
        self.statistics[user_id]['games'] += 1
        return word

    def get_random_word(self, language, difficulty):
        words_list = self.word_lists[language]
        word = random.choice(list(words_list))
        # В зависимости от сложности можно контролировать длину слова или его частотность
        # Для упрощения используем рандомное слово
        return word

    def check_guess(self, user_id, guess):
        secret_word = self.current_words[user_id]['word']
        language = self.current_words[user_id]['language']
        similarity = self.calculate_similarity(secret_word, guess, language)
        return similarity

    def calculate_similarity(self, word1, word2, language):
        # Упрощенная метрика сходства по количеству общих букв
        set1 = set(word1)
        set2 = set(word2)
        similarity = len(set1 & set2) / len(set1 | set2)
        return similarity

    def is_correct(self, user_id, guess):
        secret_word = self.current_words[user_id]['word']
        return guess.lower() == secret_word.lower()

    def increment_wins(self, user_id):
        self.statistics[user_id]['wins'] += 1
        self.current_words.pop(user_id, None)

    def get_statistics(self, user_id):
        return self.statistics[user_id]
