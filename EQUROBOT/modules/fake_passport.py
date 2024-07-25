import random
import string
from faker import Faker
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from EQUROBOT import app

def generate_fake_passport():
    fake = Faker()
    
    passport = {
        "Name": fake.name(),
        "Passport Number": ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)),
        "Date of Birth": fake.date_of_birth(minimum_age=18, maximum_age=100).strftime('%Y-%m-%d'),
        "Nationality": fake.country_code(),
        "Date of Issue": fake.date_this_decade().strftime('%Y-%m-%d'),
        "Date of Expiry": fake.date_between(start_date='+1y', end_date='+10y').strftime('%Y-%m-%d'),
        "Place of Birth": fake.city()
    }
    
    return passport

def create_passport_image(passport_details):
    # Create a blank image for the passport
    width, height = 600, 400
    image = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    
    # Add details to the image
    margin = 10
    offset = 10
    
    for key, value in passport_details.items():
        draw.text((margin, offset), f"{key}: {value}", font=font, fill=(0, 0, 0))
        offset += 30

    # Save the image
    image_path = "fake_passport.png"
    image.save(image_path)
    
    return image_path

@app.on_message(filters.command("generate_passport"))
async def send_fake_passport(client, message):
    passport_details = generate_fake_passport()
    
    details_text = "\n".join([f"{key}: {value}" for key, value in passport_details.items()])
    image_path = create_passport_image(passport_details)
    
    await message.reply_text(details_text)
    await message.reply_photo(photo=image_path)
