from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import OWNER_ID
from Flash import app, BOT_USERNAME, BOT_NAME

START_TEXT = """
**ʜᴇʏ** {},
ɪ ᴀᴍ [{bot_name}](https://t.me/{bot_username}), ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ-ʙᴀsᴇᴅ ʀᴏʙᴏᴛ ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴠᴀʀɪᴏᴜs ᴛᴀsᴋs ᴇғғᴏʀᴛʟᴇssʟʏ.

ᴇxᴘʟᴏʀᴇ ᴍʏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴛᴏ ᴅɪsᴄᴏᴠᴇʀ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴀᴘᴀʙɪʟɪᴛɪᴇs ᴀɴᴅ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴍᴇ.
"""

CHK_TXT = "Hello User!\n\n[𝗙𝗹𝗮𝘀𝗵 𐏓](https://t.me/TheFlashRobot) Checker Gates.\n\nClick on each one below to get to know them better."
NISHKA_TXT = "__Use the currency system to access premium features.__"
AUTH_TXT = "Hello User!\n\n[𝗙𝗹𝗮𝘀𝗵 𐏓](https://t.me/TheFlashRobot) Auth Gates.\n\nClick on each one below to get to know them better."
CHARGE_TXT = "Hello User!\n\n[𝗙𝗹𝗮𝘀𝗵 𐏓](https://t.me/TheFlashRobot)Charge Gates.\n\nClick on each one below to get to know them better."

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

Hello User! [𝗙𝗹𝗮𝘀𝗵 𐏓](https://t.me/TheFlashRobot) offers plenty of commands, including Auth Gates, Charge Gates, Tools, and other features.

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
        video="https://telegra.ph/file/19054d4deea2e1f4f2c97.mp4",
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
