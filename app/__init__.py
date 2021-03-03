import base64

from flask import Flask

from app.logger import Logger

from config import SQLite

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_socketio import SocketIO

from flask_login import LoginManager
import os

from cryptography.fernet import Fernet


app = Flask(__name__)
app.config.from_object(SQLite)


login = LoginManager(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


socket = SocketIO(app)
socket.init_app(app,  cors_allowed_origins="*")


fernet = Fernet(base64.urlsafe_b64encode(os.getenv('FERMET_SECRET').encode('utf-8')))


logger = Logger( folder = app.config['LOG_FOLDER'] )


from app import routes, models
