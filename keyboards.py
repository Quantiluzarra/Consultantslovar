# keyboards.py

from telegram import ReplyKeyboardMarkup

def main_menu(language):
    if language == 'ru':
        keyboard = [['Играть'], ['👤 Профиль', '⚙️ Настройки']]
    else:
        keyboard = [['Play'], ['👤 Profile', '⚙️ Settings']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def settings_menu(language):
    if language == 'ru':
        keyboard = [['Язык', 'Сложность'], ['⬅️ Назад']]
    else:
        keyboard = [['Language', 'Difficulty'], ['⬅️ Back']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def language_menu():
    keyboard = [['Русский', 'English'], ['⬅️ Назад']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def difficulty_menu():
    keyboard = [['Легкая', 'Средняя', 'Сложная'], ['⬅️ Назад']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
