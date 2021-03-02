from datetime import datetime
import json
import os
from os.path import basename
from zipfile import ZipFile

from flask_login import current_user

from app import fernet, db, app
from app.models import User, Module, Modaux, Testbattery, Testsession, Client, Clientlog, Result, Userlog, Message


def backup_db():

    check_backup()

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

    #restore_from_zip('user.pic')

    #message

    return 0


def check_backup():
    if not 'backup.zip' in os.listdir(app.config['BACKUP_FOLDER']):
        with ZipFile(os.path.join(app.config['BACKUP_FOLDER'], 'backup.zip'), 'w') as zipObj:
            pass

    #create logfile
    ts_path = os.path.join(app.config['BACKUP_FOLDER'], 'log.file')
    with open(ts_path, 'w') as logfile:
        pass
    add_to_zip(ts_path)
    os.remove(ts_path)

    #update logfile
    upd_log('Archive created')

    return 0


#DONE
def add_to_zip(fileobject_path):

    fname = fileobject_path.split('/')[-1]

    zippath = os.path.join(app.config['BACKUP_FOLDER'], 'backup.zip')
    newpath = os.path.join(app.config['BACKUP_FOLDER'], 'backup_temp.zip')


    #Create nem temp zipfile w/o the new fil to write
    with ZipFile(zippath, 'r') as oldzip, ZipFile(newpath, 'a') as newzip:
        for file in oldzip.infolist():
            buffer = oldzip.read(file.filename)
            if file.filename != fname:
                newzip.writestr(file,buffer)


    # remove orig zipfile
    os.remove(zippath)


    # rename new zipfile
    os.rename(newpath, zippath)


    # add file to the ne zipfile(renamed!)
    zipObj = ZipFile(zippath, 'a')
    zipObj.write(fileobject_path, basename(fileobject_path))
    zipObj.close()

    return 0


def upd_log(log_text):

    zippath = os.path.join(app.config['BACKUP_FOLDER'], 'backup.zip')
    filepath = app.config['BACKUP_FOLDER']
    logpath = os.path.join(app.config['BACKUP_FOLDER'], 'log.file')
    filename = 'log.file'

    message = {
        'timestamp' : f'{datetime.now().timestamp()}',
        'datetime' : f'{datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}',
        'executor' : f'{current_user.username}',
        'event' : f'{log_text}'
    }

    #1. get logfile
    with ZipFile(zippath,'r') as zipObj:
        zipObj.extract(filename, filepath)

    #2. add new entry at the end
    with open(logpath, 'r') as logfile:
        print('OLDLINES:')
        for line in logfile.readlines():
            print(line)

    with open(logpath, 'a') as logfile:
        logfile.writelines(json.dumps(message))

    with open(logpath, 'r') as logfile:
        print('NEWLINES:')
        for line in logfile.readlines():
            print(line)


    #3. add_to_zip(fileobject_path)
    add_to_zip(logpath)

    #4. delete the non-zipped
    os.remove(logpath)

    return 0


#DONE
def restore_from_zip(filename):

    zippath = os.path.join(app.config['BACKUP_FOLDER'], 'backup.zip')
    filepath = app.config['BACKUP_FOLDER']
    fp = os.path.join(app.config['BACKUP_FOLDER'], filename)


    #1. unzip single file!
    with ZipFile(zippath,'r') as zipObj:
        zipObj.extract(filename, filepath)

    #2. create file object
    with open(fp, 'rb') as file:
        old = file.read()

    #3. delete temp extracted
    os.remove(fp)

    return old


#DONE
def restore_user():

    old = restore_from_zip('user.pic')

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

    old = restore_from_zip('module.pic')

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
def restore_modaux():

    old = restore_from_zip('modaux.pic')

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

    old = restore_from_zip('testbattery.pic')

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

    old = restore_from_zip('testsession.pic')

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

    old = restore_from_zip('client.pic')

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

    old = restore_from_zip('clientlog.pic')

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

    old = restore_from_zip('result.pic')

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

    old = restore_from_zip('userlog.pic')

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

    old = restore_from_zip('message.pic')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'user.pic')

    with open( savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(usertable).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('User table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'module.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(moduletable).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Module table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'modaux.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(auxtable).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Modaux table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'testbattery.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(testbattery_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Testbattery table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'testsession.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(testsession_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Testsession table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'client.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(client_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Client table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'clientlog.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(clientlog_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Clientlog table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'result.pic')

    with open(savepath, 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(result_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Result table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'userlog.pic')

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'userlog.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(userlog_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Userlog table archived')

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

    savepath = os.path.join(app.config['BACKUP_FOLDER'], 'message.pic')

    with open(os.path.join(app.config['BACKUP_FOLDER'], 'message.pic'), 'wb') as enrcypted:
        enrcypted.write(fernet.encrypt(json.dumps(message_table).encode('utf-8')))

    add_to_zip(savepath)
    os.remove(savepath)

    upd_log('Message table archived')

    return 0