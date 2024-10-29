import nest_asyncio
import os
import requests
from gtts import gTTS
from pyrogram import filters
from pyrogram.enums import ChatAction
from EQUROBOT import app
import g4f
from pyrogram.enums import ParseMode

nest_asyncio.apply()

API_URL = "https://sugoi-api.vercel.app/search"

@app.on_message(filters.command(["qu"], prefixes=["e", "E"]))
async def chat_arvis(app, message):
    try:
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name

        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}, I am Equ. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@app.on_message(filters.command(["chatgpt", "ai", "ask", "Master"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat_gpt(app, message):
    try:
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text("Hello sir, I am Equ. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@app.on_message(filters.command(["iri"], prefixes=["s", "S"]))
async def chat_annie(app, message):
    try:
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name

        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}, I am Siri. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        tts = gTTS(response, lang='hi')
        tts.save('siri.mp3')
        await app.send_voice(chat_id=message.chat.id, voice='siri.mp3')
        os.remove('siri.mp3')
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@app.on_message(filters.command(["bing"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def bing_search(app, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(message.command[1:])
        response = requests.get(API_URL, params={"keyword": keyword})

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
                return

            message_text = "\n\n".join(f"{res.get('title', '')}\n{res.get('link', '')}" for res in results[:7])
            await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
