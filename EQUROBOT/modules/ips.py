from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
from EQUROBOT import app


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
