import os
from pyrogram import Client, filters
from pyrogram.types import Message
from EQUROBOT import app

# Function to save the message text to a .txt file
def save_message_to_txt(message_text: str, filename: str = "messages.txt"):
    with open(filename, "a") as f:
        f.write(message_text + "\n")

@app.on_message(filters.reply & filters.command("txt"))
async def save_replied_message(client: Client, message: Message):
    replied_message = message.reply_to_message
    if replied_message and replied_message.text:
        save_message_to_txt(replied_message.text)
        confirmation_message = await message.reply_text("Message saved to messages.txt!")
        
        # Send the messages.txt file to the user
        if os.path.exists("messages.txt"):
            await message.reply_document("messages.txt")
        
        # Delete the confirmation message
        await confirmation_message.delete()
    else:
        await message.reply_text("Please reply to a text message to save it.")
    if os.path.exists("messages.txt"):
        os.remove("messages.txt")
