import json
import os
from random import choice
from telebot import TeleBot, types

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

game = False
used_cities = []
letter = ''
points = 0
leaderboard = {}

def select_letter(word):
    i = -1
    letter = word[i]
    while letter in ('ъ', 'ь', 'ы', 'й'):
        i -= 1
        letter = word[i]
    return letter

def load_leaderboard():
    global leaderboard
    if os.path.exists('goroda/leaderboard.json'):
        with open('goroda/leaderboard.json', 'r', encoding='utf-8') as f:
            leaderboard = json.load(f)
    else:
        leaderboard = {}

def save_leaderboard():
    with open('goroda/leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)

with open('goroda/cities.txt', 'r', encoding='utf-8') as f:
    cities = [line.strip().lower() for line in f.readlines()]

load_leaderboard()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['goroda'])
def goroda(message):
    global game, letter, points, used_cities
    game = True
    points = 0
    used_cities = []
    city = choice(cities)
    used_cities.append(city)
    letter = select_letter(city)
    bot.send_message(message.chat.id, f'Я начинаю игру! Первый город {city}. Ты должен написать город на букву "{letter}".')

@bot.message_handler(commands=['stop'])
def stop_game(message):
    global game, points
    if game:
        bot.send_message(message.chat.id, f'Игра остановлена. Твой счет: {points}.')
        game = False
        points = 0
    else:
        bot.send_message(message.chat.id, 'Игра не идет в данный момент.')

@bot.message_handler(commands=['score'])
def show_score(message):
    bot.send_message(message.chat.id, f'Текущий счет: {points}')

@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(message):
    leaderboard_text = 'Таблица лидеров:\n'
    for user_id, score in leaderboard.items():
        leaderboard_text += f'{user_id}: {score} очков\n'
    bot.send_message(message.chat.id, leaderboard_text)

@bot.message_handler(commands=['save'])
def save_score(message):
    save_leaderboard()
    bot.send_message(message.chat.id, 'Текущие результаты сохранены!')

@bot.message_handler(commands=['all_scores'])
def show_all_scores(message):
    if os.path.exists('goroda/leaderboard.json'):
        with open('goroda/leaderboard.json', 'r', encoding='utf-8') as f:
            leaderboard_data = json.load(f)
        all_scores_text = 'Все результаты:\n'
        for user_id, score in leaderboard_data.items():
            all_scores_text += f'{user_id}: {score} очков\n'
        bot.send_message(message.chat.id, all_scores_text)
    else:
        bot.send_message(message.chat.id, 'Файл с результатами не найден.')

@bot.message_handler()
def play(message):
    global game, letter, points
    user_city = message.text.lower()
    user_id = str(message.from_user.id)  # Convert user ID to string for JSON compatibility

    if game:
        if user_city in used_cities:
            bot.send_message(message.chat.id, 'Этот город уже был.')
            return
        if user_city[0] != letter:
            bot.send_message(message.chat.id, f'Город должен начинаться на букву "{letter}".')
            return
        if user_city not in cities:
            bot.send_message(message.chat.id, 'Такого города нет.')
            return

        points += 1
        letter = select_letter(user_city)
        used_cities.append(user_city)

        for city in cities:
            if city[0] == letter and city not in used_cities:
                used_cities.append(city)
                letter = select_letter(city)
                bot.send_message(message.chat.id, f'Мой город {city}. Твой ход! Текущий счет: {points}')
                return

        bot.send_message(message.chat.id, f'Ты выиграл! Твой счет: {points}. Напиши /goroda, чтобы начать заново.')
        game = False
        if user_id in leaderboard:
            leaderboard[user_id] += points
        else:
            leaderboard[user_id] = points

if __name__ == '__main__':
    bot.polling(none_stop=True)
