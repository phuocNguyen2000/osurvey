from os import access
import requests
from flask import jsonify,json
def get_access_token():
    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                }
    data={'grant_type': 'client_credentials'}
    response = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",
    auth=('AWclxyD8OVZu-UlkCAOMgFAcep_rbqGL5jhlazEw-HiXqFMpO6P6mOqLyByoC-BnwmkqZMnQlDT0itxE',
    'ELcrCDJE9TV6gxCRZnS0sWP7116Fa444UnqjBUqMRdzco713VJ9hiI2C67ndfU3GBUz1kUNfLMYOpcvL'), data=data, headers=headers)

    return response.json()["access_token"]
def create_checkout():
    headers={
                        'Content-Type': 'application/json',
                        'Authorization':'Bearer '+ get_access_token()
                }
    data={
  "intent": "sale",
  "payer": {
    "payment_method": "paypal"
  },
  "transactions": [
    {
      "amount": {
        "total": "30.11",
        "currency": "USD",
        "details": {
          "subtotal": "30.00",
          "tax": "0.07",
          "shipping": "0.03",
          "handling_fee": "1.00",
          "shipping_discount": "-1.00",
          "insurance": "0.01"
        }
      },
      "description": "The payment transaction description.",
      "custom": "EBAY_EMS_90048630024435",
      "invoice_number": "48787589674",
      "payment_options": {
        "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
      },
      "soft_descriptor": "ECHI5786786",
      "item_list": {
        "items": [
          {
            "name": "hat",
            "description": "Brown hat.",
            "quantity": "5",
            "price": "3",
            "tax": "0.01",
            "sku": "1",
            "currency": "USD"
          },
          {
            "name": "handbag",
            "description": "Black handbag.",
            "quantity": "1",
            "price": "15",
            "tax": "0.02",
            "sku": "product34",
            "currency": "USD"
          }
        ],
        "shipping_address": {
          "recipient_name": "Brian Robinson",
          "line1": "4th Floor",
          "line2": "Unit #34",
          "city": "San Jose",
          "country_code": "US",
          "postal_code": "95131",
          "phone": "011862212345678",
          "state": "CA"
        }
      }
    }
  ],
  "note_to_payer": "Contact us for any questions on your order.",
  "redirect_urls": {
    "return_url": "http://127.0.0.1:5000/checkout",
    "cancel_url": "https://example.com/cancel"
  }
}
    response = requests.post("https://api.sandbox.paypal.com/v1/payments/payment",data=json.dumps(data), headers=headers)

    s=None
    for link in response.json()["links"]:
      if link["method"]=='REDIRECT':
            s=link['href'].split("token=")[1]
    print(response.json())

create_checkout()