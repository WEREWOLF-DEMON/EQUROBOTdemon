import random
from datetime import datetime, timedelta
import os
from pyrogram import Client, filters
from EQUROBOT import app, BOT_USERNAME

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_card_number(prefix, length):
    number = prefix
    while len(number) < (length - 1):
        number.append(random.randint(0, 9))
    checksum = luhn_checksum(int(''.join(map(str, number))) * 10)
    number.append((10 - checksum) % 10)
    return ''.join(map(str, number))

def generate_card_details(prefix):
    length = 16  # Assuming a standard length for credit card numbers
    card_number = generate_card_number(prefix, length)
    cvv = generate_cvv()
    expiration_date = generate_expiration_date()
    return f"{card_number}|{expiration_date}|{cvv}"

def generate_cvv():
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def generate_expiration_date():
    start_date = datetime.now()
    month = random.randint(1, 12)
    year = random.randint(start_date.year + 1, start_date.year + 5)
    return f"{month:02d}|{year}"

# List of BINs
bins = [
    "4411040534",
    "4833120144",
    "4427322533",
    "485038",
    "5219918900",
    "51461601",
    "4124510157",
    "428581000",
    "462845004",
    "468138000003",
    "4100390552",
    "414720221",
    "516838004",
    "47820020",
    "414720251006",
    "4147202422",
    "4147202429",
    "41855060086",
    "4485590006",
    "435546026",
    "4266841656",
    "401043202959",
    "45659820202",
    "5425504500",
    "44468900"
]

@app.on_message(filters.command("lqdump"))
async def dump_cards(client, message):
    try:
        amount = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid command to dump CC. Use /lqdump <amount>")
        return

    file_path = f"{amount}x_LQ_CC_Scraped_By_@{BOT_USERNAME}.txt"
    with open(file_path, "w") as file:
        for _ in range(amount):
            bin = random.choice(bins)
            bin_prefix = [int(d) for d in bin if d.isdigit()]
            card_details = generate_card_details(bin_prefix)
            file.write(card_details + "\n")

    await message.reply_document(file_path)
    os.remove(file_path)
