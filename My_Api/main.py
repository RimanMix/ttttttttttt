from random import choice
from telebot import TeleBot, types
from my_api import get_rundom_duck, get_rundom_dog, get_rundom_fox
import wikipedia
wikipedia.set_lang('ru')


TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def score(message):
    bot.send_message(message.chat.id, f'Hello')

@bot.message_handler(commands=['duck'])
def score(message):
    url = get_rundom_duck()
    bot.send_message(message.chat.id, url)


@bot.message_handler(commands=['dog'])
def score(message):
    url = get_rundom_dog()
    bot.send_message(message.chat.id, url)

@bot.message_handler(commands=['fox'])
def score(message):
    url = get_rundom_fox()
    bot.send_message(message.chat.id, url)

@bot.message_handler(commands=['wiki'])
def wiki(message):
    text = ''.join(message.text.split('')[1:])
    results = wikipedia.search(text)
    markup = types.InlineKeyboardMarkup()
    for result in results:
        button = types.InlineKeyboardButton(text=result, callback_data=result)
        markup.add(button)
    bot.send_message(message.chat.id, text='Смотри что я нашел!', reply_markup=markup)



if __name__ == '__main__':
    bot.polling(none_stop=True)
