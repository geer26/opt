import json
import os

from app import app, socket, db


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return('HELLO WORLD!')
