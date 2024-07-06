from random import choice
from telebot import TeleBot

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

game_choice = ['камень', 'ножницы', 'бумага']
user_poinsts = 0
bot_poinsts = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот игры "камень, ножницы, бумага". Чтобы начать игру, используйте команду /play.')

@bot.message_handler(commands=['play'])
def play(message):
    bot.send_message(message.chat.id, 'Выбери свой ход: камень, ножницы или бумага.')

@bot.message_handler(func=lambda message: message.text.lower() in game_choice)
def handle_choice(message):
    bot_choice = choice(game_choice)
    user_choice = message.text.lower()
    
    if user_choice == bot_choice:
        bot.send_message(message.chat.id, f'Ничья! Я выбрал {bot_choice}, как и ты.')
    elif (user_choice == 'камень' and bot_choice == 'ножницы') or \
         (user_choice == 'ножницы' and bot_choice == 'бумага') or \
         (user_choice == 'бумага' and bot_choice == 'камень'):
        bot.send_message(message.chat.id, f'Поздравляю! Ты выиграл! Я выбрал {bot_choice}.')
    else:
        bot.send_message(message.chat.id, f'К сожалению, ты проиграл! Я выбрал {bot_choice}.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Я не понимаю. Для начала игры используй команду /play.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
