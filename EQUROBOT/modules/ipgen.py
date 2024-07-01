from pyrogram import Client, filters
import socket
import struct
import random
import os
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
from EQUROBOT import app

# Function to generate a random IPv4 address
def generate_random_ipv4():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# Command handler for /ipgen
@app.on_message(filters.command("ipgen", prefixes="/"))
async def ipgen_command(client, message):
    # Get the argument from the command (number of IPs to generate)
    try:
        command, arg = message.text.split()
        count = int(arg)
    except ValueError:
        count = 1  # Default to generating one IP if no valid count provided

    # Generate the IPs
    ip_addresses = [generate_random_ipv4() for _ in range(count)]

    # If more than 10 IPs generated, save them to a file and send as a document
    if len(ip_addresses) > 10:
        file_name = f"ip_addresses_{count}.txt"
        with open(file_name, "w") as file:
            file.write("\n".join(ip_addresses))
        await message.reply_document(document=file_name, caption=f"Generated {count} IPv4 addresses.")
        os.remove(file_name)  # Remove the file after sending
    else:
        # Reply with the generated IPs
        if ip_addresses:
            reply_text = "\n".join(ip_addresses)
        else:
            reply_text = "No IP addresses generated."
        await message.reply_text(reply_text)



# _--------------


def get_ips_from_myipms(url, limit=None):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ip_elements = soup.find_all('a', {'href': lambda x: x and x.startswith('/info/whois/')})
        ip_addresses = [ip.text for ip in ip_elements if ip.text.count('.') == 3]
        if limit:
            ip_addresses = ip_addresses[:limit]
        return ip_addresses
    else:
        return None

@app.on_message(filters.command("ips"))
async def generate_ips(client: Client, message: Message):
    try:
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.reply_text("Usage: /ips <number_of_ips>")
            return
        
        ip_count = int(parts[1])
        url = 'http://myip.ms/'
        ip_addresses = get_ips_from_myipms(url, ip_count)
        
        if ip_addresses:
            if ip_count > 10:
                with open("ips.txt", "w") as file:
                    for ip in ip_addresses:
                        file.write(ip + "\n")
                await message.reply_document("ips.txt")
            else:
                await message.reply_text("\n".join(ip_addresses))
        else:
            await message.reply_text("Failed to retrieve IP addresses.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
