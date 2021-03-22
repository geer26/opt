import base64

from flask import Flask

from app.logger import Logger

from config import SQLite, PostgreSQL

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_socketio import SocketIO

from flask_mail import Mail

from app.geer26_backupper import Backupper

from flask_login import LoginManager
import os

from cryptography.fernet import Fernet

app = Flask(__name__)

dbtype = os.environ.get('DB_TYPE')

if not dbtype or dbtype == 'SQLite':
    app.config.from_object(SQLite)
elif dbtype and dbtype == 'PostgreSQL':
    app.config.from_object(PostgreSQL)

login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

socket = SocketIO(app)
socket.init_app(app, cors_allowed_origins="*")

print(app.config['MAIL_SERVER'])
mail = Mail(app)

'''message = Message()
message.subject = 'TEST FROM OPT'
message.body = 'THIS MESSAGE WAS SENT FROM A LIVING APP'
message.add_recipient('gergo.kurucz@gmail.com')

mail.send(message)
'''

fernet = Fernet(base64.urlsafe_b64encode(os.getenv('FERNET_SECRET').encode('utf-8')))

logger = Logger(folder=app.config['LOG_FOLDER'], socket=socket)

logger.upd_log('App started', 9)

bu = Backupper()
logger.upd_log('Backupper init', 9)

from app import routes, models

bu.init_app(app,
            tables=[
        models.User, models.Client, models.Result, models.Message,
        models.Userlog, models.Clientlog, models.Testsession,
        models.Testbattery, models.Modaux, models.Module
            ],
            logger=logger)



