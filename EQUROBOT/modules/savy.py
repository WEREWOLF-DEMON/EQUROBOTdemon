import requests
import re
import os
import json
from EQUROBOT import app
from pyrogram import Client, filters

MAX_RETRIES = 5
API_URL = "https://api.mvy.ai/"

# Extract credit card details from message text
def extract_credit_card_details(message_text):
    cards = []
    input = re.findall(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", message_text)
    
    for cc in input:
        cc = re.sub(r"[-\s]", "", cc)  # Remove spaces and dashes
        cards.append(cc)

    print(cards)
    return cards

# Read credit card information from file and format
def read_cc_file(file_path):
    cc_list = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                if len(parts[2]) == 2:  # Check if year is in two-digit format
                    parts[2] = '20' + parts[2]
                formatted_cc = ':'.join(parts)
                cc_list.append(formatted_cc)
    return cc_list

# Check credit card against API
def check_cc(cc, amount=5.0, currency="usd"):
    lista = ':'.join(cc.split('|'))
    params = {
        "lista": lista,
        "currency": currency,
        "amount": amount,
        "sk": "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"
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        
        response_data = response.json()
        status = response_data.get('status')
        message = response_data.get('message')

        if status == "approved":
            card_info = response_data.get('card_info', {})
            payment_info = response_data.get('payment_info', {})
            bank_info = response_data.get('bank_info', {})

            result = f"Transaction Approved ✅\n"
            result += f"Card: {card_info.get('number', '')}\n"
            result += f"Response: {message}\n"
            result += f"Amount: {payment_info.get('amount', '')} {payment_info.get('currency', '')}\n"
            result += f"Bin Info: {bank_info.get('bin_info', '')}\n"
            result += f"Bank: {bank_info.get('issuing_bank', '')}\n"
            result += f"Country: {bank_info.get('country', '')}\n"
            result += f"Vbv: {bank_info.get('vbv', '')}\n"

        else:
            result = f"Transaction Failed ❌\nMessage: {message}"

    except requests.RequestException as e:
        result = f"Request Exception: {str(e)}"
    
    except json.JSONDecodeError as e:
        result = f"JSON Decode Error: {str(e)}"
    
    except Exception as e:
        result = f"Error: {str(e)}"

    return result

# Save response to Live.txt for successful transactions
def save_live_response(cc, message):
    with open('Live.txt', 'a') as file:
        file.write(f"CC: {cc}\n")
        file.write(f"Response: {message} ✅\n\n")


# Handle incoming messages with the /cc command
@app.on_message(filters.command("cc", prefixes=[".", "/"]))
async def check_cc_command(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc_entry = message.text[command_prefix_length:].strip()

    reply_msg = message.reply_to_message
    if reply_msg:
        if reply_msg.text:
            cc_entries = extract_credit_card_details(reply_msg.text.strip())
            results = [check_cc(entry) for entry in cc_entries]
            await message.reply_text("\n\n".join(results))
        elif reply_msg.document:
            file_path = await app.download_media(reply_msg.document.file_id)
            output_file = f"results_{reply_msg.document.file_name}.txt"
            results = [check_cc(cc) for cc in read_cc_file(file_path)]
            with open(output_file, 'w') as file:
                file.write("\n\n".join(results))
            await message.reply_document(document=output_file)
            os.remove(file_path)
            os.remove(output_file)
        else:
            await message.reply_text("Unsupported file type.")
    elif cc_entry:
        cc_entries = cc_entry.split('\n')
        results = [check_cc(entry) for entry in cc_entries]
        await message.reply_text("\n\n".join(results))
    else:
        await message.reply_text("Please provide credit card details or reply to a message containing them.")
