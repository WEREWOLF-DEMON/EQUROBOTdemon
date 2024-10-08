from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from EQUROBOT import app


OWNER_ID = 7427691214  # Admin's Telegram ID

# Define the command handler for /buy
@app.on_message(filters.command("buy"))
async def buy_command(client, message):
    # Define the message text
    response_text = """📝 EQUROBOT 𝖯𝗅𝖺𝗇𝗌 :
━━━━━━━━━━━━━━

𝗧𝗲𝘀𝘁𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟭 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟭.𝟵𝟵$

𝗦𝘁𝗮𝗿𝘁𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟳 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟲.𝟵𝟵$

𝗦𝗶𝗹𝘃𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟭𝟱 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟭𝟰.𝟵𝟵$

𝗚𝗼𝗹𝗱: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟯𝟬 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟮𝟰.𝟵𝟵$
"""

    # Create the inline keyboard with buttons
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("KNOW ADMIN", callback_data="know_admin")],
        [InlineKeyboardButton("PAYMENT METHOD", callback_data="payment_method")],
        [InlineKeyboardButton("CLOSE", callback_data="close")]
    ])

    # Send the message with buttons
    await message.reply_text(response_text, reply_markup=keyboard)

# Handle button presses
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "know_admin":
        # Send a message to the OWNER_ID (admin)
        await client.send_message(
            chat_id=OWNER_ID,
            text=f"User {callback_query.from_user.mention} is asking for admin support."
        )

        # Send a confirmation message to the user
        await callback_query.message.edit_text("Admin has been notified. They will contact you shortly.")

    elif callback_query.data == "payment_method":
        # Updated payment method information
        payment_info = """
**CRYPTO 💸 PAYMENT 💰**

**BINANCE ID**:-
794965900 [IAMDAXX] ✅

**LTC** ✅
`LdboLQKDe9EECZHWveQUwYkgnNAvsLGCPJ`

**USDT TRC 20** ✅
`THHGSDR4xr5h93GMkv8NyjAaYqH1nYmwcm`

**BTC** ✅
`1CPUYMryhjeGxjLGL6P2sAJkhJEJkBBLRN`

**INDIAN 🇮🇳 PAYMENT 💰**

**UPI**: `iamdaxx@ybl` ✅
**QR**: OFF ❌
"""
        # Update the message with the new payment details and new buttons
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK TO PRIST LIST", callback_data="buy")],
            [InlineKeyboardButton("KNOW ADMIN", callback_data="know_admin")],
            [InlineKeyboardButton("CLOSE", callback_data="close")]
        ])
        await callback_query.message.edit_text(payment_info, reply_markup=keyboard)

    elif callback_query.data == "close":
        await callback_query.message.delete()
