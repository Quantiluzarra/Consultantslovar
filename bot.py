import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random

# Установка токена бота
TOKEN = '7881659124:AAH61KoBUM5PZlcf3BY5BaQAcI3FS0dpHKk'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Данные пользователя
users_data = {}

# Поддерживаемые языки
LANGUAGES = ['ru', 'en']

# Уровни сложности
DIFFICULTIES = ['Легкий', 'Средний', 'Тяжелый']

# Функция для получения случайного слова
def get_random_word(language):
    if language == 'ru':
        word_list = [w.strip().lower() for w in open("russian_words.txt", encoding='utf-8')]
    elif language == 'en':
        word_list = [w.strip().lower() for w in open("english_words.txt")]
    else:
        word_list = []
    return random.choice(word_list)

# Функция для генерации подсказок
def generate_hint(word):
    hints = [
        f"Слово начинается на букву: {word[0].upper()}",
        f"Слово заканчивается на букву: {word[-1].upper()}",
        f"Длина слова: {len(word)} букв",
        f"В слове есть буква: {random.choice(word[1:-1]).upper()}",
        f"Сумма буквенных кодов слова: {sum([ord(c) for c in word])}"
    ]
    return random.choice(hints)

# Команда /start
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    users_data[message.from_user.id] = {
        'language': 'ru',
        'difficulty': 'Средний',
        'games_played': 0,
        'wins': 0,
        'current_word': '',
        'hints_used': 0
    }
    await message.answer("Добро пожаловать в игру! Чтобы начать, нажмите 'Играть'.", reply_markup=main_menu())

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Играть'))
    markup.add(types.KeyboardButton('Настройки'), types.KeyboardButton('Профиль'))
    return markup

# Команда Играть
@dp.message_handler(lambda message: message.text == 'Играть')
async def play_game(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if user_data:
        language = user_data['language']
        difficulty = user_data['difficulty']
        word = get_random_word(language)
        user_data['current_word'] = word
        user_data['games_played'] += 1
        user_data['hints_used'] = 0
        hint = generate_hint(word)
        await message.answer(f"Угадайте слово:\n{hint}", reply_markup=types.ReplyKeyboardRemove())
    else:
        await start_game(message)

# Обработка ответа пользователя
@dp.message_handler()
async def check_answer(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if user_data:
        if message.text == 'Настройки':
            await show_settings(message)
        elif message.text == 'Профиль':
            await show_profile(message)
        elif user_data['current_word']:
            if message.text.lower() == user_data['current_word']:
                user_data['wins'] += 1
                await message.answer("Поздравляем! Вы угадали слово!", reply_markup=main_menu())
                user_data['current_word'] = ''
            else:
                await message.answer("Неправильно, попробуйте еще раз или запросите подсказку командой /hint.")
        else:
            await message.answer("Используйте кнопки меню для навигации.", reply_markup=main_menu())
    else:
        await start_game(message)

# Команда /hint
@dp.message_handler(commands=['hint'])
async def give_hint(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if user_data and user_data['current_word']:
        hint = generate_hint(user_data['current_word'])
        user_data['hints_used'] += 1
        await message.answer(f"Подсказка:\n{hint}")
    else:
        await message.answer("Сейчас нет активной игры. Нажмите 'Играть' для начала.")

# Показ настроек
async def show_settings(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if user_data:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Язык'), types.KeyboardButton('Сложность'))
        markup.add(types.KeyboardButton('Назад'))
        await message.answer("Настройки:", reply_markup=markup)
    else:
        await start_game(message)

# Обработка настроек
@dp.message_handler(lambda message: message.text in ['Язык', 'Сложность', 'Назад'])
async def settings_handler(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if message.text == 'Язык':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for lang in LANGUAGES:
            markup.add(types.KeyboardButton(lang.upper()))
        markup.add(types.KeyboardButton('Назад'))
        await message.answer("Выберите язык:", reply_markup=markup)
    elif message.text.upper() in [lang.upper() for lang in LANGUAGES]:
        user_data['language'] = message.text.lower()
        await message.answer(f"Язык установлен: {message.text}", reply_markup=main_menu())
    elif message.text == 'Сложность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for diff in DIFFICULTIES:
            markup.add(types.KeyboardButton(diff))
        markup.add(types.KeyboardButton('Назад'))
        await message.answer("Выберите уровень сложности:", reply_markup=markup)
    elif message.text in DIFFICULTIES:
        user_data['difficulty'] = message.text
        await message.answer(f"Сложность установлена: {message.text}", reply_markup=main_menu())
    elif message.text == 'Назад':
        await message.answer("Возвращаюсь в главное меню.", reply_markup=main_menu())
    else:
        await message.answer("Некорректный выбор. Пожалуйста, выберите параметр из меню.")

# Показ профиля
async def show_profile(message: types.Message):
    user_data = users_data.get(message.from_user.id)
    if user_data:
        await message.answer(
            f"Профиль:\n"
            f"Игры сыграно: {user_data['games_played']}\n"
            f"Победы: {user_data['wins']}\n"
            f"Язык: {user_data['language'].upper()}\n"
            f"Сложность: {user_data['difficulty']}"
        )
    else:
        await start_game(message)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
