import telebot
import telegram
from telebot import types

from credentials import bot_token

bot = telebot.TeleBot(bot_token)
saved_books: list[str] = []


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
        bot.reply_to(message, show_saved_books(), parse_mode=telegram.ParseMode.MARKDOWN, )
    else:
        bot.send_message(my_channel_id, message.text)


def save_book(message):
    try:
        book_name = message.text
        saved_books.append(book_name)
    except Exception as e:
        bot.reply_to(message, e.__str__())
    print(saved_books)


def delete_book(message):
    try:
        book_name = message.text
        saved_books.remove(book_name)
    except Exception as e:
        bot.reply_to(message, e.__str__())
    print(saved_books)


def show_saved_books() -> str:
    text = "Сохраненные книги:\n"
    for book in saved_books:
        text += "\n`" + book + '`'
    return text


def show_available_commands() -> str:
    commands = ['start', 'help', 'chat_id']
    return "Доступные комманды /" + " /".join(commands)


bot.polling(none_stop=True)
