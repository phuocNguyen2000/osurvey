
from waitress import serve
from settings import app, db
import random
from datetime import datetime
import secrets
import json

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
def __call__(self, environ, start_response):
        return app(environ, start_response)