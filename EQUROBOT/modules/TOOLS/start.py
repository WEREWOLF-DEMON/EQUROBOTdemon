from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import OWNER_ID
from EQUROBOT import app, BOT_USERNAME

BOT_NAME = '˹ ˹ ᴇǫᴜʀᴏʙᴏᴛ ˼ ˼'

START_TEXT = """
**ʜᴇʏ** {},
ɪ ᴀᴍ [{bot_name}](https://t.me/{bot_username}), ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ-ʙᴀsᴇᴅ ʀᴏʙᴏᴛ ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴠᴀʀɪᴏᴜs ᴛᴀsᴋs ᴇғғᴏʀᴛʟᴇssʟʏ.

ᴇxᴘʟᴏʀᴇ ᴍʏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴛᴏ ᴅɪsᴄᴏᴠᴇʀ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴀᴘᴀʙɪʟɪᴛɪᴇs ᴀɴᴅ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴍᴇ.
"""

CHK_TXT = "Hello User!\n\n[˹ ˹ ᴇǫᴜʀᴏʙᴏᴛ ˼ ˼](https://t.me/EQUROBOT) Checker Gates.\n\nClick on each one below to get to know them better."
NISHKA_TXT = "__Use the currency system to access premium features.__"
AUTH_TXT = "Hello User!\n\n[˹ ˹ ᴇǫᴜʀᴏʙᴏᴛ ˼ ˼](https://t.me/EQUROBOT) Auth Gates.\n\nClick on each one below to get to know them better."
CHARGE_TXT = "Hello User!\n\n[˹ ˹ ᴇǫᴜʀᴏʙᴏᴛ ˼ ˼](https://t.me/EQUROBOT)Charge Gates.\n\nClick on each one below to get to know them better."

LOOKUP_TXT = """
**Lookup Commands 🔍**

Status: **Active** ✅

➥ /bin : Retrieve BIN information.
➥ /gate : Inspect payment gateways.
➥ /sk : Check SK status (live or dead).
➥ /msk : Mass SK status check.
➥ /sktxt : Mass SK status check from a document.
➥ /proxy : Check a proxy's live status.
➥ /proxytxt : Check proxies' live status from a document.
➥ /chkip : Inspect IP information.
"""

TOOL_TXT = """
**Toolkit Commands 🛠**

Status: **Active** ✅

➥ /gen : Generate CCs using a 6-digit BIN [LUHAN ALGORITHM].
➥ /fake : Get a random address from a specific country (use country code).
➥ /scr : Scrape CCs from a channel or group.
➥ /skscr : Scrape SKs from a channel or group.
➥ /proxyscr : Scrape proxies from a channel or group.
➥ /ipgen : Generate a specified number of IP addresses.
➥ /txt : Convert replied text to a document.
➥ /fl or /clean : Clean CCs, proxies, and SKs from a file.
➥ /split : Split a file or input into specified parts.
"""

HELP_TXT = """
**Bot Status:** Active ✅

Hello User! [˹ ˹ ᴇǫᴜʀᴏʙᴏᴛ ˼ ˼](https://t.me/EQUROBOT) offers plenty of commands, including Auth Gates, Charge Gates, Tools, and other features.

Click each of them below to know more.
"""

EXTRA_TXT = """
**Additional Features:**

Status: **Active** ✅

➥ /upscale : Upscale an image.
➥ /getdraw : Generate an image.
➥ /mongochk : Verify a MongoDB URL.
➥ /insta : Download Instagram reels.
➥ /webss : Take a screenshot of a webpage.
➥ /rmbg : Remove the background from an image.
➥ /pypi : Check the version of a PyPI package.
➥ /domain : Get domain information.
➥ /gps : Retrieve GPS coordinates.
"""

STRIPESITE_TXT = """
**Stripe Site Based Charge Gate**

Status: Inactive ❌

1. Charge 5$
   ➜ Single: `/chk cc|mm|yy|cvv`
   ➜ Mass (Limit = 5): `/mchk cc|mm|yy|cvv`
"""

BCHARGE_TXT = """
**Braintree Charge Gate**

Status: Inactive ❌

1. Charge £1
   ➜ Single: `/br cc|mm|yy|cvv`
   ➜ Mass (Limit = 5): `/mbr cc|mm|yy|cvv`
"""

SKCHARGE_TXT = """
**SK Based Gates**

Status: **Active** ✅

1. Charge $1 CVV
   ➜ Single: `/xvv cc|mm|yy|cvv`
   ➜ Mass (Max Limit = 10): `/xxvv cc|mm|yy|cvv`
"""

B3AUTH_TXT = """
**Braintree Auth**

Status: Inactive ❌

1. Braintree B3 Auth
   ➜ Single: `/ba cc|mm|yy|cvv`
   ➜ Mass (Limit = 5): `/mba cc|mm|yy|cvv`
"""

STAUTH_TXT = """
**Stripe Auth**

Status: **Active** ✅

1. Stripe Auth
   ➜ Single: `/sa cc|mm|yy|cvv`
   ➜ Mass (Limit = 5): `/msa cc|mm|yy|cvv`
"""

VBV_TXT = """
**Braintree VBV**

Status: **Active** ✅

1. VBV Lookup
   ➜ Single: `/vbv cc|mm|yy|cvv`
   ➜ Mass (Limit = 5): `/mvbv cc|mm|yy|cvv`
"""


def get_home_buttons():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Menu 🔎", callback_data="help_")]]
    )


def get_back_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="help_")]]
    )


def get_skbased_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="charge_")]]
    )


def get_b3site_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="charge_")]]
    )


def get_stripesite_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="charge_")]]
    )


def get_braintreeauth_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="auth_")]]
    )


def get_stripeauth_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="auth_")]]
    )


def get_vbv_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Go Back ◀️", callback_data="checker_")]]
    )


def get_checker_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Auth", callback_data="auth_"),
                InlineKeyboardButton("Charge", callback_data="charge_"),
            ],
            [InlineKeyboardButton("VBV", callback_data="vbv_")],
            [InlineKeyboardButton("Go Back ◀️", callback_data="help_")],
        ]
    )


def get_auth_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Stripe", callback_data="stripeauth_"),
                InlineKeyboardButton("Braintree", callback_data="braintreeauth_"),
            ],
            [InlineKeyboardButton("Go Back ◀️", callback_data="checker_")],
        ]
    )


def get_charge_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Stripe", callback_data="stripesite_"),
                InlineKeyboardButton("Braintree", callback_data="b3site_"),
            ],
            [InlineKeyboardButton("SK Based", callback_data="skbased_")],
            [InlineKeyboardButton("Go Back ◀️", callback_data="checker_")],
        ]
    )


def get_help_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Checker", callback_data="checker_"),
                InlineKeyboardButton("Lookup", callback_data="lookup_"),
            ],
            [InlineKeyboardButton("Toolkit", callback_data="tool_")],
            [
                InlineKeyboardButton("Nishka", callback_data="credits_"),
                InlineKeyboardButton("Extra", callback_data="extra_"),
            ],
            [InlineKeyboardButton("Home", callback_data="home_")],
        ]
    )


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_video(
        video="https://telegra.ph/file/365de71e032aadb98e1d2.mp4",
        caption=START_TEXT.format(
            message.from_user.mention, bot_name=BOT_NAME, bot_username=BOT_USERNAME
        ),
        reply_markup=get_home_buttons(),
    )


@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply(HELP_TXT, reply_markup=get_help_buttons())


@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    text, markup = await get_callback_response(query)
    await query.message.edit_text(text, reply_markup=markup)


async def get_callback_response(query: CallbackQuery):
    callback_data = query.data

    mappings = {
        "home_": (
            START_TEXT.format(
                query.from_user.mention, bot_name=BOT_NAME, bot_username=BOT_USERNAME
            ),
            get_home_buttons(),
        ),
        "help_": (HELP_TXT, get_help_buttons()),
        "checker_": (CHK_TXT, get_checker_buttons()),
        "auth_": (AUTH_TXT, get_auth_buttons()),
        "charge_": (CHARGE_TXT, get_charge_buttons()),
        "lookup_": (LOOKUP_TXT, get_back_button()),
        "credits_": (NISHKA_TXT, get_back_button()),
        "extra_": (EXTRA_TXT, get_back_button()),
        "tool_": (TOOL_TXT, get_back_button()),
        "vbv_": (VBV_TXT, get_vbv_button()),
        "stripeauth_": (STAUTH_TXT, get_stripeauth_button()),
        "braintreeauth_": (B3AUTH_TXT, get_braintreeauth_button()),
        "skbased_": (SKCHARGE_TXT, get_skbased_button()),
        "b3site_": (BCHARGE_TXT, get_b3site_button()),
        "stripesite_": (STRIPESITE_TXT, get_stripesite_button()),
    }

    return mappings.get(callback_data, (HELP_TXT, get_help_buttons()))

#BUY COMMAND ADD

@app.on_message(filters.command("buy"))
async def buy_command(client, message):
    response_text = """📝 EQUROBOT 𝖯𝗅𝖺𝗇𝗌 :
━━━━━━━━━━━━━━

𝗧𝗲𝘀𝘁𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟭 𝗗𝗮𝘆 𝘀 𝗮𝘁 𝟭.𝟵𝟵$

𝗦𝘁𝗮𝗿𝘁𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟳 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟲.𝟵𝟵$

𝗦𝗶𝗹𝘃𝗲𝗿: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟭𝟱 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟭𝟰.𝟵𝟵$

𝗚𝗼𝗹𝗱: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗙𝗼𝗿 𝟯𝟬 𝗗𝗮𝘆𝘀 𝗮𝘁 𝟮𝟰.𝟵𝟵$
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("KNOW ADMIN", url=f"https://t.me/hitdetect")],
        [InlineKeyboardButton("PAYMENT METHOD", callback_data="payment_method")],
        [InlineKeyboardButton("CLOSE", callback_data="close")]
    ])

    await message.reply_text(response_text, reply_markup=keyboard)

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "payment_method":
        payment_info = """
**CRYPTO 💸 PAYMENT 💰**

**BINANCE ID**:-
794965900 [IAMDAXX] ✅

**LTC** ✅
LdboLQKDe9EECZHWveQUwYkgnNAvsLGCPJ

**USDT TRC 20** ✅
THHGSDR4xr5h93GMkv8NyjAaYqH1nYmwcm

**BTC** ✅
1CPUYMryhjeGxjLGL6P2sAJkhJEJkBBLRN

**INDIAN 🇮🇳 PAYMENT 💰**

**UPI**: iamdaxx@ybl ✅
**QR**: OFF ❌
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK TO PRIST LIST", callback_data="buy")],
            [InlineKeyboardButton("KNOW ADMIN", url=f"https://t.me/{OWNER_USERNAME}")],
            [InlineKeyboardButton("CLOSE", callback_data="close")]
        ])
        await callback_query.message.edit_text(payment_info, reply_markup=keyboard)

    elif callback_query.data == "close":
        await callback_query.message.delete()

