#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import description as dp
import tk
import telebot, logging, sys
import mysql.connector
import pyAesCrypt
from telebot import custom_filters, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
print('hi')
#-----------------------------------------------------------------------------#
"Variable"
bot = telebot.TeleBot(tk.kati)
bt2 = telebot.TeleBot(tk.admin)
hd = ReplyKeyboardRemove()
sys.tracebacklimit = 0
#-----------------------------------------------------------------------------#
"Database"
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="04041965z",
    database="thxmz")
cur = cnx.cursor()
#-----------------------------------------------------------------------------#

"Path Reply markup Help_Command"
hmk = types.ReplyKeyboardMarkup(one_time_keyboard=False)
hmk.row_width = 3
hmk.add('Getapps', 'รอม', 'โค้ดเนม', 'trCamera', 'Messenger', 'ปลดล็อกเครื่อง', 'Magisk', 'อัพเดตรอม', 'อัพเดตโหมดกู้คืน', 'ตารางเรียน', 'โน้ต', 'คำสั่งถัดไป')
hmk.add('โอนเงิน 💸', 'เข้ารหัสไฟล์', 'รายงาน/แนะนำ')
hmk.add('ออกจากระบบ')

freeid = None
users = {}

print('Bot is started......')
print("If you want to exit, You can press Ctrl + C to exit evertime :) ")

@bot.message_handler(commands=['start'])
def start(message):
    freeid = message.chat.id
    bot.send_message(message.chat.id, "ดีจ้า ยืนยันตัวตนก่อน จิ้ม > /auth", parse_mode='HTML', reply_markup=hmk)
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.chat.id, message.from_user.first_name))
    print('User using bot now is : ', message.from_user.first_name, ({freeid}))
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
            bot.send_message(message.chat.id, 'ยืนยัวตนตัวสำเร็จ!')
            bot.send_message(freeid, dp.start.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None
            
        print(users, freeid)
    else:
        bot.send_message(message.chat.id, 'ยืนยันสำเร็วแล้ว คุณ <b>{name}!</b>'.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)
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
                bot.send_message(message.chat.id, 'ยืนยัวตนตัวสำเร็จ!', reply_markup=hd)
                bot.send_message(freeid, dp.start.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)

                users[freeid] = message.chat.id 
                users[message.chat.id] = freeid
                freeid = None

                print(users, freeid)
        else:
            bot.send_message(message.chat.id, 'ยืนยันสำเร็วแล้ว คุณ <b>{name}!</b>'.format(name=message.from_user.first_name), parse_mode='HTML', reply_markup=hd)
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
    else:
        bot.send_message(message.chat.id, 'Error Bug. Please contact to dev.')
    print(message.from_user.first_name, " : ", message.text)

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.chat.id in users:
        msg = bot.reply_to(message, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bot.register_next_step_handler(msg, help_next_step)
    else:
        bot.send_message(message.chat.id , 'ยืนยันตัวตนก่อนจ้า จิ้ม -> /auth')
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
            bot.register_next_step_handler(h, help_next_step)
        elif (textuser == 'รอม'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 3
            markup.add('vayu', 'lime', 'mojito', '⬅️ ย้อนกลับ')
            msg = bot.reply_to(message, 'รุ่นอะไรจ๊ะ', reply_markup=markup)
            bot.register_next_step_handler(msg, next_setup_devices)
        elif (textuser == 'โค้ดเนม'):
            y = bot.reply_to(message, dp.codename, reply_markup=hmk ,parse_mode='HTML')
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
            bot.register_next_step_handler(msg, help_tr_step)
        elif (textuser == ('Messenger')):
            a = bot.reply_to(message, dp.Messenger, reply_markup=hmk, parse_mode='HTML')
            bot.register_next_step_handler(a, help_next_step)
        elif (textuser == ('ปลดล็อกเครื่อง')):
            pl = bot.reply_to(message, dp.unlockBD, parse_mode='HTML',reply_markup=hmk)
            bot.register_next_step_handler(pl, help_next_step)
        elif (textuser == ('Magisk')):
            i = bot.send_message(message.chat.id, dp.Magisk, parse_mode='HTML', disable_web_page_preview=True, reply_markup=hmk)
            bot.register_next_step_handler(i, help_next_step)
        elif (textuser == ('อัพเดตรอม')):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            markup.add('ถัดไป')
            a = bot.reply_to(message, dp.textup, reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(a, uprom_setup.uprom)
        elif (textuser == ('คำสั่งถัดไป')):
            pl = bot.reply_to(message, 'ว่าง ไม่รู้จะใส่อะไรดี', parse_mode='HTML',reply_markup=hmk)
            bot.register_next_step_handler(pl, help_next_step)
        elif (textuser == ('อัพเดตโหมดกู้คืน')):
            pl = bot.reply_to(message, 'ว่าง ไม่รู้จะใส่อะไรดี', parse_mode='HTML',reply_markup=hmk)
            bot.register_next_step_handler(pl, help_next_step)
        elif (textuser == ('โอนเงิน 💸')):
            mk = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            mk.add('SCB', 'K Plus')
            mk.add('ShopeePay')
            mk.add('True Wallet(1)', 'True Wallet(2)')
            mk.add('❌ Exit ❌')
            a = bot.send_message(message.chat.id, dp.money, reply_markup=mk ,parse_mode='HTML')
            bot.register_next_step_handler(a, bank_photo)

        # Password
        elif (textuser == ('ตารางเรียน')):
            a = bot.reply_to(message, 'ใส่รหัสก่อน', reply_markup=hd)
            bot.register_next_step_handler(a, mytab)
        
        elif (textuser == 'ออกจากระบบ'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 1
            markup.add('ยืนยัน ✔', 'ยกเลิก ❌')
            msg = bot.reply_to(message, "โปรดจิ้ม 'ยืนยัน' ที่ช่องด้านล่าง เพื่อยืนยันการออกจากระบบ", reply_markup=markup)
            bot.register_next_step_handler(msg, stop)
        else:
            bot.reply_to(message, "คำสั่งไม่ถูกต้อง")
        logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.warning((message.from_user.first_name, message.text))
        print(message.from_user.first_name, " : ", message.text)

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
            bot.send_photo(message.chat.id, caption=dp.up_in2, photo=open('photo/srec6.png', 'rb'), parse_mode='HTML')
        else:
            bot.reply_to(message, 'คำสั่งไม่ถูกต้อง')

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
        mkup.add(EU, GR, GB)
        text = "<b>Poco X3 Pro</b> - เลือกเมนูที่ต้องการจ้า"
        bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
    elif (txt == 'lime'):
        mkup = types.InlineKeyboardMarkup(row_width=2)
        EU = types.InlineKeyboardButton("ROM", callback_data="romli")
        GR = types.InlineKeyboardButton("RECOVER", callback_data="reli")
        GB = types.InlineKeyboardButton("KERNEL", callback_data="kerli")
        mkup.add(EU, GR, GB)
        text = "<b>Redmi 9t/Poco M3</b> - เลือกเมนูที่ต้องการจ้า"
        bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
    elif (txt == 'mojito'):
        mkup = types.InlineKeyboardMarkup(row_width=2)
        A = types.InlineKeyboardButton("ROM", callback_data="rommo")
        B = types.InlineKeyboardButton("RECOVER", callback_data="rec")
        Z = types.InlineKeyboardButton("KERNEL", callback_data="kermo")
        mkup.add(A,B,Z)
        text = "<b>Redmi Note 10</b> - เลือกเมนูที่ต้องการจ้า"
        bot.send_message(message.chat.id, text, reply_markup=mkup, parse_mode='HTML')
    elif txt == '⬅️ ย้อนกลับ':
        k = bot.send_message(message.chat.id, 'ต้องการอะไรเอ่ย', reply_markup=hmk)
        bot.register_next_step_handler(k, help_next_step)
    else:
        bot.reply_to(message, '❌คำสั่งไม่ถูกต้อง❌')
    logging.basicConfig(filename='user.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.warning((message.from_user.first_name, message.text))
    print(message.from_user.first_name, " : ", message.text)

# ---------------------------------- Poco X3 Pro Rom List --------------------------------------------------------------------#
# ---------------------------------- Poco X3 Pro Rom List --------------------------------------------------------------------#
# ---------------------------------- Poco X3 Pro Rom List --------------------------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'romva')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    A = types.InlineKeyboardButton("MIUI", callback_data="MIUI-va")
    B = types.InlineKeyboardButton("Pure Android", callback_data="Pure-va")
    Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
    mkup.add(A,B,Z)
    text = "รอม <b>MIUI</b> หรือ <b>Pure Andriod</b> เอ่ย"
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------- MIUI ROM --------------------------------------------------------#
#------------------------------------------- MIUI ROM --------------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'MIUI-va')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    A= types.InlineKeyboardButton("EU", callback_data="EU_va")
    B = types.InlineKeyboardButton("GR", callback_data="GR_va")
    C = types.InlineKeyboardButton("MMX", callback_data="MX_va")
    D = types.InlineKeyboardButton("GB", callback_data="GB_va")
    Z = types.InlineKeyboardButton("<<= Back", callback_data="romva")
    mkup.add(A,B,C,D,Z)
    bot.edit_message_text(dp.x3p, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#-------------------------------------------- EU ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'EU_va')
def rom_vayu(call):
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
#-------------------------------------------- GR ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GR_va')
def rom_vayu(call):
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
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
        <b>------------ GR ROM  ------------</b>

    เลือกเวอร์ชันที่ต้องการได้เลยย 😉"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)
#----------------------------------------- MMX MIUI -------------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'MX_va')
def rom_vayu(call):
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
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
        <b>------------ MMX ROM  ------------</b>

    เลือกเวอร์ชันที่ต้องการได้เลยย 😉"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)
#-------------------------------------------- GB ROM ---------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'GB_va')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1) 
    A = types.InlineKeyboardButton("V12.5.5", url='https://mifirm.net/download/5854')
    B = types.InlineKeyboardButton("V12.5.4", url='https://mifirm.net/download/5667')
    C = types.InlineKeyboardButton("V12.5.3", url='https://mifirm.net/download/5581')
    D = types.InlineKeyboardButton("V12.5.2", url='https://mifirm.net/download/5346')
    E = types.InlineKeyboardButton("V12.0.6", url='https://mifirm.net/download/5105')
    F = types.InlineKeyboardButton("V12.0.4", url='https://mifirm.net/download/4922')
    Z = types.InlineKeyboardButton("<<= Back", callback_data="MIUI-va")
    mkup.add(A, B, C, D, E, F, Z)
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
        <b>------------ GB ROM  ------------</b>

    เลือกเวอร์ชันที่ต้องการได้เลยย 😉"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------- Pure ROM --------------------------------------------------------#
#------------------------------------------- Pure ROM --------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'Pure-va')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    A= types.InlineKeyboardButton("OFFICIAL", callback_data="OF_va")
    B = types.InlineKeyboardButton("UNOFFICIAL", callback_data="UOF_va")
    Z = types.InlineKeyboardButton("<<= Back", callback_data="romva")
    mkup.add(A,B,Z)
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
    <b>------------ Pure Andriod  ------------</b>"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------ Official -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'OF_va')
def rom_vayu(call):
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
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
    <b>------------ Pure Andriod  ------------</b>
    <b>--------------- Official  ---------------</b>
"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------ UnOfficial -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'UOF_va')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    J = types.InlineKeyboardButton("CipherOS v2.0 A12 Gapps", url='https://drive.google.com/file/d/1y5ZLxzIzDrG_uFABibI_4CTThGZsdeEO/view')
    F = types.InlineKeyboardButton("EVO 6.0 A12 Gapps", url='https://sourceforge.net/projects/gengkapak/files/ROM/vayu/EvolutionX/12/evolution_vayu-ota-sd1a.210817.036.a8-11300236-unofficial-unsigned.zip/download')
    G = types.InlineKeyboardButton("LineageOs v19.0 A12 Vanilla", url='https://sourceforge.net/projects/other007/files/lineage-19.0-20211207-UNOFFICIAL-vayu.zip/download')
    Z = types.InlineKeyboardButton("<<= Back", callback_data="Pure-va")
    mkup.add(F,G,J,Z)
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
    <b>------------ Pure Andriod  ------------</b>
    <b>-------------- UNOfficial  --------------</b>
"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------ Recovery -------------------------------------------------------#
#------------------------------------------ Recovery -------------------------------------------------------#
@bot.callback_query_handler(func=lambda call: call.data == 'reva')
def rom_vayu(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    A= types.InlineKeyboardButton("TWRP", url='https://dl.twrp.me/vayu/twrp-3.6.0_11-0-vayu.img')
    B = types.InlineKeyboardButton("Orange Fox", url='https://us-dl.orangefox.download/61925ad3df607d814a41854e')
    Z = types.InlineKeyboardButton("<<= Back", callback_data="Backva")
    mkup.add(A,B,Z)
    text = """
        <b>------------     Poco X3 Pro     ------------</b>
        <b>------------  Recovery  ------------</b>

"""
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)


#------------------------------------------ Home Menu -----------------------------------------------------#
#------------------------------------------ Home Menu -----------------------------------------------------#
#------------------------------------------ Home Menu -----------------------------------------------------#

@bot.callback_query_handler(func=lambda call: call.data == 'Backva')
def c_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=2)
    EU = types.InlineKeyboardButton("ROM", callback_data="romva")
    GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
    GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
    mkup.add(EU, GR, GB)
    text = "<b>Poco X3 Pro</b> - เลือกเมนูที่ต้องการจ้า"
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'Backli')
def c_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=2)
    EU = types.InlineKeyboardButton("ROM", callback_data="romva")
    GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
    GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
    mkup.add(EU, GR, GB)
    text = "<b>Redmi 9t/Poco M3</b> - เลือกเมนูที่ต้องการจ้า"
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'Backmo')
def c_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=2)
    EU = types.InlineKeyboardButton("ROM", callback_data="romva")
    GR = types.InlineKeyboardButton("RECOVER", callback_data="reva")
    GB = types.InlineKeyboardButton("KERNEL", callback_data="kerva")
    mkup.add(EU, GR, GB)
    text = "<b>Redmi Note 10</b> - เลือกเมนูที่ต้องการจ้า"
    bot.edit_message_text( text, call.message.chat.id, call.message.message_id, reply_markup=mkup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

#------------------------------------------ End Inline -----------------------------------------------------#
#------------------------------------------ End Inline -----------------------------------------------------#
#------------------------------------------ End Inline -----------------------------------------------------#

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
        bot.reply_to(message, 'คำสั่ง <b>{chat}</b> ไม่ถูกต้อง พิมพ์ /help เพื่อดูคำสั่งเพิ่มเติม'.format(chat=message.text), parse_mode='HTML', reply_markup=hd)
    else:
        bot.send_message(message.chat.id , 'ยืนยันตัวตนก่อนจ้า จิ้ม -> /auth',reply_markup=hd)
    print(message.from_user.first_name, " : ", message.text)

bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())

bot.infinity_polling()