import json
import os

from flask import render_template

from app import app, socket, db


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('base.html')
