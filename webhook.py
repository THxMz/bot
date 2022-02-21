# *- coding: utf-8 -*-

import telebot
import telebot, sys
from flask import Flask, request

url = 'Your Host' #Config Host

#-----------------------------------------------------------------------------#
"Variable"
bot = telebot.TeleBot("Enter your token here", threaded=False)
bt2 = telebot.TeleBot("token 2") #If you don't need you can delete.
sys.tracebacklimit = 0
#-----------------------------------------------------------------------------#

"Webhook"
bot.remove_webhook()
bot.set_webhook(url=url)

app = Flask(__name__)
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route('/', methods=['GET'])
def webhook_get():
    return "HI, This is my site with flask."
