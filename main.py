# -*- coding: utf-8 -*-

import telebot, sys
import mysql.connector

#-----------------------------------------------------------------------------#
"Variable"
bot = telebot.TeleBot("Your token")
bt2 = telebot.TeleBot("Your token 2")
sys.tracebacklimit = 0
#-----------------------------------------------------------------------------#
#Database
#If you want database you can use this script.
"""cnx = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    database="")
cur = cnx.cursor()"""
#-----------------------------------------------------------------------------#

print('Bot is started......')
print("If you want to exit, You can press Ctrl + C to exit evertime :) ")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi, I'm bot. Can I help you?")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id , "I'm copy your text :)")

bot.infinity_polling()
