import json
import os

from flask import render_template, redirect
from flask_login import current_user, login_user, logout_user, login_required

from app import app, socket, db
from app.workers import hassu, generate_rnd
from app.models import User


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


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/addsu/<suname>/<password>')
def addsu(suname, password):
    if not hassu():

        user = User()
        user.username = suname
        user.set_description('Adminisztrátor felhasználó')
        user.set_contact('none@none.no')
        user.set_password(password)
        user.is_superuser = True
        user.settings = ''
        db.session.add(user)
        db.session.commit()

    return redirect('/')
