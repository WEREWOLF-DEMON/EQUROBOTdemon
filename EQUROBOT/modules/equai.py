import os, time
import openai
from pyrogram import filters
from EQUROBOT import app as Nexus
from pyrogram.enums import ChatAction, ParseMode
from gtts import gTTS

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

openai.api_key = "sk-None-odGRI5D06fdcbfbuh7atT3BlbkFJADhok3Z9eU4u2WHaHIMM"




@Nexus.on_message(filters.command(["qu" , ],  prefixes=["e","E"]))
async def chat(Nexus :Nexus, message):
    
    try:
        start_time = time.time()
        await Nexus.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "ʜᴇʟʟᴏ sɪʀ\nᴇxᴀᴍᴘʟᴇ:-.ask How to set girlfriend ?")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            await message.reply_text(f"{x}")     
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e} ")        






@Nexus.on_message(filters.command(["iri"],  prefixes=["s","S"]))
async def chat(Nexus :Nexus, message):
    
    try:
        start_time = time.time()
        await Nexus.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "ʜᴇʟʟᴏ sɪʀ\nᴇxᴀᴍᴘʟᴇ:-.assis How to set girlfriend ?")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            text = x    
            tts = gTTS(text, lang='en')
            tts.save('output.mp3')
            await Nexus.send_voice(chat_id=message.chat.id, voice='output.mp3')
            os.remove('output.mp3')            
            
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e} ")
