from flask import Flask
from config import SQLite

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_socketio import SocketIO

from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(SQLite)
print(app.config)

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


from app import routes, models
