import json
from random import SystemRandom

from app.models import User


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
    users : [
        {
            id : <id>,
            username : <username>
            description : <description> !
            contact : <contact> !
            is_superuser : <is_superuser>
            settings : <settings>
        }
    ]
    }

    '''

    data = {}
    users = []

    for user in User.query.all():
        u = {}
        u['id'] = user.id
        u['username'] = user.username
        u['description'] = user.get_description()
        u['contact'] = user.get_contact()
        u['is_superuser'] = user.is_superuser
        u['settings'] = user.settings
        users.append(u)

    data['users'] = users

    return data