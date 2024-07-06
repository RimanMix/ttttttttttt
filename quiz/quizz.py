import json
from telebot import TeleBot, types

indx = 0
points = 0
game = False

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

with open('quiz/my_quizz.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_next_keyboard(data, indx):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in data[indx]['вариант']:
        btn = types.KeyboardButton(option)
        markup.add(btn)
    markup.add(types.KeyboardButton('Выход'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Отправьте команду /quiz, чтобы начать викторину.')

@bot.message_handler(commands=['quiz'])
def quiz(message):
    global game, indx, points
    game = True
    indx = 0
    points = 0
    markup = get_next_keyboard(data, indx)
    q = data[indx]['вопрос']
    bot.send_message(message.chat.id, q, reply_markup=markup)

@bot.message_handler()
def handle_message(message):
    global points, indx, game
    if game:
        if message.text == 'Выход':
            bot.send_message(message.chat.id, f'Игра окончена. Ваш счет: {points}')
            game = False
            return
        
        if message.text == data[indx]['ответ']:
            bot.send_message(message.chat.id, 'Правильно!')
            points += 1
        else:
            bot.send_message(message.chat.id, f'Неправильно! Правильный ответ: {data[indx]["ответ"]}')
        
        indx += 1
        if indx < len(data):
            markup = get_next_keyboard(data, indx)
            q = data[indx]['вопрос']
            bot.send_message(message.chat.id, q, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'Игра окончена. Ваш счет: {points}')
            game = False
    else:
        bot.send_message(message.chat.id, 'Для начала викторины отправьте команду /quiz.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
