import os
import re,json
import requests
import time,random
import string
from EQUROBOT.modules.gatet import *
from EQUROBOT import app
from pyrogram import filters, types
from datetime import datetime, timedelta
from faker import Faker
from multiprocessing import Process
import threading

stopuser = {}

f = Faker()
name = f.name()
street = f.address()
city = f.city()
state = f.state()
postal = f.zipcode()
phone = f.phone_number()
coun = f.country()
mail = f.email()
command_usage = {}

def reset_command_usage():
	for user_id in command_usage:
		command_usage[user_id] = {'count': 0, 'last_time': None}


# Handler for document messages
@app.on_message(filters.document)
def main(_, message):
    # Extract user's first name
    name = message.from_user.first_name
    
    # Create inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    
    # Add buttons
    contact_button = types.InlineKeyboardButton(text="🏴‍☠️ 𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗔𝗨𝗧𝗛 🏴‍☠️", callback_data='br')
    sw = types.InlineKeyboardButton(text=" 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 🪽", callback_data='str')
    keyboard.add(contact_button)
    keyboard.add(sw)
    
    # Reply to the user
    app.send_message(message.chat.id, text='𝘾𝙝𝙤𝙤𝙨𝙚 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙐𝙨𝙚', reply_markup=keyboard)
    
    # Download the document file
    file_info = app.get_file(message.document.file_id)
    file_path = file_info.file_path
    
    # Save the file locally
    downloaded_file = app.download_file(file_path)
    with open("combo.txt", "wb") as file:
        file.write(downloaded_file)


# Callback query handler for 'str' button
@app.on_callback_query(filters.regex("^str$"))
def start_stripe_charge(_, callback_query):
    def my_function():
        id = callback_query.from_user.id
        gate = 'Stripe Charge'
        dd = 0
        live = 0
        ch = 0
        ccnn = 0
        
        # Edit the message to show progress
        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        
        try:
            with open("combo.txt", 'r') as file:
                lines = file.readlines()
                total = len(lines)
                
                # Set user status to 'start'
                stopuser[id] = {'status': 'start'}
                
                for cc in lines:
                    if stopuser[id]['status'] == 'stop':
                        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')
                        return
                    
                    # Perform BIN lookup
                    try:
                        data = requests.get('https://lookup.binlist.net/' + cc[:6]).json()
                    except Exception as e:
                        print(e)
                        continue
                    
                    # Extract relevant data
                    level = data.get('level', 'Unknown')
                    bank = data.get('bank', {}).get('name', 'Unknown')
                    country_flag = data.get('country', {}).get('emoji', 'Unknown')
                    country = data.get('country', {}).get('name', 'Unknown')
                    brand = data.get('scheme', 'Unknown')
                    card_type = data.get('type', 'Unknown')
                    
                    # Simulate processing time
                    start_time = time.time()
                    last = str(st(cc))  # Assuming st() is a function that checks the card
                    
                    # Determine the message to send based on the result
                    if 'risk' in last:
                        last = 'declined'
                    elif 'Duplicate' in last:
                        last = 'live'
                    
                    # Prepare and send message
                    msg = f'''<b>𝑪𝑯𝑨𝑹𝑮𝑬 ✅
                    
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(time.time() - start_time)} seconds .</b>'''
                    
                    # Send the message
                    app.send_message(callback_query.from_user.id, msg, parse_mode='html')
                    
                    # Example logic to count successful charges
                    if 'success' in last:
                        ch += 1
                        # Here you can optionally send this information to a Telegram group/channel
                        # using requests.post or app.send_message
                    elif 'funds' in last:
                        live += 1
                    elif "card's security" in last:
                        ccnn += 1
                    else:
                        dd += 1
                    
                    time.sleep(5)  # Simulate processing time
                    
        except Exception as e:
            print(e)
        
        # Reset user status to 'start'
        stopuser[id] = {'status': 'start'}
        
        # Edit the message to indicate completion
        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text='𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')
    
    # Start a new thread for the processing function
    threading.Thread(target=my_function).start()


# Callback query handler for 'br' button
@app.on_callback_query(filters.regex("^br$"))
def start_braintree_auth(_, callback_query):
    def my_function():
        id = callback_query.from_user.id
        gate = 'Braintree Auth'
        dd = 0
        live = 0
        riskk = 0
        
        # Edit the message to show progress
        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        
        try:
            with open("combo.txt", 'r') as file:
                lines = file.readlines()
                total = len(lines)
                
                # Set user status to 'start'
                stopuser[id] = {'status': 'start'}
                
                for cc in lines:
                    if stopuser[id]['status'] == 'stop':
                        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')
                        return
                    
                    # Perform BIN lookup
                    try:
                        data = requests.get('https://lookup.binlist.net/' + cc[:6]).json()
                    except Exception as e:
                        print(e)
                        continue
                    
                    # Extract relevant data
                    level = data.get('level', 'Unknown')
                    bank = data.get('bank', {}).get('name', 'Unknown')
                    country_flag = data.get('country', {}).get('emoji', 'Unknown')
                    country = data.get('country', {}).get('name', 'Unknown')
                    brand = data.get('scheme', 'Unknown')
                    card_type = data.get('type', 'Unknown')
                    
                    # Simulate processing time
                    start_time = time.time()
                    last = str(Tele(cc))  # Assuming Tele() is a function that checks the card
                    
                    # Determine the message to send based on the result
                    if 'risk' in last:
                        last = 'risk'
                    elif 'Duplicate' in last:
                        last = 'live'
                    
                    # Prepare and send message
                    msg = f'''<b>𝑪𝑯𝑨𝑹𝑮𝑬 ✅
                    
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(time.time() - start_time)} seconds .</b>'''
                    
                    # Send the message
                    app.send_message(callback_query.from_user.id, msg, parse_mode='html')
                    
                    # Example logic to count successful authorizations
                    if 'success' in last:
                        dd += 1
                    elif 'funds' in last:
                        live += 1
                    else:
                        riskk += 1
                    
                    time.sleep(5)  # Simulate processing time
                    
        except Exception as e:
            print(e)
        
        # Reset user status to 'start'
        stopuser[id] = {'status': 'start'}
        
        # Edit the message to indicate completion
        app.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text='𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')
    
    # Start a new thread for the processing function
    threading.Thread(target=my_function).start()


