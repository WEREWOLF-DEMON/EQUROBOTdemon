from pyrogram import Client, filters
import random
import aiohttp
from EQUROBOT import app

# Assuming 'app' is your Pyrogram Client instance
@app.on_message(filters.command(['vbv', 'VBV'], prefixes=['.', '/']))
async def vbv_command(client, message):
    try:
        # Extract the credit card details from the message
        card_details = message.text.split()[1].strip()

        # Simulate the 3D Secure lookup process
        result = await simulate_3d_secure_lookup(card_details)

        # Format the response based on the simulation outcome
        response_text = format_response(card_details, result)

        # Send the formatted response back to the user
        await client.send_message(chat_id=message.chat.id, text=response_text)

    except IndexError:
        await client.send_message(chat_id=message.chat.id, text="Please provide credit card details in the format: cc|mm|yyyy|cvv")
    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f"Error: {str(e)}")

def format_response(card_details, result):
    card_number, expiration_month, expiration_year, cvv = card_details.split('|')
    card_number = card_number.strip()
    expiration_month = expiration_month.strip()
    expiration_year = expiration_year.strip()
    cvv = cvv.strip()

    if "status" in result:
        status = result["status"]
        message = result["message"]
        formatted_response = (
            f"𝗣𝗮𝘀𝘀𝗲𝗱 ✅\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ {card_number}\n"
            f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ⇾ 3DS Lookup\n"
            f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {status}\n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ {message}\n"
            f"𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {status}\n"
            f"𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {status}\n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ {status}"
        )
    else:
        formatted_response = (
            f"𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ {card_number}\n"
            f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ⇾ 3DS Lookup\n"
            f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ \n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ \n"
            f"𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ \n"
            f"𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ \n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ "
        )

    return formatted_response

async def simulate_3d_secure_lookup(card_details):
    try:
        card_number, expiration_month, expiration_year, cvv = card_details.split('|')
        card_number = card_number.strip()
        expiration_month = expiration_month.strip()
        expiration_year = expiration_year.strip()
        cvv = cvv.strip()

        # Simulate authentication outcome
        authentication_outcome = random.choice(["authenticated", "not_authenticated", "attempted", "failed"])

        if authentication_outcome == "authenticated":
            return {"status": "authenticated", "message": "3D Secure authentication successful"}
        elif authentication_outcome == "not_authenticated":
            return {"status": "not_authenticated", "message": "3D Secure authentication not successful"}
        elif authentication_outcome == "attempted":
            return {"status": "attempted", "message": "3D Secure authentication attempted but not completed"}
        else:
            return {"status": "failed", "message": "3D Secure authentication failed"}

    except ValueError:
        return {"error": "Invalid card details format"}

async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")
                    
                    # Process bin_info as needed
                    return {"brand": brand, "card_type": card_type, "bank": bank, "country": country}

                except aiohttp.ContentTypeError:
                    return {"error": "Invalid JSON response"}

            else:
                return {"error": f"Failed to fetch data: {response.status}"}
