from pyrogram import Client, filters
import socket
import struct
import random
import os
from EQUROBOT import app

def generate_random_ipv4_with_port():
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    return f"{ip}:80"

@app.on_message(filters.command("ipgen", prefixes="/"))
async def ipgen_command(client, message):
    try:
        command, arg = message.text.split()
        count = int(arg)
    except ValueError:
        count = 1

    count = max(1, min(count, 100))
    ip_addresses = [generate_random_ipv4_with_port() for _ in range(count)]

    if len(ip_addresses) > 10:
        file_name = f"ip_addresses_{count}.txt"
        with open(file_name, "w") as file:
            file.write("\n".join(ip_addresses))
        await message.reply_document(
            document=file_name,
            caption=f"┏━━━━━━━⍟\n┃ GEN IP {count} IPv4 with Port 80 ✅\n┗━━━━━━━━━━━━━━━⊛\n⊙ Request by = {message.from_user.username}"
        )
        os.remove(file_name)
    else:
        reply_text = "\n".join(ip_addresses) if ip_addresses else "No IP addresses generated."
        await message.reply_text(
            f"┏━━━━━━━⍟\n┃ GEN IP {count} IPv4 with Port 80 ✅\n┗━━━━━━━━━━━━━━━⊛\n⊙ Request by = {message.from_user.username}\n\n{reply_text}"
        )
        
