
from app import db, login, fernet

import bcrypt

from datetime import datetime

from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#DONE
'''
===============================
USERS
-------------------------------
 - id (int, u)
 - username (str/16/, u)
 !- description (str/64/, enc)
 !- contact (str/256/, enc)
 - is_superuser (bool)
 - password_hash (str/128/)
 - salt (str/128/)
 - settings (str/2048/, #json)
===============================
'''
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, index = True, primary_key = True)
    username = db.Column(db.String(32), index = True, unique = True)
    description = db.Column(db.LargeBinary)
    contact = db.Column(db.LargeBinary)
    is_superuser = db.Column(db.Boolean, default = False)
    password_hash = db.Column(db.String(128), default = '')
    salt = db.Column(db.String(128), default = '')
    settings = db.Column(db.String(2048), default = '')

    added = db.Column(db.Date(), default = datetime.now())
    last_modified = db.Column(db.Date(), default = datetime.now())

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

    def set_description(self, desc):
        self.description = fernet.encrypt(desc.encode('utf-8'))
        return True

    def set_contact(self,contact):
        self.contact = fernet.encrypt(contact.encode('utf-8'))
        return True

    def get_description(self):
        return fernet.decrypt(self.description).decode('utf-8')

    def get_contact(self):
        return fernet.decrypt(self.contact).decode('utf-8')


#DONE
'''
=================================
MODULES
---------------------------------
 - id (int, u)
 - uuid (str/14/, u)
 - short_name (str/16/, u)
 - verbose_name (str/128/)
 - description (str/2048/)
 - attributes (str/1024/, #json)
=================================
'''
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, index = True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    short_name = db.Column(db.String(16), unique=True)
    verbose_name = db.Column(db.String(128), default = '')
    description = db.Column(db.String(2048), default = '')
    attributes = db.Column(db.String(1024), default = '')  #JSON

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.short_name}'


#DONE
'''
======================================
MODAUX
--------------------------------------
 - id (int, u)
 - user_id (int)  |--> USERS.id
 - module_id (int)  |--> MODULES.id
======================================
'''
class Modaux(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))


#DONE
'''
===================================
TESTBATTERIES
-----------------------------------
 - id (int, u)
 - user_id (int)  |--> USERS.id
 - name (str/64/)
 - description (str/1024/)
 - created (timestamp)
 - last_modified (timestamp)
 - modules (str/512/, #json)
===================================
'''
class Testbattery(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), default = '')
    description = db.Column(db.String(1024), default='')
    created = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())
    modules = db.Column(db.String(512), default='')  #JSON

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.name}'


#DONE
'''
=================================================
TESTSESSIONS
-------------------------------------------------
 - id (int, u)
 - uuid (str, u)
 - user_id (int)  |--> USERS.id
 - testbattery_id (int)  |--> TESTBATTERIES.id
 - created (timestamp)
 !- invitation_text (str/1024/, enc)
 - due (timestamp)
 - state (int)
=================================================
'''
class Testsession(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testbattery_id = db.Column(db.Integer, db.ForeignKey('testbattery.id'))
    created = db.Column(db.Date(), default=datetime.now())
    due = db.Column(db.Date(), default=datetime.now())
    state = db.Column(db.Integer, default = -1)
    invitation_text = db.Column(db.LargeBinary)

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.uuid}'

    def set_invitation(self, text):
        self.invitation_text = fernet.encrypt(text.encode('utf-8'))
        return True

    def get_invitation(self):
        return fernet.decrypt(self.invitation_text).decode('utf-8')


#DONE
'''
=========================================
CLIENTS
-----------------------------------------
 - id (int, u)
 - uuid (str, u)
 !- name (str/32/, enc)
 !- email (str/256/, enc)
 - session_id (int)  |--> TESTSESSIONS.id
 - invitation_status (int)  # 0 = not sent yet, 1 = error (wrong or missing email), 2 = sent
 - state (int)
=========================================
'''
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(14), index=True, unique=True)
    name = db.Column(db.LargeBinary)
    email = db.Column(db.LargeBinary)
    state = db.Column(db.Integer, default=-1)
    session_id = db.Column(db.Integer, db.ForeignKey('testsession.id'))
    invitation_status = db.Column(db.Integer, default = -1)

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.name}'

    def set_name(self,name):
        self.name = fernet.encrypt(name.encode('utf-8'))
        return True

    def set_email(self,email):
        self.email = fernet.encrypt(email.encode('utf-8'))
        return True

    def get_name(self):
        return fernet.decrypt(self.name).decode('utf-8')

    def get_email(self):
        return fernet.decrypt(self.email).decode('utf-8')


#DONE
'''
=============================================
CLIENTLOG
---------------------------------------------
 - id (int, u)
 - client_id (int)  |--> CLIENTS.id
 - timestamp (timestamp)
 - source (str/16/)  |--> MODULES.short_name
 !!!-ez nem jó > átírtam: source (int)  |--> MODULES.id -!!!
 - message (str/128/)
=============================================
'''
class Clientlog(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    message = db.Column(db.String(128), default = '')
    source = db.Column(db.Integer, db.ForeignKey('module.id'))
    timestamp = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.log}'


#DONE
'''
============================================
RESULTS
--------------------------------------------
 - id (int, u)
 - client_id (int)  |--> CLIENTS.id
 - session_id (int)  |--> TESTSESSIONS.id
 - module_id (int)  |--> MODULES.id
 - timestamp (timestamp)
 !- result_raw (str/2048/, #json, enc)
============================================
'''
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('testsession.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    timestamp = db.Column(db.Date(), default=datetime.now())
    result_raw = db.Column(db.LargeBinary)

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Modulnév: {self.timestamp}'

    def set_result(self, result):
        self.result_raw = fernet.encrypt(result.encode('utf-8'))
        return True

    def get_result(self):
        return fernet.decrypt(self.result_raw).decode('utf-8')


#DONE
'''
================================
USERLOG
--------------------------------
 - id (int, u)
 - user_id (int)  |--> USERS.id
 - timestamp (timestamp)
 - type (str/8/)
 - message (str/128/)
================================
'''
class Userlog(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Date(), default=datetime.now())
    type = db.Column(db.String(8), default = '')
    message = db.Column(db.String(128), default = '')

    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())

    def __repr__(self):
        return f'Timestamp: {self.timestamp}, Message: {self.message}'


#DONE
'''
===================================
MESSAGES
-----------------------------------
 - id (int, u)
 - direction (int)   # Itt pl. 0 lesz, ha a felhasználó a küldő, és 1, ha neki szól az üzenet
 - user_id (int)  |--> USERS.id
 - reply_to (int)  |--> MESSAGES.id   # Egy korábbi üzenetre való hivatkozás, ennek a segítségével az üzenetek akár láncba is rendezhetők - lehet üres!
 - status (int)    # pl. 0 ha olvasatlan az üzenet, 1 ha le van kezelve (user = megnyitotta, admin = megjelölte, mint kezelt üzenetet)
 - timestamp (timestamp)
 !- subject (str/32/, enc)
 !- message (str/512/, enc)
===================================
'''
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    rec_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #a címzett ID-je
    sen_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #a feladó ID-je
    ant = db.Column(db.Integer, db.ForeignKey('message.id'), nullable = True)  #előzmény
    status = db.Column(db.Integer, default = -1)
    timestamp = db.Column(db.Date(), default=datetime.now())
    added = db.Column(db.Date(), default=datetime.now())
    last_modified = db.Column(db.Date(), default=datetime.now())
    subject = db.Column(db.LargeBinary)
    message = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'Sender: {self.sen_id}, recepient: {self.rec_id}, timestamp: {self.timestamp}'

    def set_subject(self, subject):
        self.subject = fernet.encrypt(subject.encode('utf-8'))
        return True

    def set_message(self, message):
        self.message = fernet.encrypt(message.encode('utf-8'))
        return True

    def get_subject(self, subject):
        return fernet.decrypt(self.subject).decode('utf-8')

    def get_message(self):
        return fernet.decrypt(self.message).decode('utf-8')
