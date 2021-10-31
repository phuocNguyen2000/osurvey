
from settings import app, db
import random
from datetime import datetime
import secrets
import json
from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080,threads =  6)
