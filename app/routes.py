import json
import os

from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required

from app import app, socket, db


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #if user is not autheticated, display noauth index.html
    if not current_user.is_authenticated:
        return render_template('/noauth/index.html')
    #else if user is superuser display su index.html
    elif current_user.is_authenticated and current_user.is_superuser:
        return '',204
    # else if user is not superuser display user index.html
    elif current_user.is_authenticated and not current_user.is_superuser:
        return '', 204


@app.route('/login', methods=['GET'])
def login():
    return render_template('/noauth/login.html', title = 'Belépés')
