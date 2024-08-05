from pyrogram import Client, filters
from pyrogram.types import Message
import os
from EQUROBOT import app

@app.on_message(filters.command("split") & filters.reply)
async def split_file(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id
        file_name = message.reply_to_message.document.file_name
        
        # Get number from command (default is 2)
        try:
            num_lines = int(message.text.split(" ")[1])
        except (IndexError, ValueError):
            num_lines = 2

        # Download the file
        file_path = await client.download_media(file_id)

        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Split lines
        for i in range(0, len(lines), num_lines):
            split_lines = lines[i:i + num_lines]
            split_file_path = f"split_{i//num_lines + 1}.txt"
            with open(split_file_path, 'w') as split_file:
                split_file.writelines(split_lines)
            
            # Send the split file
            await client.send_document(chat_id=message.chat.id, document=split_file_path)
            
            # Clean up the split file
            os.remove(split_file_path)
        
        # Clean up the original file
        os.remove(file_path)

    else:
        await message.reply("Please reply to a document file to split it.")
