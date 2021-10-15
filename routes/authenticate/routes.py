from settings import app,db
from flask import request
import requests

@app.route('/authenticate',methods=["POST"])
def authenticate():
    url = 'https://api.fpt.ai/vision/idr/vnm'
    files = {'image': open('CCT.jpg', 'rb').read()}
    headers = {
        'api-key': 'WcmSvRQOcQlgftS5INh8DRNxpCPyDZx9'
    }

    response = requests.post(url, files=files, headers=headers)

    print(response.text)
    
    return "ok"