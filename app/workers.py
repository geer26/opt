import copy
import json
import os
import re
from random import SystemRandom
from app import db, app, fernet
import pickle
from flask_login import current_user
from datetime import datetime
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



    return json.dumps(data)


def check_adduser(data):

    u = User.query.filter(User.username == str(data['username'])).all()

    if len(u) != 0:
        return 1 #User exists

    if not validate_password(str(data['password'])):
        return 2 #invalid password

    user = User()
    user.username = str(data['username'])
    user.set_password(str(data['password']))
    user.set_description(str(data['description']))
    user.set_contact(str(data['contact']))
    user.is_superuser = data['is_superuser']

    db.session.add(user)
    db.session.commit()

    return 0


def del_user(data):
    user = User.query.get(int(data['id']))
    if not user: return 1
    else:
        db.session.delete(user)
        db.session.commit()
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

    return 0


def backup_db():
    #all tables as one JSON string ->
    entire_db = {}

    #user
    backup_user()

    #module
    backup_modules()

    #modaux
    backup_modaux()

    #testbattery
    backup_testbattery()

    #testsession
    backup_testsession()

    #client
    backup_client()

    #clientlog
    backup_clientlog()

    #result
    backup_result()

    #userlog
    backup_userlog()

    #message
    backup_message()

    return 0


def restore_db():

    #reset tables
    User.query.delete()
    Module.query.delete()
    Modaux.query.delete()
    Testbattery.query.delete()
    Testsession.query.delete()
    Client.query.delete()
    Clientlog.query.delete()
    db.session.commit()

    #load backup files and restore tables
    restore_user()

    restore_modules()

    restore_modaux()

    restore_testbattery()

    restore_testsession()

    restore_client()

    restore_clientlog()

    restore_result()

    restore_userlog()

    restore_message()

    #message

    return 0


#DONE
def restore_user():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'user.pic'), 'rb' ) as file:
        old = file.read()

    usertable = fernet.decrypt(old).decode('utf-8')

    users = json.loads(usertable)

    for user in users['users']:
        u = User()
        u.id = user['id']
        u.username = user['username']
        u.set_description(user['description'])
        u.set_contact(user['contact'])
        u.is_superuser = user['is_superuser']
        u.password_hash = user['password_hash']
        u.salt = user['salt']
        u.settings = user['settings']
        u.added = datetime.fromtimestamp(user['added'])
        u.last_modified = datetime.fromtimestamp(user['last_modified'])

        db.session.add(u)
        db.session.commit()

    return 0


#DONE
def restore_modules():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'module.pic'), 'rb' ) as file:
        old = file.read()

    moduletable = fernet.decrypt(old).decode('utf-8')

    modules = json.loads(moduletable)

    for module in modules['modules']:
        m = Module()
        m.id = module['id']
        m.uuid = module['uuid']
        m.short_name = module['short_name']
        m.verbose_name = module['verbose_name']
        m.description = module['description']
        m.attributes = module['attributes']
        m.id = module['id']
        m.added = datetime.fromtimestamp(module['added'])
        m.last_modified = datetime.fromtimestamp(module['last_modified'])

        db.session.add(m)
        db.session.commit()

    return 0


#DONE
def restore_modaux(old):
    with open( os.path.join(app.config['BACKUP_FOLDER'], 'modaux.pic'), 'rb' ) as file:
        old = file.read()

    auxtable = fernet.decrypt(old).decode('utf-8')

    modaux = json.loads(auxtable)

    for aux in modaux['auxs']:
        a = Modaux()
        a.id = aux['id']
        a.user_id = aux['user_id']
        a.module_id = aux['module_id']

        db.session.add(a)
        db.session.commit()

    return 0


#DONE
def restore_testbattery():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'testbattery.pic'), 'rb' ) as file:
        old = file.read()

    testbattery_table = fernet.decrypt(old).decode('utf-8')

    batteries = json.loads(testbattery_table)

    for bat in batteries['testbatteries']:
        tb = Testbattery()
        tb.id = bat['id']
        tb.user_id = bat['user_id']
        tb.name = bat['name']
        tb.description = bat['description']
        tb.modules = bat['modules']
        tb.created = datetime.fromtimestamp(bat['created'])
        tb.added = datetime.fromtimestamp(bat['added'])
        tb.last_modified = datetime.fromtimestamp(bat['last_modified'])

        db.session.add(tb)
        db.session.commit()

    return 0


#DONE
def restore_testsession():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'testsession.pic'), 'rb' ) as file:
        old = file.read()

    testsession_table = fernet.decrypt(old).decode('utf-8')

    sessions = json.loads(testsession_table)

    for ses in sessions['sessions']:
        s = Testsession()
        s.id = ses['id']
        s.uuid = ses['uuid']
        s.user_id = ses['user_id']
        s.testbattery_id = ses['testbattery_id']
        s.state = ses['state']
        s.created = datetime.fromtimestamp(ses['created'])
        s.due = datetime.fromtimestamp(ses['due'])
        s.set_invitation(ses['invitation_text'])
        s.added = datetime.fromtimestamp(ses['added'])
        s.last_modified = datetime.fromtimestamp(ses['last_modified'])

        db.session.add(s)
        db.session.commit()

    return 0


#DONE
def restore_client():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'client.pic'), 'rb' ) as file:
        old = file.read()

    client_table = fernet.decrypt(old).decode('utf-8')

    client = json.loads(client_table)

    for cli in client['clients']:
        c = Client()
        c.id = cli['id']
        c.uuid = cli['uuid']
        c.set_name(cli['name'])
        c.set_email(cli['email'])
        c.state = cli['state']
        c.session_id = cli['session_id']
        c.invitation_status = cli['invitation_status']
        c.added = datetime.fromtimestamp(cli['added'])
        c.last_modified = datetime.fromtimestamp(cli['last_modified'])

        db.session.add(c)
        db.session.commit()

    return 0


#DONE
def restore_clientlog():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'clientlog.pic'), 'rb' ) as file:
        old=file.read()

    clientlog_table = fernet.decrypt(old).decode('utf-8')

    clientlog = json.loads(clientlog_table)

    for cl in clientlog['clientlogs']:
        c = Clientlog()
        c.id = cl['id']
        c.client_id = cl['client_id']
        c.message = cl['message']
        c.source = cl['source']
        c.timestamp = datetime.fromtimestamp(cl['timestamp'])
        db.session.add(c)
        db.session.commit()

    return 0


#DONE
def restore_result():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'result.pic'), 'rb' ) as file:
        old = file.read()

    result_table = fernet.decrypt(old).decode('utf-8')
    result = json.loads(result_table)

    for re in result['results']:
        r = Result()
        r.id = re['id']
        r.client_id = re['']
        r.session_id = re['']
        r.module_id = re['']
        r.set_result(re['result_raw'])
        r.timestamp = datetime.fromtimestamp(re['timestamp'])
        r.added = datetime.fromtimestamp(re['added'])
        r.last_modified = datetime.fromtimestamp(re['last_modified'])

        db.session.add(r)
        db.session.commit()

    return 0


#DONE
def restore_userlog():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'userlog.pic'), 'rb' ) as file:
        old = file.read()

    userlog_table = fernet.decrypt(old).decode('utf-8')
    userlog = json.loads(userlog_table)

    for ul in userlog['userlogs']:
        u = Userlog()
        u.id = ul['id']
        u.user_id = ul['user_id']
        u.type = ul['type']
        u.message = ul['message']
        u.timestamp = datetime.fromtimestamp(ul['timestamp'])
        u.added = datetime.fromtimestamp(ul['added'])
        u.last_modified = datetime.fromtimestamp(ul['last_modified'])

        db.session.add(u)
        db.session.commit()

    return 0


#DONE
def restore_message():

    with open( os.path.join(app.config['BACKUP_FOLDER'], 'message.pic'), 'rb' ) as file:
        old = file.read()

    message_table = fernet.decrypt(old).decode('utf-8')
    messages = json.loads(message_table)

    for me in messages['messages']:
        m = Message()

        m.id = me['id']
        m.set_subject(me['subject'])
        m.set_message(me['message'])
        m.rec_id = me['rec_id']
        m.sen_id = me['sen_id']
        m.ant = me['ant']
        m.status = me['status']
        m.timestamp = datetime.fromtimestamp(me['timestamp'])
        m.added = datetime.fromtimestamp(me['added'])
        m.last_modified = datetime.fromtimestamp(me['last_modified'])

        db.session.add(m)
        db.session.commit()

    return 0


#DONE
def backup_user():
    usertable = {}
    users = []

    for user in User.query.all():
        us = {}
        us['id'] = user.id
        us['username'] = user.username
        us['description'] = user.get_description()
        us['contact'] = user.get_contact()
        us['is_superuser'] = user.is_superuser
        us['password_hash'] = user.password_hash
        us['salt'] = user.salt
        us['settings'] = user.settings
        us['added'] = user.added.timestamp()
        us['last_modified'] = user.last_modified.timestamp()
        users.append(us)

    usertable['timestamp'] = datetime.now().timestamp()
    usertable['users'] = users

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'user.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(usertable).encode('utf-8')))

    return 0


#DONE
def backup_modules():
    moduletable = {}
    modules = []

    for mod in Module.query.all():
        m = {}
        m['id'] = mod.id
        m['uuid'] = mod.uuid
        m['short_name'] = mod.short_name
        m['verbose_name'] = mod.verbose_name
        m['description'] = mod.description
        m['attributes'] = mod.attributes
        m['added'] = mod.added.timestamp()
        m['last_modified'] = mod.last_modified.timestamp()

        modules.append(m)

    moduletable['timestamp'] = datetime.now().timestamp()
    moduletable['modules'] = modules

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'module.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(moduletable).encode('utf-8')))

    return 0


#DONE
def backup_modaux():
    auxtable = {}
    auxs = []

    for aux in Modaux.query.all():
        a = {}
        a['id'] = aux.id
        a['user_id'] = aux.user_id
        a['module_id'] = aux.module_id
        auxs.append(a)

    auxtable['timestamp'] = datetime.now().timestamp()
    auxtable['auxs'] = auxs

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'modaux.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(auxtable).encode('utf-8')))

    return 0


#DONE
def backup_testbattery():
    testbattery_table = {}
    testbatteries = []

    for testbattery in Testbattery.query.all():
        t = {}
        t['id'] = testbattery.id
        t['user_id'] = testbattery.user_id
        t['name'] = testbattery.name
        t['description'] = testbattery.description
        t['modules'] = testbattery.modules
        t['created'] = testbattery.created.timestamp()
        t['added'] = testbattery.added.timestamp()
        t['last_modified'] = testbattery.last_modified.timestamp()

        testbatteries.append(t)

    testbattery_table['timestamp'] = datetime.now().timestamp()
    testbattery_table['testbatteries'] = testbatteries

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'testbattery.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(testbattery_table).encode('utf-8')))

    return 0


#DONE
def backup_testsession():
    testsession_table = {}
    sessions = []

    for session in Testsession.query.all():
        s = {}
        s['id'] = session.id
        s['uuid'] = session.uuid
        s['user_id'] = session.user_id
        s['testbattery_id'] = session.testbattery_id
        s['created'] = session.created.timestamp()
        s['due'] = session.due.timestamp()
        s['state'] = session.state
        s['invitation_text'] = session.get_invitation()
        s['added'] = session.added.timestamp()
        s['last_modified'] = session.last_modified.timestamp()
        sessions.append(s)

    testsession_table['timestamp'] = datetime.now().timestamp()
    testsession_table['sessions'] = sessions

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'testsession.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(testsession_table).encode('utf-8')))

    return 0


#DONE
def backup_client():
    client_table = {}
    clients = []

    for client in Client.query.all():
        c = {}
        c['id'] = client.id
        c['uuid'] = client.uuid
        c['name'] = client.get_name()
        c['email'] = client.get_email()
        c['state'] = client.state
        c['session_id'] = client.session_id
        c['invitation_status'] = client.invitation_status
        c['added'] = client.added.timestamp()
        c['last_modified'] = client.last_modified.timestamp()
        clients.append(c)

    client_table['timestamp'] = datetime.now().timestamp()
    client_table['clients'] = clients

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'client.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(client_table).encode('utf-8')))
    return 0


#DONE
def backup_clientlog():
    clientlog_table = {}
    clientlogs = []

    for clientlog in Clientlog.query.all():
        c = {}
        c['id'] = clientlog.id
        c['client_id'] = clientlog.client_id
        c['message'] = clientlog.message
        c['source'] = clientlog.source
        c['timestamp'] = clientlog.timestamp.timestamp()
        clientlogs.append(c)

    clientlog_table['timestamp'] = datetime.now().timestamp()
    clientlog_table['clientlogs'] = clientlogs

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'clientlog.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(clientlog_table).encode('utf-8')))
    return 0


#DONE
def backup_result():
    result_table = {}
    results = []

    for res in Result.query.all():
        r = {}
        r['id'] = res.id
        r['client_id'] = res.client_id
        r['session_id'] = res.session_id
        r['module_id'] = res.module_id
        r['timestamp'] = res.timestamp.timestamp()
        r['result_raw'] =res.get_result()
        r['added'] = res.added.timestamp()
        r['last_modified'] = res.last_modified.timestamp()
        results.append(r)

    result_table['timestamp'] = datetime.now().timestamp()
    result_table['results'] = results

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'result.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(result_table).encode('utf-8')))
    return 0


#DONE
def backup_userlog():
    userlog_table = {}
    userlogs = []

    for ul in Userlog.query.all():
        u = {}
        u['id'] = ul.id
        u['user_id'] = ul.user_id
        u['timestamp'] = ul.timestamp.timestamp()
        u['type'] = ul.type
        u['message'] = ul.message
        u['added'] = ul.added.timestamp()
        u['last_modified'] = ul.last_modified.timestamp()
        userlogs.append(u)

    userlog_table['timestamp'] = datetime.now().timestamp()
    userlog_table['userlogs'] = userlogs

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'userlog.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(userlog_table).encode('utf-8')))
    return 0


#DONE
def backup_message():
    message_table = {}
    messages = []

    for me in Message.query.all():
        m = {}
        m['id'] = me.id
        m['subject'] = me.get_subject()
        m['message'] = me.get_message()
        m['rec_id'] = me.rec_id
        m['sen_id'] = me.sen_id
        m['ant'] = me.ant
        m['status'] = me.status
        m['timestamp'] = me.timestamp.timestamp()
        m['added'] = me.added.timestamp()
        m['last_modified'] = me.last_modified.timestamp()
        messages.append(m)

    message_table['timestamp'] = datetime.now().timestamp()
    message_table['messages'] = messages

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'message.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(message_table).encode('utf-8')))
    return 0