import json
import re
from random import SystemRandom
from app import db
from flask_login import current_user

from app.models import User, Module


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

    users = []

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
        pass
        #get all

    return json.dumps(data)


def check_adduser(data):

    u = User.query.filter(User.username == str(data['username'])).all()

    if len(u) != 0:
        return 1 #User exists
    if not validate_password(str(data['pw1'])):
        return 2 #invalid password

    user = User()
    user.username = str(data['username'])
    user.set_password(str(data['pw1']))
    user.set_description(str(data['description']))
    user.set_contact(str(data['contact']))
    user.is_superuser = data['is_superuser']

    db.session.add(user)
    db.session.commit()

    return 0


def del_user(data):
    user = User.query.get(int(data['userid']))
    if not user: return 1
    else:
        db.session.delete(user)
        db.session.commit()
    return 0