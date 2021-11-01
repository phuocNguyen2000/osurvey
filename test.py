# from os import access
# import requests
# from flask import jsonify,json
# def get_access_token():
#     headers={
#                         'Content-Type': 'application/x-www-form-urlencoded'
#                 }
#     data={'grant_type': 'client_credentials'}
#     response = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",
#     auth=('AWclxyD8OVZu-UlkCAOMgFAcep_rbqGL5jhlazEw-HiXqFMpO6P6mOqLyByoC-BnwmkqZMnQlDT0itxE',
#     'ELcrCDJE9TV6gxCRZnS0sWP7116Fa444UnqjBUqMRdzco713VJ9hiI2C67ndfU3GBUz1kUNfLMYOpcvL'), data=data, headers=headers)

#     return response.json()["access_token"]
# def create_checkout():
#     headers={
#                         'Content-Type': 'application/json',
#                         'Authorization':'Bearer '+ get_access_token()
#                 }
#     data={
#   "intent": "sale",
#   "payer": {
#     "payment_method": "paypal"
#   },
#   "transactions": [
#     {
#       "amount": {
#         "total": "30.11",
#         "currency": "USD",
#         "details": {
#           "subtotal": "30.00",
#           "tax": "0.07",
#           "shipping": "0.03",
#           "handling_fee": "1.00",
#           "shipping_discount": "-1.00",
#           "insurance": "0.01"
#         }
#       },
#       "description": "The payment transaction description.",
#       "custom": "EBAY_EMS_90048630024435",
#       "invoice_number": "48787589674",
#       "payment_options": {
#         "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
#       },
#       "soft_descriptor": "ECHI5786786",
#       "item_list": {
#         "items": [
#           {
#             "name": "hat",
#             "description": "Brown hat.",
#             "quantity": "5",
#             "price": "3",
#             "tax": "0.01",
#             "sku": "1",
#             "currency": "USD"
#           },
#           {
#             "name": "handbag",
#             "description": "Black handbag.",
#             "quantity": "1",
#             "price": "15",
#             "tax": "0.02",
#             "sku": "product34",
#             "currency": "USD"
#           }
#         ],
#         "shipping_address": {
#           "recipient_name": "Brian Robinson",
#           "line1": "4th Floor",
#           "line2": "Unit #34",
#           "city": "San Jose",
#           "country_code": "US",
#           "postal_code": "95131",
#           "phone": "011862212345678",
#           "state": "CA"
#         }
#       }
#     }
#   ],
#   "note_to_payer": "Contact us for any questions on your order.",
#   "redirect_urls": {
#     "return_url": "http://127.0.0.1:5000/checkout",
#     "cancel_url": "https://example.com/cancel"
#   }
# }
#     response = requests.post("https://api.sandbox.paypal.com/v1/payments/payment",data=json.dumps(data), headers=headers)

#     s=None
#     for link in response.json()["links"]:
#       if link["method"]=='REDIRECT':
#             s=link['href'].split("token=")[1]
#     print(response.json())

# create_checkout()

# import datetime

# year=str(datetime.datetime.now().year)
# month=str(datetime.datetime.now().month)
# day=str(datetime.datetime.now().day)
# hour=str(datetime.datetime.now().hour)
# minu=str(datetime.datetime.now().minute)
# second=str(datetime.datetime.now().second)
# print(year+month+day+hour+minu+second)
# import fcm_manager
# fcm_manager.sendPush(title="Wellcome to oSurvey",msg="Hello",re_token= ['fnZaLKjcSA6B8GshGewNM1:APA91bEwxgS5KYYnueFT-2FjjdK2EYawGkYmHplynQyYUWCyCK15jFvvoNCTj_1lqI1s9cY6R4EF6CTr5_ansgd6D7XtHLNPTn3Ej46otmFSnGJvftoFRrqti45e1ptK4Tuu-J4X08ti'])
S="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDNUmkJpLA0JzHY\nKtIFfHbkrc2ljCzrJYGaYzcNbRkE0JvZiGwXVJE2Pi7MJKL7twOZ0t7/CmWaEuiv\n5cVkG3l6oAJJBf/duZrdjmZ91vBJsfZmFDQbuvt46Pn+naZzg5MGz8YOHSOaNWoK\nQb7mDVWPGvKgxleunVFoQ5lwovhUaSBUJhwxEWKHYNnX2BDPqz2NiyXTtHD3sluT\nPM06dkPfokZrCB3hP9LlervctP/UvtMZcQfLWCpn9eOaACaGXWf/TJ81H3Vu7Kau\npl06nQtLiZ/fVAn1TO5CAKcY7dRimwwSQGRBphCUUNTeyfTNLH9iRzQTkeaFyIpR\nxP/pOoqpAgMBAAECggEAVacA2XyB4yfMo9RtK8u533jf1qVM4cWSNOEZyLiP3NHX\nih5elTb6oum65P+NnDtDPcrZqwRf0S/9MM/GEhZiDXUtrt/ZVtpEUBPFDs75C405\ncGkSOdU9bbmm/IAwvXSQg6Fuilm+jeildWTq6ZZ7cEj6GXbUgivvl3LH0lSyCqfX\nAZbVVDA5pyILONUU+XtGu7sY2r7KdbdSNj/4ltxiA7E0XWqAf+sEfbgjO/572O5l\nqmG/Ch/b/DzmbX0ODHZ3y1cbD3ZObEIb5Y9nrIaybzLSYgj1c7YqAn9eeQ4Hq5Au\nvrn5ubFxgOMfhclZrlOxHth4tX+G5U98ZbmUVe0zLwKBgQDnUhagnbdC5m+5eAXE\niwxCp2rzoF9JzIwarwHCSQL5HqnIyOfc8C/ahlwwhsoYTXrq5BYxrbMVsCkZjYKE\nGdWAeoMYDx7u+gEojJhUNfKJudTeQmX+aW8pGgMEubTaWfYwDKuEU5qq2WjXMqQs\nrXC/TAMMm1lVuue/ztBP2shy+wKBgQDjOjwtNwU28hrfEp6IRAArRGuT/gJq8XiI\niZtMgBMOrOIl+TgqLw8+0BF33zFTbqeyD1pYdKKMCNbrVVAPkBgeHHF8fLiNSXZk\nmxs//RxXbIeVuMimsBpWYbNcgU+tTnAhHO7B+nWSLTtL2LOSjpi6/iT1V1Ls7uf8\nMsFuFrynqwKBgBwpr12Qth4sBhAzn6glMbHvxiKxNMi8YZZiFjm8P+Nqq0spwqjw\niTL2xsSVtIcu77cnW9hiiHosf2SACRLiPk8tG0bTmHWJ9JgmPemKw+Omv1bsCJTn\n60O6ygFKRs2KxGFnOX6b2ynP3GbO4JQb7a0sqPZg94hrgAmnOU9vmJX/AoGBAKf3\ne1Y9DrjAHMb7H39BLRLOv+sk4Cqnlt7vQYI6RlwZxg4l/LOKF+3pppACx5aR/Jpu\nKO2sQh/bxOsvJEBs1rcjdWx9UXr3a/IQigMyGgox6sPtVT2Kfd2O2SQvXnOQwOhp\nV8DCYLiOgP+fD5btm87WYQGO7HjCXXAbIMs9OXWDAoGACGCU0JCEyjKf6ErFPnNx\npwXrsqVAILwaSCXUu5EBU+aUgoM/e0WKwudiur4EXxEXi4agys/fZJBHXNxfCvGy\n4vIg7QQ2mY/48VSZvRRi78NEsEgfWiHak3aOsgxyydlYKwJWlJM3GXS64AcM34Av\nwkpCt+DTKgCS0aPUbVqAoj8=\n-----END PRIVATE KEY-----\n"
import re

g=re.sub('\n', '/\\n/g', S)
print(g);
