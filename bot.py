from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardRemove
from config import TOKEN, LANGUAGES, DIFFICULTIES
from game import Game
from keyboards import main_menu, settings_menu, language_menu, difficulty_menu

# Создаем экземпляр игры
game = Game()
# Хранилище настроек пользователей
user_settings = {}

def start(update, context):
    user_id = update.effective_chat.id
    user_settings[user_id] = {'language': 'ru', 'difficulty': 'medium'}
    update.message.reply_text(
        'Привет! Добро пожаловать в Контекстную игру!',
        reply_markup=main_menu('ru')
    )

def play(update, context):
    user_id = update.effective_chat.id
    language = user_settings[user_id]['language']
    difficulty = user_settings[user_id]['difficulty']
    word = game.start_game(user_id, language, difficulty)
    update.message.reply_text(
        'Игра началась! Попробуйте отгадать слово.',
        reply_markup=ReplyKeyboardRemove()
    )

def profile(update, context):
    user_id = update.effective_chat.id
    stats = game.get_statistics(user_id)
    message = f"👤 Ваш профиль:\nИгры: {stats['games']}\nПобеды: {stats['wins']}"
    update.message.reply_text(message)

def settings(update, context):
    user_id = update.effective_chat.id
    language = user_settings[user_id]['language']
    update.message.reply_text(
        '⚙️ Настройки:',
        reply_markup=settings_menu(language)
    )

def change_language(update, context):
    update.message.reply_text(
        'Выберите язык:',
        reply_markup=language_menu()
    )

def change_difficulty(update, context):
    update.message.reply_text(
        'Выберите сложность:',
        reply_markup=difficulty_menu()
    )

def handle_message(update, context):
    user_id = update.effective_chat.id
    text = update.message.text
    if user_id not in user_settings:
        user_settings[user_id] = {'language': 'ru', 'difficulty': 'medium'}
    language = user_settings[user_id]['language']

    if text in ['Играть', 'Play']:
        play(update, context)
    elif text in ['👤 Профиль', '👤 Profile']:
        profile(update, context)
    elif text in ['⚙️ Настройки', '⚙️ Settings']:
        settings(update, context)
    elif text in ['Язык', 'Language']:
        change_language(update, context)
    elif text in ['Сложность', 'Difficulty']:
        change_difficulty(update, context)
    elif text in ['Русский', 'English']:
        user_settings[user_id]['language'] = 'ru' if text == 'Русский' else 'en'
        update.message.reply_text(
            'Язык изменен.',
            reply_markup=main_menu(user_settings[user_id]['language'])
        )
    elif text in DIFFICULTIES.keys():
        user_settings[user_id]['difficulty'] = DIFFICULTIES[text]
        update.message.reply_text(
            'Сложность изменена.',
            reply_markup=main_menu(user_settings[user_id]['language'])
        )
    elif text in ['⬅️ Назад', '⬅️ Back']:
        update.message.reply_text(
            'Главное меню:',
            reply_markup=main_menu(user_settings[user_id]['language'])
        )
    else:
        process_guess(update, context, text)

def process_guess(update, context, guess):
    user_id = update.effective_chat.id
    if user_id not in game.current_words:
        update.message.reply_text(
            'У вас нет активной игры. Нажмите "Играть", чтобы начать новую игру.'
        )
        return
    language = user_settings[user_id]['language']
    if game.is_correct(user_id, guess):
        game.increment_wins(user_id)
        update.message.reply_text(
            '🎉 Поздравляем! Вы угадали слово!',
            reply_markup=main_menu(language)
        )
    else:
        similarity = game.check_guess(user_id, guess)
        update.message.reply_text(
            f'Неправильно. Сходство: {similarity:.2f}\nПопробуйте еще раз.'
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Команды
    dp.add_handler(CommandHandler('start', start))

    # Сообщения
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    updater.start_polling()
    print('Бот запущен...')
    updater.idle()

if __name__ == '__main__':
    main()
