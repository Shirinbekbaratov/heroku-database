import os
#from datetime import *

import telebot
from telebot import types
from flask import Flask, request
from config import *
from libgen_api import LibgenSearch

s = LibgenSearch()
results = s.search_author("Jane Austen")
item_to_download = results[0]
download_links = s.resolve_download_links(item_to_download)['GET']
#print(download_links)

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Assalomu alaykum, ' + message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Menu")
    btn2 = types.KeyboardButton("❓ Haqida")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Salom, {0.first_name}! men menu botman! Quyidagi knopkalarni bosib men haqimda blib oling".format(message.from_user), reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "👋 Menu"):
        bot.send_message(message.chat.id, text="Biz hozir test rejimida ishlayapmiz!)")
    elif(message.text == "❓ Haqida"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Bu qanday bot?")
        btn2 = types.KeyboardButton("Menuni ko'rasizmi?")
        back = types.KeyboardButton("Bosh menuga qaytish")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Menga savollaringiz bormi", reply_markup=markup)

    elif(message.text == "Bu qanday bot?"):
        bot.send_message(message.chat.id,download_links, "Toshkent,Olmaliq sh")

    elif message.text == "Menuni ko'rasizmi?":
        bot.send_message(message.chat.id, text="Sizga buyurtma berishda yordamlashaman")

    elif (message.text == "Bosh menuga qaytish"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Menu")
        button2 = types.KeyboardButton("❓ Haqida")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Bosh sahifaga qaytdingiz", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Bu buyruqni bajara olmayman")

#bot.polling(none_stop=True)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)

@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
