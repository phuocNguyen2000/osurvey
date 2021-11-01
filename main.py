
from settings import app, db
import random
from datetime import datetime
import secrets
import json

if __name__ == '__main__':
    app.run(debug=False,host='https://osurvey-server.herokuapp.com')
