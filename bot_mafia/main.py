from time import time
from random import choice
from telebot import TeleBot, types


with open('bot_mafia/bad_words.txt', 'r', encoding='utf-8') as file:
    bad_words = [line.strip().lower() for line in file.readlines()]


TOKEN = '7092457320:AAG8qrYvpdatP3PVWxLsH_STh6Z-Mc7kUms'
bot = TeleBot(TOKEN)

def has_bad_word(text):
    return any ([word in text.lower() for word in bad_words])


@bot.message_handler(func=lambda m: has_bad_word(m.text.lower()))
def censor(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Такие слова использовать нельзя')
    bot.restrict_chat_member(message.chat,id, 
                             message.from_user.id, 
                             until_date=time()+60)

@bot.message_handler(func=lambda m: m.entities is not None)
def delete_links(message):
    for entity in message.entities:
        if entity.type == 'url':
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Ссылки запрещены!')
            break
 

if __name__ == '__main__':
    bot.polling(none_stop=True)
