from random import randint
from telebot import TeleBot

TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

class GameManager:
    def __init__(self):
        self.user_points = 10  # Изначально даем игроку 10 очков

gm = GameManager()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот игры "Loot Box". Чтобы открыть лутбокс, используйте команду /lootbox.')

@bot.message_handler(commands=['lootbox'])
def lootbox(message):
    if gm.user_points == 0:
        bot.send_message(message.chat.id, "У вас недостаточно очков, чтобы открыть лутбокс.")
        return
    
    gm.user_points -= 1  # Уменьшаем количество очков на 1
    
    if gm.user_points <= 80:
        number = randint(1, 100)
        if number <= 80:
            image = 'C:/Users/admin/Downloads/UIDD/bot/lootbox/rare.png'
        elif number <= 95:
            image = 'C:/Users/admin/Downloads/UIDD/bot/lootbox/super_rare.png'
        else:
            image = 'C:/Users/admin/Downloads/UIDD/bot/lootbox/epic.png'
        
        img = open(image, 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        
    bot.send_message(message.chat.id, f"Осталось очков: {gm.user_points}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
