from pyrogram import Client, filters, enums
import psutil
from EQUROBOT import app

def get_ram_usage():
    ram = psutil.virtual_memory()
    return ram.percent

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

@app.on_message(filters.command("ping", prefixes="."))
async def statuschk(client, message):
    ram_usage = get_ram_usage()
    cpu_usage = get_cpu_usage()

    await message.reply_text(f'''
I am alive, my dear genius master.

{chr(0x1D04)}{chr(0x1D00)}{chr(0x1D1B)}{chr(0x1D07)} {chr(0x1D05)}{chr(0x1D07)} {chr(0x1D1A)}{chr(0x1D07)}{chr(0x1D04)}{chr(0x1D05)}{chr(0x1D07)}{chr(0x1D0F)}{chr(0x1D0F)}

{chr(0x1D05)}{chr(0x1D07)}{chr(0x1D1C)}{chr(0x1D1A)} {chr(0x1D05)}{chr(0x1D07)}{chr(0x1D00)}{chr(0x1D0F)}{chr(0x1D18)}{chr(0x1D1A)}: {chr(0x1D0F)}{chr(0x1D13)} ✅
{chr(0x1D1B)}{chr(0x1D00)}{chr(0x1D10)} {chr(0x1D1C)}{chr(0x1D1A)}{chr(0x1D04)}{chr(0x1D07)}: {ram_usage}%
{chr(0x1D04)}{chr(0x1D18)}{chr(0x1D1C)} {chr(0x1D1C)}{chr(0x1D1A)}{chr(0x1D04)}{chr(0x1D07)}: {cpu_usage}%
{chr(0x1D05)}{chr(0x1D0F)}{chr(0x1D1B)} {chr(0x1D0D)}{chr(0x1D00)}{chr(0x1D03)} {chr(0x1D07)}{chr(0x1D18)}: [MR°᭄DAXX ࿐](https://t.me/YourExDestiny)
    ''', parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
