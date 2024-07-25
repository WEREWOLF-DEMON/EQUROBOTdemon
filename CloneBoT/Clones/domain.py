import aiohttp
import whois
from PIL import Image, ImageEnhance
from io import BytesIO
from pyrogram import Client, filters
from EQUROBOT import app

# Define a function to generate Carbon image
async def make_carbon(text):
    url = "https://carbonara.solopov.dev/api/cook"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": text}) as resp:
            image_data = await resp.read()

    # Open the image using PIL
    carbon_image = Image.open(BytesIO(image_data))

    # Increase brightness
    enhancer = ImageEnhance.Brightness(carbon_image)
    bright_image = enhancer.enhance(1.7)  # Adjust the enhancement factor as needed

    # Save the modified image to BytesIO object with increased quality
    output_image = BytesIO()
    bright_image.save(output_image, format='PNG', quality=95)  # Adjust quality as needed
    output_image.name = "carbon.png"
    return output_image

# Define a handler for domain messages
@app.on_message(filters.command("domain"))
async def domain_info(client, message):
    # Get the domain name after the command
    domain_name = " ".join(message.command[1:])
    
    # Get WHOIS information
    try:
        domain_info = whois.whois(domain_name)
        info_text = str(domain_info)
    except whois.parser.PywhoisError as e:
        info_text = str(e)
    
    # Generate Carbon image based on WHOIS information
    image = await make_carbon(info_text)
    
    # Send the Carbon image
    await client.send_photo(message.chat.id, photo=image)
