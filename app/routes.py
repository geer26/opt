import json
import os

from flask import render_template, redirect, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, AddUserForm
from app import app, socket, db, logger
from app.workers import hassu, generate_rnd, get_sudata, check_adduser, del_user, reset_db
from app.backup import backup_db, restore_db, upd_log, check_backup
from app.models import User


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #if user is not autheticated, display noauth index.html
    if not current_user.is_authenticated:
        logger.upd_log(f'Non-auth visit from IP: {request.access_route}', 0)
        return render_template('/noauth/index.html')
    #else if user is superuser display admin index.html
    elif current_user.is_authenticated and current_user.is_superuser:
        adduserform = AddUserForm()
        logger.upd_log(f'Admin visit from IP: {request.access_route}, admin: {current_user.username}', 0)
        return render_template('/admin/index-admin.html', data = get_sudata(), adduserform = adduserform)
    # else if user is not superuser display user index.html
    elif current_user.is_authenticated and not current_user.is_superuser:
        logger.upd_log(f'User visit from IP: {request.access_route}, user: {current_user.username}', 0)
        return render_template('/user/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        logger.upd_log(f'{current_user.username} tried to reach loginsite, redirected to /', 1)
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST' and not current_user.is_authenticated:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                mess = {}
                mess['event'] = 1109
                socket.emit('generic', mess)
                logger.upd_log(f'Login attempt with invalid username: {form.username.data} from IP: {request.access_route}', 2)
                return '',204

            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                logger.upd_log(f'Successful login: {form.username.data} from IP: {request.access_route}', 0)
                return redirect('/')

            else:
                mess = {}
                mess['event'] = 1109
                socket.emit('generic', mess)
                logger.upd_log(f'Login attempt with invalid password: {form.username.data} from IP: {request.access_route}', 2)
                return '', 204

    return render_template('/noauth/login.html', title = 'Belépés', form = form)


@login_required
@app.route('/logout')
def logout():
    logger.upd_log(f'User logged out from ip: {request.access_route}, user: {current_user.username}', 0)
    logout_user()
    return redirect('/')


@login_required
@app.route('/getbackup', methods=['GET', 'POST'])
def get_backup():
    if not current_user.is_superuser:
        logger.upd_log(f'{current_user.username} tried to download backups from IP: {request.access_route}', 2)
        return '', 204
    logger.upd_log(f'Backup downloaded by: {current_user.username} from IP: {request.access_route}', 1)
    return send_from_directory(directory=app.config['BACKUP_FOLDER'], filename='backup.zip')


@login_required
@app.route('/getlog/<log>', methods=['GET', 'POST'])
def get_log(log):
    if not current_user.is_superuser:
        logger.upd_log(f'{current_user.username} tried to download logs from IP: {request.access_route}', 2)
        return '', 204
    if log == 'archive':
        logger.upd_log(f'Log archive downloaded by: {current_user.username} from IP: {request.access_route}', 1)
        return send_from_directory(directory=app.config['LOG_FOLDER'], filename='log_archive.zip')
    if log == 'current':
        logger.upd_log(f'Current log downloaded by: {current_user.username} from IP: {request.access_route}', 1)
        return send_from_directory(directory=app.config['LOG_FOLDER'], filename='log.file')
    else:
        logger.upd_log(f'Log download failed from IP: {request.access_route}', 3)
        return '', 204

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
        login_user(user, remember=True)
        logger.upd_log(f'First admin: {suname} added and logged in from IP: {request.access_route}', 1)

    return redirect('/')


@socket.on('admin')
def new_admin_message(data):

    if not current_user.is_authenticated or not current_user.is_superuser:
        logger.upd_log(f'Non-superuser tried to reach ws admin namespace from IP {request.access_route}', 2)
        return False

    # where to send the answer -> sid
    sid = request.sid

    #check adduser creditentials
    if data['event'] == 2201:
        mess = {}
        mess['event'] = 1201
        mess['status'] = check_adduser(data)

        if mess['status'] == 0 :
            mess['new_users'] = json.dumps(json.loads(get_sudata())['users'])

        socket.emit('admin', mess, room=sid)
        logger.upd_log(f'{current_user.username} adder new user with status code {mess["status"]}', 1)
        return True


    #del user by id
    if data['event'] == 2251:
        mess = {}
        mess['event'] = 1251
        mess['status'] = del_user(data)
        mess['new_users'] = json.dumps(json.loads(get_sudata())['users'])
        socket.emit('admin', mess, room=sid)
        return True


    #request for refreshed logfile as json
    if data['event'] == 2801:
        mess = {}
        mess['event'] = 1801
        mess['data'] = logger.return_json()
        socket.emit('admin', mess, room=sid)
        return True


    #backup entire db
    if data['event'] == 2851:
        mess = {}
        mess['event'] = 1850
        mess['status'] = backup_db()
        socket.emit('admin', mess, room=sid)
        return True


    #restore entire db
    if data['event'] == 2871:
        mess = {}
        mess['event'] = 1871
        mess['status'] = restore_db()
        socket.emit('admin', mess, room=sid)
        return True


    #reset entire db
    if data['event'] == 2899:
        mess = {}
        mess['event'] = 1899
        mess['status'] = reset_db()
        socket.emit('admin', mess, room=sid)
        return True