import requests
import datetime
import telebot
import time
import mysql.connector
import json
from pyrogram import filters
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from mysql.connector import Error
from EQUROBOT import app

def find_captcha(response_text):
    response_text_lower = response_text.lower()
    if 'recaptcha' in response_text_lower:
        return 'Using Google reCAPTCHA ✅'
    elif 'hcaptcha' in response_text_lower:
        return 'Using hCaptcha ✅'
    return 'Not using Any Captcha 🚫'

def detect_cloudflare(response):
    cloudflare_elements = ["cloudflare.com", "__cfduid"]
    cloudflare_headers = ["cf-ray", "cf-cache-status", "server"]

    response_text_lower = response.text.lower()
    if any(element in response_text_lower for element in cloudflare_elements):
        return True
    if any(header in response.headers for header in cloudflare_headers):
        return True
    return False

def find_payment_gateways(response_text):
    detected_gateways = []
    lower_text = response_text.lower()

    gateways = {
        "paypal": "PayPal",
        "stripe": "Stripe",
        "braintree": "Braintree",
        "square": "Square",
        "authorize.net": "Authorize.Net",
        "2checkout": "2Checkout",
        "adyen": "Adyen",
        "worldpay": "Worldpay",
        "sagepay": "SagePay",
        "checkout.com": "Checkout.com",
        "skrill": "Skrill",
        "neteller": "Neteller",
        "payoneer": "Payoneer",
        "klarna": "Klarna",
        "afterpay": "Afterpay",
        "sezzle": "Sezzle",
        "alipay": "Alipay",
        "wechat pay": "WeChat Pay",
        "tenpay": "Tenpay",
        "qpay": "QPay",
        "sofort": "SOFORT Banking",
        "giropay": "Giropay",
        "trustly": "Trustly",
        "zelle": "Zelle",
        "venmo": "Venmo",
        "epayments": "ePayments",
        "revolut": "Revolut",
        "wise": "Wise (formerly TransferWise)",
        "shopify payments": "Shopify Payments",
        "woocommerce": "WooCommerce",
        "paytm": "Paytm",
        "phonepe": "PhonePe",
        "google pay": "Google Pay",
        "bhim upi": "BHIM UPI",
        "razorpay": "Razorpay",
        "instamojo": "Instamojo",
        "ccavenue": "CCAvenue",
        "payu": "PayU",
        "mobikwik": "MobiKwik",
        "freecharge": "FreeCharge",
        "cashfree": "Cashfree",
        "jio money": "JioMoney",
        "yandex.money": "Yandex.Money",
        "qiwi": "QIWI",
        "webmoney": "WebMoney",
        "paysafe": "Paysafe",
        "bpay": "BPAY",
        "mollie": "Mollie",
        "paysera": "Paysera",
        "multibanco": "Multibanco",
        "pagseguro": "PagSeguro",
        "mercadopago": "MercadoPago",
        "payfast": "PayFast",
        "billdesk": "BillDesk",
        "paystack": "Paystack",
        "interswitch": "Interswitch",
        "voguepay": "VoguePay",
        "flutterwave": "Flutterwave",
    }

    for key, value in gateways.items():
        if key in lower_text:
            detected_gateways.append(value)

    if not detected_gateways:
        detected_gateways.append("Unknown")

    return detected_gateways

def find_stripe_version(response_text):
    response_text_lower = response_text.lower()
    if 'stripe3dsecure' in response_text_lower:
        return "3D Secured ✅"
    elif 'stripe-checkout' in response_text_lower:
        return "Checkout external link 🔗"
    return "2D site ACTIVE 📵"

def find_payment_gateway(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        detected_gateways = find_payment_gateways(response.text)
        return detected_gateways
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return ["Error"]

@app.on_message(filters.command("gate"))
async def check_payment_gateways(_, message):
    try:
        processing_message = await message.reply("**Processing your request...**", disable_web_page_preview=True)

        website_url = message.text[len('/gate'):].strip()
        if not website_url.startswith(("http://", "https://")):
            website_url = "http://" + website_url  

        response = requests.get(website_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        detected_gateways = find_payment_gateways(response.text)
        detected_captcha = find_captcha(response.text)
        is_cloudflare_protected = detect_cloudflare(response)

        result_message = (
            f"┏━━━━━━━⍟\n"
            f"┃ 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 : ✅\n"
            f"┗━━━━━━━━━━━━⊛\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
            f"•➥ 𝗦𝗶𝘁𝗲 -» `{website_url}`\n"
            f"•➥ 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀: {', '.join(detected_gateways)}\n"
            f"•➥ 𝗖𝗮𝗽𝘁𝗰𝗵𝗮: {detected_captcha}\n"
            f"•➥ 𝗖𝗹𝗼𝘂𝗱𝗳𝗹𝗮𝗿𝗲 𝗣𝗿𝗼𝘁𝗲𝗰𝘁𝗶𝗼𝗻: {'✅' if is_cloudflare_protected else '🚫'}\n\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        )
        await processing_message.edit_text(result_message, disable_web_page_preview=True)

    except requests.RequestException:
        await processing_message.edit_text("**Error: In Fetching Details. Please check if the link is reachable or not.**", disable_web_page_preview=True)
        
