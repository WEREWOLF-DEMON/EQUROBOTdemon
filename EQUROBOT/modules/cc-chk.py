import os
import re
import json
import requests
import time
import string
from EQUROBOT.modules.gatet import *
from EQUROBOT import app
from pyrogram import filters
from pyrogram.types import *
from datetime import datetime, timedelta
from faker import Faker
from multiprocessing import Process
import threading

stopuser = {}
f = Faker()

# Common function to handle both Stripe and Braintree actions
async def handle_payment_gateway(callback_query, gateway):
    id = callback_query.from_user.id
    gate = gateway
    dd = 0
    live = 0
    ch = 0
    ccnn = 0
    
    # Edit the message to show progress
    await app.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text=f"𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝙪𝙨𝙞𝙣𝙜 {gate}...⌛")
    
    try:
        with open("combo.txt", 'r') as file:
            lines = file.readlines()
            total = len(lines)
            
            # Set user status to 'start'
            stopuser[id] = {'status': 'start'}
            
            for cc in lines:
                if stopuser[id]['status'] == 'stop':
                    await app.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')
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
                
                # Determine the function to call based on the gateway
                if gateway == 'Stripe Charge':
                    last = str(st(cc))  # Assuming st() is a function that checks the card
                elif gateway == 'Braintree Auth':
                    last = str(Tele(cc))  # Assuming Tele() is a function that checks the card
                
                # Determine the message to send based on the result
                if 'risk' in last:
                    last = 'risk'
                elif 'Duplicate' in last:
                    last = 'live'
                elif 'success' in last:
                    last = 'success'
                elif 'funds' in last:
                    last = 'live'
                elif "card's security" in last:
                    last = 'card security issue'
                else:
                    last = 'unknown'
                
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
                await app.send_message(callback_query.from_user.id, msg, parse_mode='html')
                
                # Example logic to count successful charges/authorizations
                if 'success' in last:
                    ch += 1
                elif 'live' in last:
                    live += 1
                elif 'card security issue' in last:
                    ccnn += 1
                else:
                    dd += 1
                
                time.sleep(5)  # Simulate processing time
    
    except Exception as e:
        print(e)
    
    # Reset user status to 'start'
    stopuser[id] = {'status': 'start'}
    
    # Edit the message to indicate completion
    await app.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text=f'𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗬 ➜ @YourExDestiny')


# Callback query handler for both 'str' and 'br' buttons
@app.on_callback_query(filters.regex("^(str|br)$"))
def start_payment(_, callback_query):
    if callback_query.data == 'str':
        await handle_payment_gateway(callback_query, 'Stripe Charge')
    elif callback_query.data == 'br':
        await handle_payment_gateway(callback_query, 'Braintree Auth')


# Handler for document messages
@app.on_message(filters.document)
async def handle_document(_, message):
    # Extract user's first name
    name = message.from_user.first_name
    
    # Create inline keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🏴‍☠️ 𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗔𝗨𝗧𝗛 🏴‍☠️", callback_data='br'),
                InlineKeyboardButton(text=" 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 🪽", callback_data='str'),
            ]
        ]
    )
    
    # Reply to the user
    await message.reply_text('𝘾𝙝𝙤𝙤𝙨𝙚 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙐𝙨𝙚', reply_markup=keyboard)
    
    # Save the file locally
    downloaded_file = await message.download()
    with open("combo.txt", "wb") as file:
        file.write(downloaded_file)

