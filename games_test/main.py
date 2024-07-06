from random import choice
from telebot import TeleBot

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

game_choice = ['камень', 'ножницы', 'бумага']

# message.text

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, I am a bot!')


if __name__ == '__main__':
    bot.polling(none_stop=True)