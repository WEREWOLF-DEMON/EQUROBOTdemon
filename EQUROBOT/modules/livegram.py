from pyrogram import Client, filters
from pyrogram.types import Message
from EQUROBOT import app

# Bot owner's Telegram ID
owner_id = "7427691214"  # Replace with your Telegram ID


# Function to forward messages to owner
@app.on_message(filters.private & ~filters.forwarded & ~filters.bot)
async def forward_to_owner(client, message: Message):
    await client.forward_messages(chat_id=owner_id, from_chat_id=message.chat.id, message_ids=message.message_id)

# Function to send owner's reply back to original sender
@app.on_message(filters.chat(owner_id) & ~filters.forwarded)
async def forward_to_sender(client, message: Message):
    # Check if the message is a reply
    if message.reply_to_message:
        # Get the original sender's chat ID
        original_sender = message.reply_to_message.forward_from.id
        # Forward the reply to the original sender
        await client.forward_messages(chat_id=original_sender, from_chat_id=message.chat.id, message_ids=message.message_id)
