
from app import db, login

import bcrypt

from datetime import datetime

from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#DONE
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, index = True, primary_key = True)
    uuid = db.Column(db.String(14), unique = True)
    username = db.Column(db.String(32), index = True, unique = True)
    is_superuser = db.Column(db.Boolean, default = False)
    password_hash = db.Column(db.String(128), default = '')
    salt = db.Column(db.String(128), default = '')
    settings = db.Column(db.String(256), default = '')

    #testpacket = db.relationship('TestPacket', backref = '_user', lazy = 'dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        salt = bcrypt.gensalt(14)
        p_bytes = password.encode()
        pw_hash = bcrypt.hashpw(p_bytes,salt)
        self.password_hash = pw_hash.decode()
        self.salt = salt.decode()
        return True

    def check_password(self, password):
        c_password = bcrypt.hashpw(password.encode(),self.salt.encode()).decode()
        if c_password == self.password_hash:
            return True
        else:
            return False


#DONE
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, index = True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    short_name = db.Column(db.String(32), unique=True)
    verbose_name = db.Column(db.String(128), default = '')
    description = db.Column(db.String(256), default = '')
    attributes = db.Column(db.String(512), default = '')  #JSON

    def __repr__(self):
        return f'Modulnév: {self.short_name}'


#DONE
class Modaux(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))


#DONE
class Testbattery(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(32), default = '')
    description = db.Column(db.String(256), default='')
    created = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())
    modules = db.Column(db.String(128), default='')

    def __repr__(self):
        return f'Modulnév: {self.name}'


#DONE
class Testsession(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testbattery_id = db.Column(db.Integer, db.ForeignKey('testbattery.id'))
    created = db.Column(db.Date(), default=datetime.now())
    due = db.Column(db.Date(), default=datetime.now())
    state = db.Column(db.Integer, default = -1)

    def __repr__(self):
        return f'Modulnév: {self.uuid}'


#DONE
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    name = db.Column(db.String(14), default = '')
    session_id = db.Column(db.Integer, db.ForeignKey('testsession.id'))
    log_id = db.Column(db.Integer, db.ForeignKey('clientlog.id'))

    def __repr__(self):
        return f'Modulnév: {self.name}'


#DONE
class Clientlog(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    #ez meg minek??? -> uuid = db.Column(db.String(14), index=True, unique=True)
    state = db.Column(db.Integer, default = -1)
    log = db.Column(db.String(128), default = '')
    #ezek nincsenek a megadott spec.-ben!
    timestamp = db.Column(db.Date(), default=datetime.now())
    client = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return f'Modulnév: {self.log}'


#DONE
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('testsession.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    log_id = db.Column(db.Integer, db.ForeignKey('clientlog.id'))
    timestamp = db.Column(db.Date(), default=datetime.now())
    result_raw = db.Column(db.String(128), default = '')

    def __repr__(self):
        return f'Modulnév: {self.result_raw}'



'''

*** Adattáblák

# id: egyedi azonosító, autoincrement
# uuid: egyedi random azonosító
# u = unique

========================
USERS
------------------------
 - id (int, u)
 - uuid (str, u)
 - username (str, u)
 - is_superuser (bool)
 - password ...
 - settings (str, json)
========================

==========================
MODULES
--------------------------
 - id (int, u)
 - uuid (str, u)
 - short_name (str, u)
 - name (str)
 - description (str)
 - attributes (str, json)
==========================

======================================
MODAUX
--------------------------------------
 - id (int, u)
 - user_id (str)  |--> USERS.uuid
 - module_id (str)  |--> MODULES.uuid
======================================

===================================
TESTBATTTERIES
-----------------------------------
 - id (int, u)
 - uuid (str, u)
 - user_id (str)  |--> USERS.uuid
 - name (str)
 - description (str)
 - created (timestamp)
 - last_modified (timestamp)
 - modules (str, json)
===================================

=================================================
TESTSESSIONS
-------------------------------------------------
 - id (int, u)
 - uuid (str, u)
 - user_id (str)  |--> USERS.uuid
 - testbattery_id (str)  |--> TESTBATTERIES.uuid
 - created (timestamp)
 - due (timestamp)
 - state (int)
=================================================

============================================
CLIENTS
--------------------------------------------
 - id (int, u)
 - uuid (str, u)
 - name (str)
 - session_id (str)  |--> TESTSESSIONS.uuid
 - log_id (str)  |--> CLIENTLOG.uuid
============================================

===============
CLIENTLOG
---------------
 - id (int, u)
 - uuid (str, u)
 - state (int)
 - log (str)
===============

============================================
RESULTS
--------------------------------------------
 - id (int, u)
 - client_id (str)  |--> CLIENTS.uuid
 - session_id (str)  |--> TESTSESSIONS.uuid
 - module_id (str)  |--> MODULES.uuid
 - log_id (str)  |--> CLIENTLOG.uuid
 - timestamp (timestamp)
 - result_raw (str, json)
============================================



'''