import json
import os

from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required

from app import app, socket, db


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return render_template('/noauth/index.html')
