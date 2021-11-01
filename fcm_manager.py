import firebase_admin
from firebase_admin import messaging

key={
  "type": "service_account",
  "project_id": "esurvey-ee4c3",
  "private_key_id": "d043f2db7a4c63d0b0e4aaf9e9d3f3a8c595ab16",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcPTLj9Rm+tggx\nnspCAf1JJvye/gIb8MVctcajhSkA0gz+IR8GEUXTq+zxvLTi0y7eHDQZlx+eery1\nUiBycW7GCDfgvIu8f+kHl6EYohSkgaMwr3yHgsD+GYMwCf6+t/SSor+j53wnGy3d\ny/VlXFR03wDrZSEGDQmrUiulEgiLkoV9EFxLokC4Clyzzw2KaPdzH18rfgEfjcf1\n92u1G5Cxsw66LbgapWNGLfHM02KSub/ozEx4ZSsEeQWDWkmT0pa69WaVl2YAvH2J\nf1WJ4rWlC0Eg6CYkWNNO3xWYG9gF6759rXrll6sTWN0d5l6jh/MPslVysPST/KVW\nuE44h4f/AgMBAAECggEAHRBpIjLQPki2IBuSbs+QZhJNDYumf5rF5jbe4JQhax2i\niqRC/IFUXlthSNgxuX/2aWf+FXp0uRdSxqLwlpRoR/NXBxjFYA+JPcVBhIdZ2LPQ\nSLZ/5T+DdIUCuQON/gviAg/pi8RwBUEi9mgvbubrsQNU6GZPdgWhHF4bAGJhhPmH\nDt1JZOlVtHXw44rkniHNj+68TDvCGPAvufKWaEFY1wm7mJiRljSasDvV0PqFDtwK\n9dVeE2l6tMOe7tn54SgxXOTbmWpIRc1Woq8b6Ek+EfpiX/gIsco+AZ8br89I5bxo\nuznS+1dXIY6aBWbOw5AM4zWT9yjfz7Snb0USVp8CcQKBgQDzzai82L8d/FDvUsc0\n+oupYUA4BGdA/TaT+1wHBoJygQFWotUI1NunyNFYkn46ufeubB3e27cPm2VKDnZU\nyYlV3ZPX1fdSvaGRcT24YgcisnBMy9J2+HXrhB9ElcO6rDMHCKJszoTLinaL9jYI\nw3o9fryAr4Kc4K8dQF+cFL088wKBgQDnQcGjcuKp33jHz/AuVPzT/N3dC5Q5iFBb\nDACiYgAxJHtp/zAgmQRzseVeVuBzri42SxT3DRMKE9HP8g0yZ0g2PF7hBz2sr5w9\nxSq+x4Z0KsXD5XsX//jGpOM3/WHSfdqf09hfsTh9l292RfRzKw4wcpjA/NEdDj1l\nPZS8cx4bxQKBgEVFkQUfXKYrc9+cGIfgDGCzBikkbyYTDDfdupcwbU4Vg4jXOUqK\nGGNC9uCAtyb+gfZoN9CDgy8HCy+QjmSm4sOn8oLoA57ZzJdjopLKH5bnNmtLmmA9\nVlv1rWCyYOugU9tSw7vArhCbJfW8nju9NvVUFkFGHQlv+bGJAeF6Lw6rAoGAGaK3\ndYgJym0EdZn+dRRkxpc0fQmIj+wlhEJLW7Tjco8pwzFPw31S+gRReejFju1TIB+o\nnk5ruuVBj/y0K885ORHuLqHf22HIPyy5NVbm97+6FqI8yAdPK64hphZHns7mymrw\nhIMf0QRVjdXpaE7wjrxVZKdiAweOFMgD0fQs9UUCgYEAuNq+Ijkr5732vGBPnF3c\n49hxp1qi7P/0SD+MjE33pNYdQqSegkUS9N5LA04hRrFjkzLYeMmlk6aIPinZx4sN\nKzkP4yMvxDuCYMdnNzP/3NSbgDyLtrFAUzKKno+vA0Kg4QIJ5PmJSnAbBW0c4Iyo\nNmfy6fTsLRHRaUBdURN/2pY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-styad@esurvey-ee4c3.iam.gserviceaccount.com",
  "client_id": "112825693966029201082",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-styad%40esurvey-ee4c3.iam.gserviceaccount.com"
}
 
from firebase_admin import credentials 
cred=credentials.Certificate(key)
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