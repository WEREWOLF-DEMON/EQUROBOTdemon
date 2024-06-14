from EQUROBOT import app
import requests
import re
from pyrogram import filters

@app.on_message(filters.command("xchk", prefixes=["/", "."]))
async def check_cc(_, message):
    cc_data = message.text[len('/xchk '):].strip()
    reply_msg = message.reply_to_message
    if reply_msg:
        cc_data = reply_msg.text.strip()
    
    cards = cc_data.split('\n')
    
    if len(cards) > 3:
        return await message.reply_text('Please provide details for up to 3 cards only.')

    results = []
    
    for cc in cards:
        x = re.findall(r'\d+', cc)
        if len(x) != 4:
            results.append(f'Invalid CC format for card: {cc}. Should be in the format: 4355460260824973|03|2029|273')
            continue

        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]

        VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
        if not ccn.startswith(VALID):
            results.append(f'Invalid CC type for card: {cc}')
            continue

        url = "https://mvy.ai/sk_api/api.php"
        params = {
            "lista": f"{ccn}:{mm}:{yy}:{cvv}",
            "sk": "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"
        }

        r = requests.get(url, params=params).json()

        if r['status'] == 'die':
            fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
            die_message = (
                f"┏━━━━━━━⍟\n"
                f"┃𝖣𝖤𝖢𝖫𝖨𝖭𝖤𝖣  ❌\n"
                f"┗━━━━━━━━━━━⊛\n"
                f"➩ 𝗖𝗮𝗿𝗱 : `{fullcc}`\n"
                f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : **{r['message']}**\n\n"
                f"➩ 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
                f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
            )
            results.append(die_message)
        elif r['status'] == 'approved':
            fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
            approved_message = (
                f"┏━━━━━━━⍟\n"
                f"┃𝖲𝖳𝖱𝖨𝖯𝖤 𝖠𝖴𝖳𝖧 2 ✅\n"
                f"┗━━━━━━━━━━━⊛\n"
                f"➩ 𝗖𝗮𝗿𝗱 : {fullcc}\n"
                f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 :**{r['message']}**"
                f"➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : CHARGED ${r['payment_info']['amount']}\n\n"
                f"➩ 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
                f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
            )
            results.append(approved_message)
        else:
            results.append(f"Unknown status received for card: {cc}")

    await message.reply_text("\n\n".join(results))
  
