import json
import os

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, AddUserForm
from app import app, socket, db
from app.workers import hassu, generate_rnd, get_sudata, check_adduser, del_user
from app.models import User


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #if user is not autheticated, display noauth index.html
    if not current_user.is_authenticated:
        return render_template('/noauth/index.html')
    #else if user is superuser display admin index.html
    elif current_user.is_authenticated and current_user.is_superuser:
        adduserform = AddUserForm()
        return render_template('/admin/index.html', data = get_sudata(), adduserform = adduserform)
    # else if user is not superuser display user index.html
    elif current_user.is_authenticated and not current_user.is_superuser:
        return render_template('/user/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST' and not current_user.is_authenticated:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                mess = {}
                mess['event'] = 1109
                socket.emit('generic', mess)
                return '',204

            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')

            else:
                mess = {}
                mess['event'] = 1109
                socket.emit('generic', mess)
                return '', 204

    return render_template('/noauth/login.html', title = 'Belépés', form = form)


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


@socket.on('admin')
def new_admin_message(data):

    if not current_user.is_authenticated or not current_user.is_superuser:
        return False

    # where to send the answer -> sid
    sid = request.sid

    #check adduser creditentials
    if data['event'] == 2201:
        mess = {}
        mess['event'] = 1201
        mess['status'] = check_adduser(data)
        mess['userdata'] = get_sudata()
        socket.emit('admin', mess, room=sid)
        return True


    #del user by id
    if data['event'] == 2251:
        mess = {}
        mess['event'] = 1251
        mess['status'] = del_user(data)
        mess['userdata'] = get_sudata()
        socket.emit('admin', mess, room=sid)
        return True