import firebase_admin
from firebase_admin import messaging
import re


from firebase_admin import credentials
s="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDNUmkJpLA0JzHY\nKtIFfHbkrc2ljCzrJYGaYzcNbRkE0JvZiGwXVJE2Pi7MJKL7twOZ0t7/CmWaEuiv\n5cVkG3l6oAJJBf/duZrdjmZ91vBJsfZmFDQbuvt46Pn+naZzg5MGz8YOHSOaNWoK\nQb7mDVWPGvKgxleunVFoQ5lwovhUaSBUJhwxEWKHYNnX2BDPqz2NiyXTtHD3sluT\nPM06dkPfokZrCB3hP9LlervctP/UvtMZcQfLWCpn9eOaACaGXWf/TJ81H3Vu7Kau\npl06nQtLiZ/fVAn1TO5CAKcY7dRimwwSQGRBphCUUNTeyfTNLH9iRzQTkeaFyIpR\nxP/pOoqpAgMBAAECggEAVacA2XyB4yfMo9RtK8u533jf1qVM4cWSNOEZyLiP3NHX\nih5elTb6oum65P+NnDtDPcrZqwRf0S/9MM/GEhZiDXUtrt/ZVtpEUBPFDs75C405\ncGkSOdU9bbmm/IAwvXSQg6Fuilm+jeildWTq6ZZ7cEj6GXbUgivvl3LH0lSyCqfX\nAZbVVDA5pyILONUU+XtGu7sY2r7KdbdSNj/4ltxiA7E0XWqAf+sEfbgjO/572O5l\nqmG/Ch/b/DzmbX0ODHZ3y1cbD3ZObEIb5Y9nrIaybzLSYgj1c7YqAn9eeQ4Hq5Au\nvrn5ubFxgOMfhclZrlOxHth4tX+G5U98ZbmUVe0zLwKBgQDnUhagnbdC5m+5eAXE\niwxCp2rzoF9JzIwarwHCSQL5HqnIyOfc8C/ahlwwhsoYTXrq5BYxrbMVsCkZjYKE\nGdWAeoMYDx7u+gEojJhUNfKJudTeQmX+aW8pGgMEubTaWfYwDKuEU5qq2WjXMqQs\nrXC/TAMMm1lVuue/ztBP2shy+wKBgQDjOjwtNwU28hrfEp6IRAArRGuT/gJq8XiI\niZtMgBMOrOIl+TgqLw8+0BF33zFTbqeyD1pYdKKMCNbrVVAPkBgeHHF8fLiNSXZk\nmxs//RxXbIeVuMimsBpWYbNcgU+tTnAhHO7B+nWSLTtL2LOSjpi6/iT1V1Ls7uf8\nMsFuFrynqwKBgBwpr12Qth4sBhAzn6glMbHvxiKxNMi8YZZiFjm8P+Nqq0spwqjw\niTL2xsSVtIcu77cnW9hiiHosf2SACRLiPk8tG0bTmHWJ9JgmPemKw+Omv1bsCJTn\n60O6ygFKRs2KxGFnOX6b2ynP3GbO4JQb7a0sqPZg94hrgAmnOU9vmJX/AoGBAKf3\ne1Y9DrjAHMb7H39BLRLOv+sk4Cqnlt7vQYI6RlwZxg4l/LOKF+3pppACx5aR/Jpu\nKO2sQh/bxOsvJEBs1rcjdWx9UXr3a/IQigMyGgox6sPtVT2Kfd2O2SQvXnOQwOhp\nV8DCYLiOgP+fD5btm87WYQGO7HjCXXAbIMs9OXWDAoGACGCU0JCEyjKf6ErFPnNx\npwXrsqVAILwaSCXUu5EBU+aUgoM/e0WKwudiur4EXxEXi4agys/fZJBHXNxfCvGy\n4vIg7QQ2mY/48VSZvRRi78NEsEgfWiHak3aOsgxyydlYKwJWlJM3GXS64AcM34Av\nwkpCt+DTKgCS0aPUbVqAoj8=\n-----END PRIVATE KEY-----\n".replace('\\n', '\n')
g=re.sub('/\\n/g', '\n', s)

key={
  "type": "service_account",
  "project_id": "esurvey-ee4c3",
  "private_key_id": "fe590e2c41d337bea1c84edab045d2f7a329404c",
  "private_key":s ,
  "client_email": "firebase-adminsdk-styad@esurvey-ee4c3.iam.gserviceaccount.com",
  "client_id": "112825693966029201082",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-styad%40esurvey-ee4c3.iam.gserviceaccount.com"
}


cred=credentials.Certificate("./serviceAccountkey.json")
default_app = firebase_admin.initialize_app(cred)

def sendPush(title,msg,re_token,dataObj=None):
    message=messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObj,
        tokens=re_token
    )

    response=messaging.send_multicast(message)
    print(response)