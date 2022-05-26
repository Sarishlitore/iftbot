from telebot import TeleBot, types

import credentials
from db import DataBase

db = DataBase(credentials.db_host, credentials.db_user, credentials.db_password)

bot = TeleBot(credentials.bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_button = types.KeyboardButton("Сохранить книгу")
    delete_button = types.KeyboardButton("Удалить книгу")
    saved_books_list = types.KeyboardButton("Список сохраненных книг")
    markup.add(save_button)
    markup.add(delete_button)
    markup.add(saved_books_list)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['chat_id'])
def chat_id_message(message):
    bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, show_available_commands())


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Сохранить книгу":
        bot.register_next_step_handler(message, save_book)
    elif message.text == "Удалить книгу":
        bot.register_next_step_handler(message, delete_book)
    elif message.text == "Список сохраненных книг":
        bot.reply_to(message, show_saved_books(), parse_mode="Markdown", )
    else:
        bot.send_message(credentials.my_channel_id, message.text)


def save_book(message):
    try:
        book_name = message.text
        db.save_book(book_name)
    except Exception as e:
        bot.reply_to(message, e.__str__())


def delete_book(message):
    try:
        book_name = message.text
        db.delete_book(book_name)
    except Exception as e:
        bot.reply_to(message, e.__str__())


def show_saved_books() -> str:
    text = "Сохраненные книги:\n"
    books = db.show_books()
    for book in books:
        text += "\n`" + book + '`'
    return text


def show_available_commands() -> str:
    commands = ['start', 'help', 'chat_id']
    return "Доступные комманды /" + " /".join(commands)


bot.polling(none_stop=True)
