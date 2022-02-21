# *- coding: utf-8 -*-

import os
import telebot
import description as dp
import tk
import telebot, logging, sys
import mysql.connector
import pyAesCrypt
from flask import Flask, request
from telebot import custom_filters, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

url = 'https://hxkmm.pythonanywhere.com/' #Config Host

#-----------------------------------------------------------------------------#
"Variable"
bot = telebot.TeleBot(tk.THxMz, threaded=False)
bt2 = telebot.TeleBot(tk.Private)
hd = ReplyKeyboardRemove()
sys.tracebacklimit = 0
#-----------------------------------------------------------------------------#
"Database"
cnx = mysql.connector.connect(
    host="hxkmm.mysql.pythonanywhere-services.com",
    user="hxkmm",
    passwd="ทัหๆสพนนะ",
    database="hxkmm$telex")
cur = cnx.cursor()
#-----------------------------------------------------------------------------#

"Webhook"
bot.remove_webhook()
bot.set_webhook(url=url)

"Path Reply markup Help_Command"
hmk = types.ReplyKeyboardMarkup(one_time_keyboard=False)
hmk.row_width = 3
hmk.add('Getapps', 'รอม', 'โค้ดเนม', 'trCamera', 'Messenger', 'ปลดล็อกเครื่อง', 'Magisk', 'อัพเดตรอม', 'อัพเดตโหมดกู้คืน', 'ตารางเรียน', 'โน้ต', 'คำสั่งถัดไป')
hmk.add('โอนเงิน 💸', 'เข้ารหัสไฟล์', 'รายงาน/แนะนำ')
hmk.add('ออกจากระบบ')

freeid = None
users = {}

app = Flask(__name__)
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route('/', methods=['GET'])
def webhook_get():
    return "HI, This is website for katies."

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    global freeid
    if message.chat.id not in users:
        freeid = message.chat.id
        bot.send_message(message.chat.id, "ดีจ้า ยืนยันตัวตนก่อน จิ้ม > /auth", parse_mode='HTML', reply_markup=hd)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.chat.id, message.from_user.first_name))
    else:
        bot.send_message(message.chat.id, "ดีจ้า {name} จิ้ม -> /help เพื่อดูข้อมูลเพิ่มเติม".format(name = message.from_user.first_name), reply_markup=hd)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
    print(message.from_user.first_name, " : ", message.text)

@bot.message_handler(commands=['auth'])
def find(message):
    global freeid

    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'กำลังตรวจสอบ...')
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.chat.id, message.from_user.first_name))
        logging.warning((message.from_user.first_name, message.text))

        if freeid == None:
            freeid = message.chat.id
            popup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            popup.add('AUTH')
            msg = bot.send_message(message.chat.id, 'ไม่พบข้อมูล โปรดจิ้มที่ด้านล่างเพื่อยืนยันข้อมูล', reply_markup=popup)
            bot.register_next_step_handler(msg, find_step2)
        else:
            bot.send_message(message.chat.id, 'ยืนยันตัวตนสำเร็จ!')
            bot.send_message(freeid, dp.start.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        print(users, freeid)
    else:
        bot.send_message(message.chat.id, 'ยืนยันสำเร็วแล้ว คุณ <b>{name}!</b>'.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
    print(message.from_user.first_name, " : ", message.text)

def find_step2(message):
    global freeid
    
    if message.text == 'AUTH':
        if message.chat.id not in users:
            bot.send_message(message.chat.id, 'กำลังตรวจสอบ...')

            if freeid == None:
                freeid = message.chat.id
                bot.send_message(message.chat.id, 'ไม่เจอข้อมูล โปรดจิ้ม -> /auth อีกครั้ง เพื่อทำการบันทึกข้อมูล')
            else:
                bot.send_message(message.chat.id, 'ยืนยันตนตัวสำเร็จ!', reply_markup=hd)
                bot.send_message(freeid, dp.start.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)

                users[freeid] = message.chat.id 
                users[message.chat.id] = freeid
                freeid = None

                bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
                print(users, freeid)
        else:
            bot.send_message(message.chat.id, 'ยืนยันสำเร็วแล้ว คุณ <b>{name}!</b>'.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
    else:
        bot.send_message(message.chat.id, 'Error Bug. Please contact to dev.')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
    print(message.from_user.first_name, " : ", message.text)

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.chat.id in users:
        msg = bot.reply_to(message, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(msg, help_next_step)
    else:
        bot.send_message(message.chat.id , 'ยืนยันตัวตนก่อนจ้า จิ้ม -> /auth')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.chat.id, message.from_user.first_name))
    print(message.from_user.first_name, " : ", message.text)

def help_next_step(message):
        textuser = message.text
        if (textuser == 'Getapps'):
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton("MI Getapps", url='https://drive.google.com/file/d/1488kDsfk3IlUoQasxV-TqcelPu_gEoTy/view?usp=drivesdk'))
            h = bot.reply_to(message, dp.getapps, reply_markup=markup)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(h, help_next_step)

        elif (textuser == 'รอม'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 3
            markup.add('vayu', 'lime', 'mojito', '⬅️ ย้อนกลับ')
            msg = bot.reply_to(message, 'รุ่นอะไรจ๊ะ', reply_markup=markup)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(msg, next_setup_devices)

        elif (textuser == 'โค้ดเนม'):
            y = bot.reply_to(message, dp.codename, reply_markup=hmk ,parse_mode='HTML')
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(y, help_next_step)

        elif (textuser == ('trCamera')):
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton("โหลดได้ที่นี่", url='https://drive.google.com/file/d/1Fj4RqOK0xz4c0Z57psNVuRHaEq2w4B1N/view?usp=sharing'))
            markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            markup1.add('Help')
            markup1.row_width = 1
            bot.reply_to(message, dp.trcamera, reply_markup=markup)
            msg = bot.reply_to(message, 'ส่วนด้านล่างคือวิธีใช้', reply_markup=markup1)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(msg, help_tr_step)

        elif (textuser == ('Messenger')):
            a = bot.reply_to(message, dp.Messenger, reply_markup=hmk, parse_mode='HTML')
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(a, help_next_step)

        elif (textuser == ('ปลดล็อกเครื่อง')):
            bt = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            bt.row_width = 1
            bt.add('ADB Driver', 'โหลดไฟล์', 'ปลดล็อกเครื่อง', 'ย้อนกลับ')
            pl = bot.reply_to(message, dp.preun, parse_mode='HTML', reply_markup=bt)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(pl, unlock_step)

        elif (textuser == ('เข้ารหัสไฟล์')):
            ch = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            ch.add('เข้ารหัสไฟล์', 'ถอดรหัสไฟล์', 'ย้อนกลับ')
            s = bot.send_message(message.chat.id, "เลือกเมนูด้านล่างเลยจ้า", reply_markup=ch)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(s, encrypt_step)

        elif (textuser == ('Magisk')):
            i = bot.send_message(message.chat.id, dp.Magisk, parse_mode='HTML', disable_web_page_preview=True, reply_markup=hmk)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(i, help_next_step)

        elif (textuser == ('อัพเดตรอม')):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            markup.add('ถัดไป', 'ยกเลิก')
            a = bot.reply_to(message, dp.textup, reply_markup=markup, parse_mode='HTML')
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom)

        elif (textuser == ('คำสั่งถัดไป')):
            pl = bot.reply_to(message, 'ว่าง ไม่รู้จะใส่อะไรดี', parse_mode='HTML',reply_markup=hmk)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(pl, help_next_step)

        elif (textuser == ('อัพเดตโหมดกู้คืน')):
            pl = bot.reply_to(message, 'ว่าง ไม่รู้จะใส่อะไรดี', parse_mode='HTML',reply_markup=hmk)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(pl, help_next_step)

        elif (textuser == ('โอนเงิน 💸')):
            mk = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            mk.add('SCB', 'K Plus')
            mk.add('ShopeePay')
            mk.add('True Wallet(1)', 'True Wallet(2)')
            mk.add('❌ Exit ❌')
            a = bot.send_message(message.chat.id, dp.money, reply_markup=mk ,parse_mode='HTML')
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(a, bank_photo)

        # Password
        elif (textuser == ('ตารางเรียน')):
            a = bot.reply_to(message, 'ใส่รหัสก่อน', reply_markup=hd)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(a, mytab)
        elif (textuser == ('รายงาน/แนะนำ')):
            a = bot.reply_to(message, 'ทิ้งข้อความไว้เลย เดี๋ยวข้อความนี้จะไปโผล่ที่นักพัฒนา 😁', reply_markup=hd)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(a, report)
        elif (textuser == 'โน้ต'):
            n = bot.send_message(message.chat.id, "ใส่รหัสก่อน", reply_markup=hd)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(n, note)
        
        elif (textuser == 'ออกจากระบบ'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 1
            markup.add('ยืนยัน ✔', 'ยกเลิก ❌')
            msg = bot.reply_to(message, "โปรดจิ้ม 'ยืนยัน' ที่ช่องด้านล่าง เพื่อยืนยันการออกจากระบบ", reply_markup=markup)
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.register_next_step_handler(msg, stop)
        else:
            bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
            bot.reply_to(message, "คำสั่งไม่ถูกต้อง")
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
        print(message.from_user.first_name, " : ", message.text)

def encrypt_step(message):
    if message.text == 'เข้ารหัสไฟล์':
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาจ้า จะเข้ารหัสให้", reply_markup=hd)
        bot.register_next_step_handler(s, encrypt_file)
    elif message.text == 'เข้ารหัสไฟล์เพิ่ม':
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาจ้า จะเข้ารหัสให้", reply_markup=hd)
        bot.register_next_step_handler(s, decrypt_file)
    elif message.text == 'ถอดรหัสไฟล์':
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาจ้า จะถอดรหัสให้", reply_markup=hd)
        bot.register_next_step_handler(s, decrypt_file)
    elif message.text == 'ถอดรหัสไฟล์เพิ่ม':
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาจ้า จะถอดรหัสให้", reply_markup=hd)
        bot.register_next_step_handler(s, decrypt_file)
    elif message.text == 'ย้อนกลับ':
        s = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bot.register_next_step_handler(s, help_next_step)
    elif message.text == 'ไม่ดีกว่า':
        s = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bot.register_next_step_handler(s, help_next_step)
    else:
        s = bot.send_message(message.chat.id, 'คำสั่งไม่ถูกต้อง', reply_markup=hmk)
        bot.register_next_step_handler(s, help_next_step)

def encrypt_file(message):
    if message.document:
        bot.send_message(message.chat.id, "รอแป๊บนึง กำลังเข้ารหัสไฟล์...")
        file = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file.file_path)
        nf = message.document.file_name
        ps = "@ewg1#ec@fewp_gewaa"
        with open(nf, 'wb') as new_file:
            new_file.write(downloaded_file)
        pyAesCrypt.encryptFile(nf, nf+".katies", ps)
        os.remove(nf)
        bot.send_message(message.chat.id, 'เรียบร้อย')
        bot.send_document(message.chat.id, open(nf+".katies", 'rb'), caption='นี่จ้า ไฟล์ที่เข้ารหัสแล้ว')
        os.remove(nf+".katies")
        ko = types.ReplyKeyboardMarkup()
        ko.add('เข้ารหัสไฟล์เพิ่ม', 'ไม่ดีกว่า')
        s = bot.send_message(message.chat.id, 'ต้องการอะไรอีกมั้ย', reply_markup=ko)
        bot.register_next_step_handler(s, encrypt_step)
    else:
        ch = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        ch.add('เข้ารหัสไฟล์', 'ถอดรหัสไฟล์', 'ย้อนกลับ')
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาด้วยนะจ๊ะ", reply_markup=ch)
        bot.register_next_step_handler(s, encrypt_step)

def decrypt_file(message):
    if message.document:
        bot.send_message(message.chat.id, "รอแป๊บนึง กำลังถอดรหัสไฟล์...")
        file = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file.file_path)
        nf = message.document.file_name
        ps = "@ewg1#ec@fewp_gewaa"
        with open(nf, 'wb') as new_file:
            new_file.write(downloaded_file)
        spl = os.path.splitext(nf)
        f_name = spl[0]
        pyAesCrypt.decryptFile(nf, f_name, ps)
        os.remove(nf)
        bot.send_message(message.chat.id, 'เรียบร้อย')
        bot.send_document(message.chat.id, open(f_name, 'rb'), caption='นี่จ้า ไฟล์ที่ถอดรหัสแล้ว')
        os.remove(f_name)
        ko = types.ReplyKeyboardMarkup()
        ko.add('ถอดรหัสไฟล์เพิ่ม', 'ไม่ดีกว่า')
        s = bot.send_message(message.chat.id, 'ต้องการอะไรอีกมั้ย', reply_markup=ko)
        bot.register_next_step_handler(s, encrypt_step)
    else:
        ch = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        ch.add('เข้ารหัสไฟล์', 'ถอดรหัสไฟล์', 'ย้อนกลับ')
        s = bot.send_message(message.chat.id, "ส่งไฟล์มาด้วยนะจ๊ะ", reply_markup=ch)
        bot.register_next_step_handler(s, encrypt_step)

def unlock_step(message):
    if message.text == 'ADB Driver':
        a = bot.send_message(message.chat.id, dp.adbin, parse_mode='HTML')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, unlock_step)
    elif message.text == 'โหลดไฟล์':
        lk = types.InlineKeyboardMarkup()
        l1 = types.InlineKeyboardButton('ADB Driver', url='google.com')
        l2 = types.InlineKeyboardButton('Mi Flash Unlock', url='google.com')
        lk.add(l1, l2)
        a = bot.send_message(message.chat.id, 'โหลดไฟล์ทั้งสองมาเก็บไว้ในคอมพิวเตอร์', reply_markup=lk, parse_mode='HTML')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, unlock_step)
    elif message.text == 'ปลดล็อกเครื่อง':
        a = bot.send_message(message.chat.id, dp.unlock, parse_mode='HTML')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, unlock_step)
    elif message.text == 'ย้อนกลับ':
        a = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, help_next_step)
    else:
        a = bot.send_message(message.chat.id, 'คำสั่งไม่ถูกต้อง', reply_markup=hmk)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, help_next_step)

def report(message : types.Message):
    mkup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    mkup.add('ส่งข้อความเพิ่ม', 'กลับสู่หน้าหลัก')
    bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n\n<b>Report to developer\n: </b>" + message.text , parse_mode='HTML')
    if "ควย" in message.text:
        f = bot.send_message(message.chat.id, 'ส่งข้อความแล้ว แต่ใช้คำสุภาพด้วยนะจ๊ะ', reply_markup=mkup)
        bot.register_next_step_handler(f, report1)
    elif "แมว" in message.text:
        ae = bot.send_message(message.chat.id, "ส่งข้อความสำเร็จ แต่อย่าให้รู้นะว่าเอาแมวไปปทำอะไร!")
        bot.register_next_step_handler(ae, report1)
    else:
        fe = bot.send_message(message.chat.id, "ส่งข้อความสำเร็จ!", reply_markup=mkup)
        bot.register_next_step_handler(fe, report1)

def report1(message : types.Message):
    if message.text == 'ส่งข้อความเพิ่ม':
        a = bot.send_message(message.chat.id, 'ว่ามาเลยย')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.register_next_step_handler(a, report)
    elif message.text == 'กลับสู่หน้าหลัก':
        a = bot.send_message(message.chat.id, 'เรียบร้อย!', reply_markup=hmk)
        bot.register_next_step_handler(a, help_next_step)
    else:
        a = bot.send_message(message.chat.id, "คำสั่งไม่ถูกต้อง", reply_markup=hmk)
        bot.register_next_step_handler(a, help_next_step)

def bank_photo(message):
    if message.text == 'SCB':
        d = bot.send_photo(message.chat.id, photo=open('photo/SCB.jpg', 'rb'))
        bot.register_next_step_handler(d, bank_photo)
    elif message.text == 'K Plus':
        p = bot.send_photo(message.chat.id, photo=open('photo/Kplus.jpg', 'rb'))
        bot.register_next_step_handler(p, bank_photo)
    elif message.text == 'ShopeePay':
        vy = bot.send_photo(message.chat.id, photo=open('photo/Shp.jpg', 'rb'))
        bot.register_next_step_handler(vy, bank_photo)
    elif message.text == 'True Wallet(1)':
        xy = bot.send_photo(message.chat.id, photo=open('photo/mnt.jpg', 'rb'))
        bot.register_next_step_handler(xy, bank_photo)
    elif message.text == 'True Wallet(2)':
        swed = bot.send_photo(message.chat.id, photo=open('photo/mnt.jpg', 'rb'))
        bot.register_next_step_handler(swed, bank_photo)
    elif message.text == '❌ Exit ❌':
        c = bot.send_message(message.chat.id, 'Done!', reply_markup=hmk)
        bot.register_next_step_handler(c, help_next_step)
    elif message.text == 'แน่นอน':
        c = bot.send_message(message.chat.id, 'Done!', reply_markup=hmk)
        bot.register_next_step_handler(c, help_next_step)
    else:
        ex = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        ex.add('แน่นอน')
        bot.send_message(message.chat.id, 'ว้าา ดูเหมือนคำสั่งจะไม่ถูกต้อง')
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        u = bot.send_message(message.chat.id, 'ต้องการกลับไปที่เมนูหลักมั้ย', reply_markup=ex)
        bot.register_next_step_handler(u, bank_photo)
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

class uprom_setup:
    def uprom(message):
        if message.text == 'ถัดไป':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False,resize_keyboard=True)
            markup.add('ถัดไป')
            a = bot.send_photo(message.chat.id, caption=dp.upfirst, photo=open('photo/srec.png', 'rb'), parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(a, uprom_setup.uprom1)
        elif message.text == 'ยกเลิก':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False,resize_keyboard=True)
            c = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
            bot.register_next_step_handler(c, help_next_step)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom1(message):
        if message.text == 'ถัดไป':
            a = bot.send_photo(message.chat.id, caption=dp.upfirst1,photo=open('photo/srec2.png', 'rb'), parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom2)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom2(message):
        if message.text == 'ถัดไป':
            bot.send_photo(message.chat.id, caption=dp.up_wipe, photo=open('photo/srec3.png', 'rb'), parse_mode='HTML')
            a = bot.send_photo(message.chat.id, caption=dp.up_wipex,photo=open('photo/srec4.png', 'rb'), parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom3)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom3(message):
        if message.text == 'ถัดไป':
            a = bot.send_photo(message.chat.id, caption=dp.up_in, photo=open('photo/srec1.png', 'rb'), parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom4)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom4(message):
        if message.text == 'ถัดไป':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            markup.add('ถัดไป')
            a = bot.send_photo(message.chat.id, caption=dp.up_in1, photo=open('photo/srec5.png', 'rb'), parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom5)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom5(message):
        if message.text == 'ถัดไป':
            a = bot.send_photo(message.chat.id, caption=dp.up_in2, photo=open('photo/srec6.png', 'rb'), parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom6)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')
    def uprom6(message):
        if message.text == 'ถัดไป':
            #bot.send_photo(message.chat.id, caption='รูปภาพยังไม่พร้อมใช้งาน', parse_mode='HTML')
            #a = bot.send_photo(message.chat.id, caption=dp.up_in3, parse_mode='HTML')
            bot.send_message(message.chat.id, 'รูปภาพยังไม่พร้อมใช้งานในขณะนี้', reply_markup=hmk)
            a = bot.send_message(message.chat.id, dp.up_in3)
            bot.register_next_step_handler(a, help_next_step)
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')

def note(message : types.Message):
    if message.text == 'mynote':
        bot.delete_message(message.chat.id, message.message_id)
        bt = types.InlineKeyboardMarkup(row_width=2)
        lst = types.InlineKeyboardButton('ดูรายชื่อบัญชี', callback_data='sma')
        lst1 = types.InlineKeyboardButton('ดูข้อมูลบัญชี', callback_data='smd')
        lst2 = types.InlineKeyboardButton('เพิ่มข้อมูล', callback_data='add')
        lst3 = types.InlineKeyboardButton('ลบข้อมูล', callback_data='del')
        lst4 = types.InlineKeyboardButton('จบการทำงาน', callback_data='exit')
        bt.add(lst, lst1, lst2, lst3, lst4)
        bot.send_message(message.chat.id, 'เลือกรายการที่ต้องการจ้า', reply_markup=bt)
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
    else:
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        k = bot.send_message(message.chat.id, "เหมือนมีคนใส่รหัสไม่ถูกน้าา", reply_markup=hmk)
        bot.register_next_step_handler(k, help_next_step)

def mytab(message):
    txt = message.text
    if txt == 'bbo':
        with open('photo/mytab.png', 'rb') as file:
            bot.delete_message(message.chat.id, message.message_id)
            s = bot.send_message(message.chat.id, 'รหัสถูกต้อง รอแป๊บ', reply_markup=hmk)
            bot.send_photo(message.chat.id, file)
            bot.register_next_step_handler(s, help_next_step)
            print("---> sent photo to", message.from_user.first_name, "succeed")
    else:
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        c = bot.send_message(message.chat.id, 'ใส่ไม่ถูก ไม่ให้หรอก', reply_markup=hmk)
        bot.register_next_step_handler(c, help_next_step)
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

def help_tr_step(message):
    Help = message.text
    if (Help == 'Help'):
        j = bot.reply_to(message, dp.trhelp, reply_markup=hmk, parse_mode='HTML')
        bot.register_next_step_handler(j, help_next_step)
    else:
        o = bot.send_message(message.chat.id, 'คำสั่งไม่ถูกต้อง', reply_markup=hmk)
        bot.register_next_step_handler(o, help_next_step)
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

def stop(message: types.Message):
    global freeid

    if message.chat.id in users:
        txt = message.text
        
    if txt == 'ยืนยัน ✔':
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.send_message(message.chat.id, 'กำลังออกจากระบบ...', reply_markup=hd)
        bot.send_message(users[message.chat.id], 'ออกจากระบบเสร็จสิ้น โปรดอย่าได้เจอกับอีกเลย😉')

        del users[users[message.chat.id]]
        del users[message.chat.id]

        print(message.chat.id, "is logout")
        print(users, freeid)
    elif message.chat.id == freeid:
        bot.send_message(message.chat.id, 'กำลังออกจากระบบ...')
        freeid = None

        print(users, freeid)
    else:
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.send_message(message.chat.id, 'การออกจากระบบล้มเหลว 😐', reply_markup=hd)
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

#-------------------------------- Inline Markup-------------------------------------------#
#-------------------------------- Inline Markup-------------------------------------------#
#-------------------------------- Inline Markup-------------------------------------------#

def next_setup_devices(message):
    txt = message.text
    if (txt == 'vayu'):
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romva")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        mkup.add(EU, GR, GB, Ex)
        text = "<b>Poco X3 Pro</b> - เลือกเมนูที่ต้องการจ้า"
        bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
    elif (txt == 'lime'):
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romli")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reli")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerli")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        #mkup.add(EU, GR, GB, Ex)
        #text = "<b>Redmi 9t/Poco M3</b> - เลือกเมนูที่ต้องการจ้า"
        text = "ยังไม่เปิดใช้งาน"
        #bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
        bot.send_message(message.chat.id, text)
    elif (txt == 'mojito'):
        mkup = types.InlineKeyboardMarkup(row_width=2)
        A = types.InlineKeyboardButton("ROM", callback_data="rommo")
        B = types.InlineKeyboardButton("RECOVER", callback_data="rec")
        Z = types.InlineKeyboardButton("KERNEL", callback_data="kermo")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        #mkup.add(A, B, Z, Ex)
        #text = "<b>Redmi Note 10</b> - เลือกเมนูที่ต้องการจ้า"
        text = "ยังไม่เปิดใช้งาน"
        #bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
        bot.send_message(message.chat.id, text)
    elif txt == '⬅️ ย้อนกลับ':
        k = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bot.register_next_step_handler(k, help_next_step)
    else:
        bot.reply_to(message, '❌คำสั่งไม่ถูกต้อง❌')
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

# ---------------------------------- Poco X3 Pro --------------------------------------------------#
# ---------------------------------- Poco X3 Pro --------------------------------------------------#
# ---------------------------------- Poco X3 Pro --------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'romva')
def rom_vayu_se(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("MIUI", callback_data="MIUI-va")
        B = types.InlineKeyboardButton("Pure Android", callback_data="Pure-va")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
        mkup.add(A,B,Z)
        text = "รอม <b>MIUI</b> หรือ <b>Pure Andriod</b> เอ่ย"
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------- MIUI ROM --------------------------------------------------------#
#------------------------------------------- MIUI ROM --------------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'MIUI-va')
def rom_vayu_mi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("EU", callback_data="EU_va")
        B = types.InlineKeyboardButton("GR", callback_data="GR_va")
        C = types.InlineKeyboardButton("MMX", callback_data="MX_va")
        D = types.InlineKeyboardButton("Global", callback_data="GB_va")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="romva")
        mkup.add(A,B,C,D,Z)
        bot.edit_message_text(dp.x3p, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#-------------------------------------------- EU ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'EU_va')
def rom_vayu_eu(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.7.0.RJUMIXM_v12-11.zip/download') 
        B = types.InlineKeyboardButton("V12.5.5", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.5.0.RJUMIXM_v12-11.zip/download')
        C = types.InlineKeyboardButton("V12.5.4", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.4.0.RJUMIXM_v12-11.zip/download')
        D = types.InlineKeyboardButton("V12.5.3", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.3.0.RJUMIXM_v12-11.zip/download')
        E = types.InlineKeyboardButton("V12.5.2", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.2.0.RJUMIXM_v12-11.zip/download')
        F = types.InlineKeyboardButton("V12.5.1", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.1.0.RJUMIXM_v12-11.zip/download')
        G = types.InlineKeyboardButton("V12.0.6", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.0.6.0.RJUMIXM_v12-11.zip/download')
        H = types.InlineKeyboardButton("V12.0.4", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.0.4.0.RJUMIXM_v12-11.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, G, H, Z)
        bot.edit_message_text(dp.x3peu, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#-------------------------------------------- GR ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GR_va')
def rom_vayu_gr(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='google.com') 
        B = types.InlineKeyboardButton("V12.5.5", url='google.com')
        C = types.InlineKeyboardButton("V12.5.4", url='google.com')
        D = types.InlineKeyboardButton("V12.5.3", url='google.com')
        E = types.InlineKeyboardButton("V12.5.2", url='google.com')
        F = types.InlineKeyboardButton("V12.5.1", url='google.com')
        G = types.InlineKeyboardButton("V12.0.6", url='google.com')
        H = types.InlineKeyboardButton("V12.0.4", url='google.com')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, G, H, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>----------   GR ROM   ----------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#----------------------------------------- MMX MIUI -------------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'MX_va')
def rom_vayu_mx(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='https://androidfilehost.com/?fid=7161016148664849871') 
        B = types.InlineKeyboardButton("V12.5.5", url='https://androidfilehost.com/?fid=7161016148664825201')
        C = types.InlineKeyboardButton("V12.5.4", url='https://androidfilehost.com/?fid=7161016148664797557')
        D = types.InlineKeyboardButton("V12.5.3", url='https://androidfilehost.com/?fid=7161016148664782181')
        E = types.InlineKeyboardButton("V12.5.2", url='https://androidfilehost.com/?fid=14943124697586352735')
        F = types.InlineKeyboardButton("V12.5.1", url='https://androidfilehost.com/?fid=14943124697586345571')
        G = types.InlineKeyboardButton("V12.0.6", url='https://androidfilehost.com/?fid=2188818919693787302')
        H = types.InlineKeyboardButton("V12.0.4", url='https://androidfilehost.com/?fid=2188818919693784819')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, G, H, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>----------   MMX ROM   ----------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#-------------------------------------------- GB ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GB_va')
def rom_vayu_gb(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1) 
        A = types.InlineKeyboardButton("V12.5.5", url='https://mifirm.net/download/5854')
        B = types.InlineKeyboardButton("V12.5.4", url='https://mifirm.net/download/5667')
        C = types.InlineKeyboardButton("V12.5.3", url='https://mifirm.net/download/5581')
        D = types.InlineKeyboardButton("V12.5.2", url='https://mifirm.net/download/5346')
        E = types.InlineKeyboardButton("V12.0.6", url='https://mifirm.net/download/5105')
        F = types.InlineKeyboardButton("V12.0.4", url='https://mifirm.net/download/4922')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>---------   Global ROM   ---------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------- Pure ROM --------------------------------------------------------#
#------------------------------------------- Pure ROM --------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'Pure-va')
def rom_vayu_aso(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("OFFICIAL", callback_data="OF_va")
        B = types.InlineKeyboardButton("UNOFFICIAL", callback_data="UOF_va")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="romva")
        mkup.add(A,B,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n\n"
        "     <b>---------   Pure Andriod   ---------</b>"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ Official -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'OF_va')
def rom_vayu_ofi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("AncientOS", url='https://www.pling.com/p/1606146')
        B = types.InlineKeyboardButton("AICP v16.1 A11 Vanilla", url='https://dwnld.aicp-rom.com/device/vayu/WEEKLY/aicp_vayu_r-16.1-WEEKLY-20211203.zip')
        C = types.InlineKeyboardButton("ArrowOS", url='https://arrowos.net/download/vayu')
        D = types.InlineKeyboardButton("Derpfest A12 Gapps", url='https://sourceforge.net/projects/derpfest/files/vayu/DerpFest-12-Official-Shion-vayu-20211203.zip/download')
        E = types.InlineKeyboardButton("DotOS v5.2.1 A11",url='https://www.droidontime.com/devices/vayu')
        G = types.InlineKeyboardButton("LineageOs v18.1 A11 Vanilla", url='https://mirrorbits.lineageos.org/full/vayu/20211203/lineage-18.1-20211203-nightly-vayu-signed.zip')
        H = types.InlineKeyboardButton("Pixel Ex Beta A12 Gapps", url='https://download.pixelexperience.org/vayu')
        I = types.InlineKeyboardButton("XPerience v16.0 A12", url='https://sourceforge.net/projects/xperience-aosp/files/vayu/16/nightly/xperience-16.0.0-20211202-NIGHTLY-vayu.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Pure-va")
        mkup.add(A,B,C,D,E,G,H,I,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "    <b>--------   Pure Andriod   --------</b>\n"
        "      <b>----------   Officail   ----------</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ UnOfficial -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'UOF_va')
def rom_vayu_unofi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        J = types.InlineKeyboardButton("CipherOS v2.0 A12 Gapps", url='https://drive.google.com/file/d/1y5ZLxzIzDrG_uFABibI_4CTThGZsdeEO/view')
        F = types.InlineKeyboardButton("EVO 6.0 A12 Gapps", url='https://sourceforge.net/projects/gengkapak/files/ROM/vayu/EvolutionX/12/evolution_vayu-ota-sd1a.210817.036.a8-11300236-unofficial-unsigned.zip/download')
        G = types.InlineKeyboardButton("LineageOs v19.0 A12 Vanilla", url='https://sourceforge.net/projects/other007/files/lineage-19.0-20211207-UNOFFICIAL-vayu.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Pure-va")
        mkup.add(F,G,J,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "    <b>--------   Pure Andriod   --------</b>\n"
        "      <b>----------   Unofficail   ----------</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ Recovery -------------------------------------------------------#
#------------------------------------------ Recovery -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'reva')
def rom_vayu_rec(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("TWRP", url='https://dl.twrp.me/vayu/twrp-3.6.0_11-0-vayu.img')
        B = types.InlineKeyboardButton("Orange Fox", url='https://us-dl.orangefox.download/61925ad3df607d814a41854e')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
        mkup.add(A,B,Z)
        text = (
            "<b>------------     Poco X3 Pro     ------------</b>\n"
            "       <b>------------  Recovery  ------------</b>     "
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#------------------------------------------ Kernels -------------------------------------------------------#
#------------------------------------------ Kernels -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'kerva')
def rom_vayu_rec(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
        mkup.add(Z)
        text = (
            "ยังไม่อัพเดต"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

# ---------------------------------- Redmi 9t --------------------------------------------------#
# ---------------------------------- Redmi 9t --------------------------------------------------#
# ---------------------------------- Redmi 9t --------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'romli')
def rom_vayu_se(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("MIUI", callback_data="MIUI-li")
        B = types.InlineKeyboardButton("Pure Android", callback_data="Pure-li")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backli")
        mkup.add(Z)
        text = "ยังไม่อัพเดต"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------- MIUI ROM --------------------------------------------------------#
#------------------------------------------- MIUI ROM --------------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'MIUI-li')
def rom_vayu_mi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("EU", callback_data="EU_li")
        B = types.InlineKeyboardButton("GR", callback_data="GR_li")
        C = types.InlineKeyboardButton("MMX", callback_data="MX_li")
        D = types.InlineKeyboardButton("Global", callback_data="GB_li")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="romli")
        mkup.add(A,B,C,D,Z)
        text = (
            "Redmi 9t"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#-------------------------------------------- EU ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'EU_li')
def rom_vayu_eu(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.7.0.RJUMIXM_v12-11.zip/download') 
        B = types.InlineKeyboardButton("V12.5.5", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.5.0.RJUMIXM_v12-11.zip/download')
        C = types.InlineKeyboardButton("V12.5.4", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.4.0.RJUMIXM_v12-11.zip/download')
        D = types.InlineKeyboardButton("V12.5.3", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.3.0.RJUMIXM_v12-11.zip/download')
        E = types.InlineKeyboardButton("V12.5.2", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.2.0.RJUMIXM_v12-11.zip/download')
        F = types.InlineKeyboardButton("V12.5.1", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.5.1.0.RJUMIXM_v12-11.zip/download')
        G = types.InlineKeyboardButton("V12.0.6", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.0.6.0.RJUMIXM_v12-11.zip/download')
        H = types.InlineKeyboardButton("V12.0.4", url='https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/xiaomi.eu_multi_POCOX3Pro_V12.0.4.0.RJUMIXM_v12-11.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-li")
        #mkup.add(A, B, C, D, E, F, G, H, Z)
        mkup.add(Z)
        bot.edit_message_text("ยังไม่อัพเดต", call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#-------------------------------------------- GR ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GR_li')
def rom_vayu_gr(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='google.com') 
        B = types.InlineKeyboardButton("V12.5.5", url='google.com')
        C = types.InlineKeyboardButton("V12.5.4", url='google.com')
        D = types.InlineKeyboardButton("V12.5.3", url='google.com')
        E = types.InlineKeyboardButton("V12.5.2", url='google.com')
        F = types.InlineKeyboardButton("V12.5.1", url='google.com')
        G = types.InlineKeyboardButton("V12.0.6", url='google.com')
        H = types.InlineKeyboardButton("V12.0.4", url='google.com')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, G, H, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>----------   GR ROM   ----------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#----------------------------------------- MMX MIUI -------------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'MX_li')
def rom_vayu_mx(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("V12.5.7", url='https://androidfilehost.com/?fid=7161016148664849871') 
        B = types.InlineKeyboardButton("V12.5.5", url='https://androidfilehost.com/?fid=7161016148664825201')
        C = types.InlineKeyboardButton("V12.5.4", url='https://androidfilehost.com/?fid=7161016148664797557')
        D = types.InlineKeyboardButton("V12.5.3", url='https://androidfilehost.com/?fid=7161016148664782181')
        E = types.InlineKeyboardButton("V12.5.2", url='https://androidfilehost.com/?fid=14943124697586352735')
        F = types.InlineKeyboardButton("V12.5.1", url='https://androidfilehost.com/?fid=14943124697586345571')
        G = types.InlineKeyboardButton("V12.0.6", url='https://androidfilehost.com/?fid=2188818919693787302')
        H = types.InlineKeyboardButton("V12.0.4", url='https://androidfilehost.com/?fid=2188818919693784819')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, G, H, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>----------   MMX ROM   ----------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#-------------------------------------------- GB ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GB_li')
def rom_vayu_gb(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1) 
        A = types.InlineKeyboardButton("V12.5.5", url='https://mifirm.net/download/5854')
        B = types.InlineKeyboardButton("V12.5.4", url='https://mifirm.net/download/5667')
        C = types.InlineKeyboardButton("V12.5.3", url='https://mifirm.net/download/5581')
        D = types.InlineKeyboardButton("V12.5.2", url='https://mifirm.net/download/5346')
        E = types.InlineKeyboardButton("V12.0.6", url='https://mifirm.net/download/5105')
        F = types.InlineKeyboardButton("V12.0.4", url='https://mifirm.net/download/4922')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
        mkup.add(A, B, C, D, E, F, Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "       <b>---------   Global ROM   ---------</b>\n\n"

        "เลือกเวอร์ชันที่ต้องการได้เลยย 😉"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------- Pure ROM --------------------------------------------------------#
#------------------------------------------- Pure ROM --------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'Pure-li')
def rom_vayu_aso(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("OFFICIAL", callback_data="OF_va")
        B = types.InlineKeyboardButton("UNOFFICIAL", callback_data="UOF_va")
        Z = types.InlineKeyboardButton("<<= Back", callback_data="romva")
        mkup.add(A,B,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n\n"
        "     <b>---------   Pure Andriod   ---------</b>"
        )
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ Official -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'OF_li')
def rom_vayu_ofi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A = types.InlineKeyboardButton("AncientOS", url='https://www.pling.com/p/1606146')
        B = types.InlineKeyboardButton("AICP v16.1 A11 Vanilla", url='https://dwnld.aicp-rom.com/device/vayu/WEEKLY/aicp_vayu_r-16.1-WEEKLY-20211203.zip')
        C = types.InlineKeyboardButton("ArrowOS", url='https://arrowos.net/download/vayu')
        D = types.InlineKeyboardButton("Derpfest A12 Gapps", url='https://sourceforge.net/projects/derpfest/files/vayu/DerpFest-12-Official-Shion-vayu-20211203.zip/download')
        E = types.InlineKeyboardButton("DotOS v5.2.1 A11",url='https://www.droidontime.com/devices/vayu')
        G = types.InlineKeyboardButton("LineageOs v18.1 A11 Vanilla", url='https://mirrorbits.lineageos.org/full/vayu/20211203/lineage-18.1-20211203-nightly-vayu-signed.zip')
        H = types.InlineKeyboardButton("Pixel Ex Beta A12 Gapps", url='https://download.pixelexperience.org/vayu')
        I = types.InlineKeyboardButton("XPerience v16.0 A12", url='https://sourceforge.net/projects/xperience-aosp/files/vayu/16/nightly/xperience-16.0.0-20211202-NIGHTLY-vayu.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Pure-va")
        mkup.add(A,B,C,D,E,G,H,I,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "    <b>--------   Pure Andriod   --------</b>\n"
        "      <b>----------   Officail   ----------</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ UnOfficial -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'UOF_li')
def rom_vayu_unofi(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        J = types.InlineKeyboardButton("CipherOS v2.0 A12 Gapps", url='https://drive.google.com/file/d/1y5ZLxzIzDrG_uFABibI_4CTThGZsdeEO/view')
        F = types.InlineKeyboardButton("EVO 6.0 A12 Gapps", url='https://sourceforge.net/projects/gengkapak/files/ROM/vayu/EvolutionX/12/evolution_vayu-ota-sd1a.210817.036.a8-11300236-unofficial-unsigned.zip/download')
        G = types.InlineKeyboardButton("LineageOs v19.0 A12 Vanilla", url='https://sourceforge.net/projects/other007/files/lineage-19.0-20211207-UNOFFICIAL-vayu.zip/download')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Pure-va")
        mkup.add(F,G,J,Z)
        text = (
        "<b>------------     Poco X3 Pro     ------------</b>\n"
        "    <b>--------   Pure Andriod   --------</b>\n"
        "      <b>----------   Unofficail   ----------</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ Recovery -------------------------------------------------------#
#------------------------------------------ Recovery -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'reli')
def rom_vayu_rec(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        A= types.InlineKeyboardButton("TWRP", url='https://dl.twrp.me/vayu/twrp-3.6.0_11-0-vayu.img')
        B = types.InlineKeyboardButton("Orange Fox", url='https://us-dl.orangefox.download/61925ad3df607d814a41854e')
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
        mkup.add(A,B,Z)
        text = (
            "<b>------------     Poco X3 Pro     ------------</b>\n"
            "       <b>------------  Recovery  ------------</b>     "
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
#------------------------------------------ Kernels -------------------------------------------------------#
#------------------------------------------ Kernels -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'kerli')
def rom_vayu_rec(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=1)
        Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
        mkup.add(Z)
        text = (
            "ยังไม่อัพเดต"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ Home Menu -----------------------------------------------------#
#------------------------------------------ Home Menu -----------------------------------------------------#
#------------------------------------------ Home Menu -----------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'Backva')
def a_choosen(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romva")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        mkup.add(EU, GR, GB, Ex)
        text = "<b>Poco X3 Pro</b> - เลือกเมนูที่ต้องการจ้า"
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'Backli')
def b_choosen(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romva")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        mkup.add(EU, GR, GB, Ex)
        text = "<b>Redmi 9t/Poco M3</b> - เลือกเมนูที่ต้องการจ้า"
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'Backmo')
def c_choosen(call):
    if call.message.chat.id in users:
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romva")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
        Ex = types.InlineKeyboardButton("Exit", callback_data="end")
        mkup.add(EU, GR, GB, Ex)
        text = "<b>Redmi Note 10</b> - เลือกเมนูที่ต้องการจ้า"
        bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)
    
#------------------------------------------ End Command -------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'end')
def end(call):
    if call.message.chat.id in users:
        bot.edit_message_text('สำเร็จ!', call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text('ไม่รู้จักคร้าา ยืนยันตัวตนก่อน จิ้ม > /auth', call.message.chat.id, call.message.message_id)

#------------------------------------------ End Inline -----------------------------------------------------#
#------------------------------------------ End Inline -----------------------------------------------------#
#------------------------------------------ End Inline -----------------------------------------------------#

#------------------------------------------ Note --------------------------------------------#
#------------------------------------------ Note --------------------------------------------#
#------------------------------------------ Note --------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'sma') # Show my account
def showdata(call : types.CallbackQuery):
    if call.message.chat.id in users:
        bt = types.InlineKeyboardMarkup()
        lst = types.InlineKeyboardButton('ย้อนกลับ', callback_data='Back')
        bt.add(lst)
        cur.execute("SELECT Name FROM Face")
        ps = ""
        for row in cur.fetchall():
            row = row[0]
            ps = ps + '- ' + row + '\n'
        text = "รายการบัญชี :\n{ls}".format(ls=ps)
        bot.edit_message_text(str(text), call.message.chat.id, call.message.message_id, reply_markup=bt)
        cnx.commit()
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'smd') # Show my data
def showdata2(call : types.CallbackQuery):
    if call.message.chat.id in users:
        cur.execute("SELECT Name FROM Face")
        ps = ""
        for row in cur.fetchall():
            row = row[0]
            ps = ps + '- ' + row + '\n'
        text = "อยากดูรายการบัญชีไหนเอ่ย\n\nรายการบัญชี :\n{ls}".format(ls=ps)
        s = bot.edit_message_text(str(text), call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(s, showdata3)
        bot.answer_callback_query(call.id)
        cnx.commit()
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)

def showdata3(message):
    bc = types.InlineKeyboardMarkup()
    bc.add(types.InlineKeyboardButton('Back', callback_data='Back'))
    cur.execute("SELECT Name FROM Face WHERE Name = '{text}'".format(text=message.text))
    cr = cur.fetchall()
    if message.text in str(cr):
        cur.execute("SELECT * FROM Face WHERE Name = '{text}'".format(text=message.text))
        cr = cur.fetchall()
        bot.send_message(message.chat.id, 'ข้อมูลบัญชี\n\nName: <b>{Name}</b>\nEmail: <b>{Email}</b>\nPassword: <tg-spoiler>{Password}</tg-spoiler>'.format(Name=cr[0][1], Email=cr[0][2], Password=cr[0][3]), parse_mode='HTML', reply_markup=bc)
    else:
        bot.send_message(message.chat.id, 'ไม่เจอชื่อ {text} นี้ในระบบ'.format(text=message.text), reply_markup=bc)

@bot.callback_query_handler(func=lambda call: call.data == 'add') # Add data
def add(call : types.CallbackQuery):
    if call.message.chat.id in users:
        text = """ส่งรหัสที่ต้องการเพิ่มได้เลยย\n\nให้ส่งมาแบบนี้นะ \n'ชื่อบัญชี', 'อีเมล หรือ ชื่อผู้ใช้', 'รหัสผ่าน'\n\n<b>ตัวอย่าง</b>\n<b>Myacc</b> <b>email@ex.com</b> <b>passwd10</b>"""
        s = bot.edit_message_text(str(text), call.message.chat.id, call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler(s, add2)
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)

def add2(message):
    mmsg = message.text.split(' ')
    bc = types.InlineKeyboardMarkup()
    bc.add(types.InlineKeyboardButton('Back', callback_data='Back'))
    if len(mmsg) == 3:
        cur.execute("SELECT Name FROM Face")
        cr = cur.fetchall()
        if message.text in str(cr):
            bot.send_message(message.chat.id, 'มีชื่อบัญชีนี้ในระบบอยู่เด้อ เอาชื่อใหม่', reply_markup=bc)
        else:
            cur.execute("INSERT INTO Face (Name, Email, Password) VALUES ('{Name}', '{Email}', '{Password}')".format(Name=mmsg[0], Email=mmsg[1], Password=mmsg[2]))
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'เพิ่มข้อมูลเรียบร้อย', reply_markup=bc)
            cnx.commit()
    else:
        bot.send_message(message.chat.id, 'รูปแบบไม่ถูกต้อง อ่านบ่เกาะว่า', reply_markup=bc)

@bot.callback_query_handler(func=lambda call: call.data == 'del')
def del2(call : types.CallbackQuery):
    if call.message.chat.id in users:
        cur.execute("SELECT Name FROM Face")
        ps = ""
        for row in cur.fetchall():
            row = row[0]
            ps = ps + '- ' + row + '\n'
        text = "อยากลบบัญชีไหนเอ่ย\n\nรายการบัญชี :\n{ls}".format(ls=ps)
        s = bot.edit_message_text(str(text), call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(s, del3)
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)

def del3(message):
    bc = types.InlineKeyboardMarkup()
    bc.add(types.InlineKeyboardButton('Back', callback_data='Back'))
    cur.execute("SELECT Name FROM Face")
    cr = cur.fetchall()
    if message.text in str(cr):
        cur.execute("DELETE FROM Face WHERE Name = '{text}'".format(text=message.text))
        cur.execute("alter table Face auto_increment = 1")
        bot.send_message(message.chat.id, 'ลบเรียบร้อย', reply_markup=bc)
    else:
        bot.send_message(message.chat.id, 'ลบ <b>{text}</b> ไม่ได้ ไม่เจอในระบบ'.format(text=message.text), reply_markup=bc, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'exit')
def endin(call : types.CallbackQuery):
    if call.message.chat.id in users:
        bot.edit_message_text('ลาก่อน', call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'Back')
def back(call : types.CallbackQuery):
    if call.message.chat.id in users:
        bt = types.InlineKeyboardMarkup(row_width=2)
        lst = types.InlineKeyboardButton('ดูรายชื่อบัญชี', callback_data='sma')
        lst1 = types.InlineKeyboardButton('ดูข้อมูลบัญชี', callback_data='smd')
        lst2 = types.InlineKeyboardButton('เพิ่มข้อมูล', callback_data='add')
        lst3 = types.InlineKeyboardButton('ลบข้อมูล', callback_data='del')
        lst4 = types.InlineKeyboardButton('จบการทำงาน', callback_data='exit')
        bt.add(lst, lst1, lst2, lst3, lst4)
        bot.edit_message_text('เลือกรายการที่ต้องการจ้า', call.message.chat.id, call.message.message_id, reply_markup=bt)
        bot.answer_callback_query(call.id)
    else:
        bot.edit_message_text('ยืนยันตัวตนก่อน จิ้ม -> /auth', call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['ver'])
def version_bot(message):
    if message.chat.id in users:
        bot.send_message(message.chat.id, dp.ver, parse_mode='HTML')
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.chat.id, message.from_user.first_name))
    else:
        bot.send_message(message.chat.id , 'ยืนยันตัวตนก่อนจ้า จิ้ม -> /auth')
    print(message.from_user.first_name, " : ", message.text)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.chat.id in users:
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
        bt2.send_message(tk.admin, text = "<b>User </b> : " + message.from_user.full_name + "\n<b>User ID </b>: " + str(message.chat.id) + "\n<b>Text : </b>" + message.text , parse_mode='HTML')
        bot.reply_to(message, 'อย่ามาจิงฮิงงจองฮองแถวนี้นะ พิมพ์ /help ก่อน', parse_mode='HTML', reply_markup=hd)
    else:
        bot.send_message(message.chat.id , 'ยืนยันตัวตนก่อนจ้า จิ้ม -> /auth',reply_markup=hd)
    print(message.from_user.first_name, " : ", message.text)

bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())