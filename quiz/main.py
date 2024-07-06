import json
from telebot import TeleBot, types

indx = 0
points = 0
game = False

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

with open('quiz/victorina.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_next_keyboard(data, indx):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(4):
        btn = types.KeyboardButton(data[indx]['вариант'][i])
        markup.add(btn)
    markup.add(types.KeyboardButton('Выход'))
    return markup


@bot.message_handler(commands=['quiz'])
def quiz(message):
    global game
    game = True
    markup = get_next_keyboard(data, indx)
    q = data[indx]['вопрос']
    bot.send_message(message.chat.id, q, reply_markup=markup)


@bot.message_handler()
def game(message):
    global points, indx, game
    if game:
        if message.text == data[indx]['ответ']:
            bot.send_message(message.chat.id, 'Правильно!')
            points += 1
        elif message.text == 'Выход':
            bot.send_message(message.chat.id, f'Игра окенчена. Ваш счет {points}')
            game = False
            return
        else:
            bot.send_message(message.chat.id, f'Неправильно! Правильный ответ: {data[indx]["ответ"]}')
        indx += 1
        mark = get_next_keyboard(data, indx)
        if indx < len(data):
            q = data[indx]['вопрос']
            bot.send_message(message.chat.id, q, reply_markup=mark)
        else:
            bot.send_message(message.chat.id, f'Игра окенчена. Ваш счет {points}')
            game = False



if __name__ == '__main__':
    bot.polling(none_stop=True)
