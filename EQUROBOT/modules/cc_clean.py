from pyrogram import Client, filters
import re
from io import BytesIO
from EQUROBOT import app

def filter_bin(input_text):
    pattern = r'\d{15,16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}'
    matches = re.findall(pattern, input_text)
    return '\n'.join(matches)

@app.on_message(filters.command("clean") & filters.reply)
async def clean_command(client, message):
    if message.reply_to_message.document:
        doc = message.reply_to_message.document
        if doc.file_name.endswith('.txt'):
            file_path = await client.download_media(doc)
            with open(file_path, 'r') as file:
                text = file.read()
            
            filtered_text = filter_bin(text)
            lines = filtered_text.splitlines()

            if not filtered_text:
                await message.reply("No matching data found.")
            else:
                output = BytesIO()
                output.write(filtered_text.encode())
                output.seek(0)
                await client.send_document(
                    chat_id=message.chat.id,
                    document=output,
                    caption="Hᴇʀᴇ ɪs ᴛʜᴇ Cʟᴇᴀɴ 🫧 🪥 CC 💳 Rᴇsᴜʟᴛ",
                    file_name="cc_clean.txt"
                )
        else:
            await message.reply("Please reply to a .txt document.")
    else:
        await message.reply("Pʟᴇᴀsᴇ Rᴇᴘʟʏ A ᴅᴏᴄᴜᴍᴇɴᴛ 📄 Fɪʟᴇ.")
