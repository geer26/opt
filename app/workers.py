
import json
import re
from random import SystemRandom
from os import environ

from flask import request

from app import db, fernet, logger
from flask_login import current_user
from datetime import datetime

from flask_mail import Message as MAIL

import smtplib
from email.message import EmailMessage

from app import mail

from app.models import User, Module, Modaux, Testbattery, Testsession, Client, Clientlog, Result, Userlog, Message


def validate_password(password):
    lowers = '[+a-z]'
    uppers = '[+A-Z]'
    digits = '[+0-9]'
    specs = '[+!@#$%^&*?_~]'
    if re.search(lowers,password) and re.search(uppers,password) and re.search(digits, password) and re.search(specs, password) and len(password) >= 8:
        return True
    return False


def hassu():
    for user in User.query.all():
        if user.is_superuser: return True
    return False


def generate_rnd(N):
    import string
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))


def get_sudata():
    '''

    return a json, format:
    {
    current_user{
        id: <id>,
        id : <id>,
        username : <username>
        description : <description> !
        contact : <contact> !
        is_superuser : <is_superuser>
        settings : <settings>
        added : <formatted string>
        last_modified : <formatted string>
    },
    users : [
        {
            id : <id>,
            username : <username>
            description : <description> !
            contact : <contact> !
            is_superuser : <is_superuser>
            settings : <settings>
            added : <formatted string>
            last_modified : <formatted string>
        }
    ]
    }

    '''

    data = {}

    users = []  #DONE
    modules = []  #DONE
    modauxs = []  #DONE
    testbatteries = []  #DONE
    testsessions = []  #DONE
    clients = []  #DONE
    clientlogs = []  #DONE
    results = []  #DONE


    cu = {}
    cu['id'] = current_user.id
    cu['username'] = current_user.username
    cu['description'] = current_user.get_description()
    cu['contact'] = current_user.get_contact()
    cu['is_superuser'] = current_user.is_superuser
    cu['settings'] = current_user.settings
    #cu['added'] = current_user.added
    cu['added'] = current_user.added.strftime("%Y-%m-%dT%H:%M:%S")
    #cu['last_modified'] = current_user.last_modified
    cu['last_modified'] = current_user.last_modified.strftime("%Y-%m-%dT%H:%M:%S")

    data['current_user'] = cu


    for user in User.query.all():
        u = {}
        u['id'] = user.id
        u['username'] = user.username
        u['description'] = user.get_description()
        u['contact'] = user.get_contact()
        u['is_superuser'] = user.is_superuser
        u['settings'] = user.settings
        #u['added'] = user.added
        u['added'] = user.added.strftime("%Y-%m-%dT%H:%M:%S")
        #u['last_modified'] = user.last_modified
        u['last_modified'] = user.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        users.append(u)

    data['users'] = users

    for module in Module.query.all():
        m = {}
        m['id'] = module.id
        m['uuid'] = module.uuid
        m['short_name'] = module.short_name
        m['verbose_name'] = module.verbose_name
        m['description'] = module.description
        m['attributes'] = module.attributes
        m['added'] = module.added.strftime("%Y-%m-%dT%H:%M:%S")
        m['last_modified'] = module.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        modules.append(module)

    data['modules'] = modules

    for modaux in Modaux.query.all():
        ma = {}
        ma[id] = modaux.id
        ma['user_id'] = module.user_id
        ma['module_id'] = module.module_id
        modauxs.append(ma)
    data['modaux'] = modauxs

    for testbattery in Testbattery.query.all():
        tb = {}
        tb['id'] = testbattery.id
        tb['user_id'] = testbattery.user_id
        tb['name'] = testbattery.name
        tb['description'] = testbattery.description
        tb['created'] = testbattery.created.strftime("%Y-%m-%dT%H:%M:%S")
        tb['last_modified'] = testbattery.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        tb['modules'] = testbattery.modules
        testbatteries.append(tb)
    data['testbatteries'] = testbatteries

    for testsession in Testsession.query.all():
        ts = {}
        ts['id'] = testsession.id
        ts['uuid'] = testsession.uuid
        ts['user_id'] = testsession.user_id
        ts['testbattery_id'] = testsession.testbattery_id
        ts['created'] = testsession.created.strftime("%Y-%m-%dT%H:%M:%S")
        ts['due'] = testsession.due.strftime("%Y-%m-%dT%H:%M:%S")
        ts['state'] = testsession.state
        ts['invitation_text'] = testsession.get_invitation()
        ts['added'] = testsession.added.strftime("%Y-%m-%dT%H:%M:%S")
        ts['last_modified'] = testsession.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        testsessions.append(ts)
    data['testsessions'] = testsessions

    for client in Client.query.all():
        c = {}
        c['id'] = client.id
        c['uuid'] = client.uuid
        c['name'] = client.get_name()
        c['email'] = client.get_email()
        c['state'] = client.state
        c['session_id'] = client.session_id
        c['invitation_status'] = client.invitation_status
        c['added'] = client.added.strftime("%Y-%m-%dT%H:%M:%S")
        c['last_modified'] = client.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        clients.append(c)
    data['clients'] = clients

    for clientlog in Clientlog.query.all():
        cl = {}
        cl['id'] = clientlog.id
        cl['client_id'] = clientlog.client_id
        cl['message'] = clientlog.message
        cl['source'] = clientlog.source
        cl['timestamp'] = clientlog.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        clientlogs.append(cl)
    data['clientlogs'] = clientlogs

    for result in Result.query.all():
        r = {}
        r['id'] = result.id
        r['client_id'] = result.client_id
        r['session_id'] = result.session_id
        r['module_id'] = result.module_id
        r['timestamp'] = result.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        r['result_raw'] = result.get_result()
        r['added'] = result.added.strftime("%Y-%m-%dT%H:%M:%S")
        r['last_modified'] = result.last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        results.append(r)
    data['results'] = results

    logger.upd_log(f'All data provided to IP: {request.access_route}', 1)

    return json.dumps(data)


def check_adduser(data):

    u = User.query.filter(User.username == str(data['username'])).all()
    num_of_su = len(User.query.filter(User.is_superuser).all())

    if len(u) != 0:
        logger.upd_log(f'Unsuccess user add from IP: {request.access_route}', 2)
        return 1 #User exists

    if not validate_password(str(data['password'])):
        logger.upd_log(f'Unsuccess user add from IP: {request.access_route}', 2)
        return 2 #invalid password

    user = User()
    user.username = str(data['username'])
    user.set_password(str(data['password']))
    user.set_description(str(data['description']))
    user.set_contact(str(data['contact']))

    if user.is_superuser and num_of_su < 5:
        user.is_superuser = data['is_superuser']

    elif user.is_superuser and num_of_su >= 5:
        logger.upd_log(f'Unsuccess user add from IP: {request.access_route}', 2)
        return 3  # su munber exceeded

    db.session.add(user)
    db.session.commit()

    logger.upd_log(f'User \"{user.username}\" added from IP: {request.access_route}', 0)

    return 0


def del_user(data):
    user = User.query.get(int(data['id']))
    if not user:
        logger.upd_log(f'Unsuccess user delete from IP: {request.access_route}', 2)
        return 1
    else:
        db.session.delete(user)
        db.session.commit()
        logger.upd_log(f'User \"{user.username}\" deleted from IP: {request.access_route}', 0)
    return 0


def reset_db():

    for user in User.query.all():
        if not user.is_superuser:
            db.session.delete(user)
            db.session.commit()

    Module.query.delete()
    Modaux.query.delete()
    Testbattery.query.delete()
    Testsession.query.delete()
    Client.query.delete()
    Clientlog.query.delete()
    Result.query.delete()
    Userlog.query.delete()
    Message.query.delete()
    db.session.commit()
    logger.upd_log('Database wiped except superusers', 1)

    return 0


def sendmail(data):

    print (data)

    """msg = MAIL(data['subject'], recipients=[data['recepient']])
    msg.body = data['body']
    #msg.html = html_body
    mail.send(msg)"""

    fromaddr = environ.get('MAIL_DEFAULT_SENDER')
    toaddr = str(data['recepient'])
    subject = data['subject']
    body = data['body']

    server = smtplib.SMTP('localhost', 25)
    server.connect("localhost", 25)
    server.ehlo()
    server.starttls()

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = fromaddr
    msg["To"] = toaddr

    server.send_message(msg)

    #server.sendmail(fromaddr, toaddr, text)

    server.quit()

    return 0


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
