import asyncio, os, time, aiohttp, random, requests
from requests.adapters import HTTPAdapter, Retry
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegraph import upload_file
from pymongo import MongoClient
import re
import config
from datetime import datetime
from pyrogram import filters, Client
from EQUROBOT import app
import httpx


# ---------------------------------------------------------------------

@app.on_message(filters.command(["deploy"]))
async def heroku_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a repository URL.")
        return

    repo_url = message.text.split(" ", 1)[1]
    heroku_url = f"https://dashboard.heroku.com/new?template={repo_url}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Deploy to Heroku", url=heroku_url)]]
    )
    await message.reply_text("Click the button below to deploy to Heroku:", reply_markup=reply_markup)


# ----------------------------------------------------------------------

mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')


@app.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please enter your MongoDB URL after the command. Example: /mongochk YOUR_MONGO_URL")
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()
            await message.reply("MongoDB URL is valid and connection successful ✅")
        except Exception as e:
            await message.reply(f"Failed to connect to MongoDB: {e}")
    else:
        await message.reply("Invalid MongoDB URL format. Please enter a valid MongoDB URL💔")


# ---------------------------------------------------------------------

@app.on_message(filters.command('info'))
async def myinfo_command(client, message):
    user = message.from_user

    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user = await app.get_users(user_id)
        except ValueError:
            await app.send_message(chat_id=message.chat.id, text="Invalid user ID.")
            return

    user_info = (
        f"**User Info**\n"
        f"ID: `{user.id}`\n"
        f"Username: @{user.username}\n"
        f"First Name: {user.first_name}\n"
        f"Last Name: {user.last_name}\n"
        f"Mention: {user.mention}\n"
    )
    await app.send_message(chat_id=message.chat.id, text=user_info)


# ---------------------------------------------------------------------

@app.on_message(filters.command("lg") & filters.user(config.OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    await message.reply_text("Your bot has successfully left the chat 🙋‍♂️")
    await app.leave_chat(chat_id=chat_id, delete=True)


# ---------------------------------------------------------------------

@app.on_message(filters.command("repo"))
async def repo(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/repos/DAXXTEAM/GITHUB-HEROKU/contributors")

    if response.status_code == 200:
        users = response.json()
        list_of_users = ""
        count = 1
        for user in users:
            list_of_users += f"{count}. [{user['login']}]({user['html_url']})\n"
            count += 1

        text = f"""[Repo Link](https://github.com/DAXXTEAM/GITHUB-HEROKU) | [Group](https://t.me/HEROKUFREECC)
| Contributors |
----------------
{list_of_users}"""
        await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, text="Failed to fetch contributors.")


# ---------------------------------------------------------------------

def download_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to download source code. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.on_message(filters.command("html"))
def web_download(client, message):
    if len(message.command) == 1:
        message.reply_text("Please enter a URL along with the /html command.")
        return

    url = message.command[1]
    source_code = download_website(url)
    if source_code.startswith('An error occurred') or source_code.startswith('Failed to download'):
        message.reply_text(source_code)
    else:
        with open('website.txt', 'w', encoding='utf-8') as file:
            file.write(source_code)
        message.reply_document(document='website.txt', caption=f"Source code of {url}")


# ---------------------------------------------------------------------

def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        pypi_info = response.json()
        return pypi_info
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None


@app.on_message(filters.command("pypi", prefixes="/"))
def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        pypi_info = get_pypi_info(package_name)
        if pypi_info:
            info_message = f"Package Name: {pypi_info['info']['name']}\n" \
                           f"Latest Version: {pypi_info['info']['version']}\n" \
                           f"Description: {pypi_info['info']['summary']}\n" \
                           f"Project URL: {pypi_info['info']['project_urls']['Homepage']}"
            client.send_message(message.chat.id, info_message)
        else:
            client.send_message(message.chat.id, "Failed to fetch information from PyPI")
    except IndexError:
        client.send_message(message.chat.id, "Please provide a package name after the /pypi command.")


# ---------------------------------------------------------------------

@app.on_message(filters.video_chat_started)
async def video_chat_started(_, msg):
    await msg.reply("**🎙️ Voice chat started!**")


@app.on_message(filters.video_chat_ended)
async def video_chat_ended(_, msg):
    await msg.reply("**🔇 Voice chat ended. Thanks for joining**")


@app.on_message(filters.video_chat_members_invited)
async def video_chat_members_invited(app, message: Message):
    text = f"{message.from_user.mention} invited "
    for user in message.video_chat_members_invited.users:
        text += f"[{user.first_name}](tg://user?id={user.id}) "
    await message.reply(f"{text} ☄️")


@app.on_message(filters.command("leavegroup") & filters.user(config.OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    await message.reply_text("Goodbye! 🫡")
    await app.leave_chat(chat_id=chat_id, delete=True)


@app.on_message(filters.command(["tgm", "telegraph"]))
def upload_to_telegraph(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("Making a telegraph link, please wait...")
        path = reply.download()
        fk = upload_file(path)
        url = "https://graph.org" + fk[0]
        i.edit(f'Your link: {url}')


@app.on_message(filters.command("table"))
def multiplication_table(_, message: Message):
    try:
        number = int(message.text.split()[1])
        table = "\n".join([f"{number} x {i} = {number * i}" for i in range(1, 11)])
        message.reply_text(f"Multiplication table of {number}:\n\n{table}")
    except IndexError:
        message.reply_text("Please enter a valid number after the command /table.")
    except ValueError:
        message.reply_text("Invalid input. Please enter a valid number.")


@app.on_message(filters.command("me"))
def get_user_chat_id(_: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    response_text = f"Your ID: `{user_id}`\nChat ID: `{chat_id}`"
    message.reply_text(response_text)


@app.on_message(filters.command("repo"))
async def send_repo_link(client: Client, message: Message):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Repository", url="https://github.com/DAXXTEAM/GITHUB-HEROKU")]
    ])
    await message.reply_text("Visit our repository:", reply_markup=reply_markup)
    
