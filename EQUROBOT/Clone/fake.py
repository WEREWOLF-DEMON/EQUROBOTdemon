import requests
from EQUROBOT import app as Checker
from pyrogram import filters

@Checker.on_message(filters.command("fake"))
async def address(_, message):
    try:
        query = message.text.split(maxsplit=1)[1].strip()
        url = f"https://randomuser.me/api/?nat={query}"
        response = requests.get(url)
        data = response.json()

        if "results" in data:
            user_data = data["results"][0]

            name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
            address = f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}" 
            city = user_data['location']['city']
            state = user_data['location']['state']
            country = user_data['location']['country'] 
            postal = user_data['location']['postcode']
            email = user_data['email']
            phone = user_data['phone']
            picture_url = user_data['picture']['large']

            caption = f"""
┏━━━━━━━⍟
┃🗺️**{country}**🗺️
┗━━━━━━━━━━━⊛     
**𝗙𝗨𝗟𝗟 𝗡𝗔𝗠𝗘 ** ⇢`{name}`
**𝗔𝗗𝗗𝗥𝗘𝗦𝗦** ⇢ `{address}`
**𝗖𝗢𝗨𝗡𝗧𝗥𝗬 ** ⇢ `{country}`
**𝗖𝗜𝗧𝗬** ⇢ `{city}`
**𝗦𝗧𝗔𝗧𝗘** ⇢ `{state}`
**𝗣𝗢𝗦𝗧𝗔𝗟** ⇢ `{postal}`
**𝗘𝗠𝗔𝗜𝗟** ⇢ `{email}`
**𝗣𝗛𝗢𝗡𝗘** ⇢ `{phone}`
            """

            await message.reply_photo(photo=picture_url, caption=caption)
        else:
            await message.reply_text("No address found. Please provide a valid country code.")
    except IndexError:
        await message.reply_text("Please provide a country code after the /fake command.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
