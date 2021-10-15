import firebase_admin
from firebase_admin import messaging


from firebase_admin import credentials 
cred=credentials.Certificate("./serviceAccountKey.json")
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