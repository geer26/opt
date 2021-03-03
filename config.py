import os
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY') or '01!ChAnGeThIs!89'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or '!Opt2021!'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    TEMPLATES_AUTO_RELOAD = True

    UPLOAD_FOLDER = path.join('app/uploads/')
    BACKUP_FOLDER = environ.get('BACKUP_FOLDER') or path.join(basedir, 'app/backup/')
    if environ.get('LOG_FOLDER'):
        LOG_FOLDER = path.join(basedir,environ.get('LOG_FOLDER'))
    else:
        LOG_FOLDER = path.join(basedir, 'app/log/')

    #CLIENT_LISTS = path.join('app/temp/')
    ALLOWED_EXTENSIONS = {'zip'}
    #SENDGRID_API_KEY = environ.get('SENDGRID_API_KEY') or 'APIKEY'
    #LANG = environ.get('LANG') or 'C.UTF-8'
    #LC_ALL = environ.get('LC_ALL') or 'C.UTF-8'

class PostgreSQL(Config):
    """Production config."""
    #FLASK_ENV = 'production'
    #DEBUG = False
    #TESTING = False
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = environ.get('POSTGRES_URI')


class SQLite(Config):
    """Development config."""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLITE_URI') or \
                              'sqlite:///' + path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False