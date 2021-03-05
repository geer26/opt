import base64
from os import listdir, remove, path, getenv
from zipfile import ZipFile

from cryptography.fernet import Fernet
from flask_login import current_user
from os.path import basename
from datetime import datetime
import json


__version__ = '0.1'


class Backupper():

    def __init__(self, app=None, **kwargs):

        self.app = None
        self.folder = None
        self.archive_name = None
        self.log_name = None
        self.socket = None
        self.event_code = None
        self.tables = None
        self.backup_path = None
        self.log_path = None
        self.temp_log_path = None
        self.fernet = None
        self.log_type = {0: 'INFO', 1: 'WRITE', 2: 'READ', 3: 'ERROR'}

        return


    def init_app(self, app, tables,  **kwargs):
        self.fernet = Fernet(base64.urlsafe_b64encode(getenv('DB_SECRET').encode('utf-8')))

        if app is not None:
            if not hasattr(app, 'extensions'):
                app.extensions = {}
            app.extensions['backupper'] = self

        self.tables = tables

        if 'folder' in kwargs:
            self.folder = kwargs.get('folder')
        else:
            self.folder = app.config['BACKUP_FOLDER']

        if 'archive_name' in kwargs:
            self.archive_name = kwargs.get('archive_name')
        else:
            self.archive_name = 'backup2.zip'

        self.backup_path = path.join(self.folder, self.archive_name)

        if 'log_name' in kwargs:
            self.log_name = kwargs.get('log_name')
        else:
            self.log_name = 'log.file'
        self.log_path = path.join(self.folder, self.log_name)

        self.temp_log_path = path.join(self.folder, f'temp_{self.log_name}')

        if 'db' in kwargs:
            self.db = kwargs.get('db')
        else:
            self.db = app.extensions.get('sqlalchemy')
            from app import db
            self.db = db

        self.check()


    def check(self):
        """
        Checks if archive exists, if not creates!
        :return: None
        """

        files = listdir(self.folder)
        if self.archive_name not in files:
            #Create archive
            with ZipFile(self.backup_path, 'w') as archive:
                #create first log entry
                with open(self.log_path, 'a') as logfile:
                    logfile.write(self.create_log_entry('Archive created'))
                    logfile.write('\n')
                archive.write(self.log_path, basename(self.log_path))
            remove(self.log_path)

        return


    def create_log_entry(self, message, type=0):
        if current_user and current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        message = {
            'type': self.log_type[type],
            'timestamp': f'{datetime.now().timestamp()}',
            'datetime': f'{datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}',
            'executor': f'{username}',
            'event': f'{message}'
        }

        return json.dumps(message)


    def update_log(self,message, type=0):
        pass


    def flush_table(self, table):
        return 0


    def restore_table(self, table):
        return 0


    def backup_all(self):

        #1. extract archive to folder and delete old zipfile
        self.extract_all()

        #2. create encrypted table saves
        for table in self.tables:
            tablename = table.__name__
            temp = ''
            for rekord in table.query.all():
                temp+= rekord.dump()
                temp+='\n'

            with open(path.join(self.folder, f'{tablename}.pic'), 'wb') as enrcypted:
                enrcypted.write(self.fernet.encrypt(temp.encode('utf-8')))


            #3. write pic file to zip
            self.to_zip(path.join(self.folder, f'{tablename}.pic'))

            #4. delete temporary files
            remove(path.join(self.folder, f'{tablename}.pic'))

            #5. update log
            with open(self.log_path, 'a') as logfile:
                logfile.write(self.create_log_entry(f'{tablename} table flushed', type=2))
                logfile.write('\n')

        #6. add log to zip
        self.to_zip(path.join(self.folder, 'log.file'))

        #7. remove unzipped logfile
        remove(path.join(self.folder, 'log.file'))

        return 0


    def restore_all(self):
        print('RESTORE HERE!')
        #1. unzip all
        self.extract_all(nodelete=True)

        #2. Clear all tables entirerly(log it per table!)
        for table in self.tables:
            self.wipe_table(table)
            pass

        #3. iter over saves, decode and save it again with 'temp_' prefix
        for file in listdir(self.folder):
            if file.endswith('.pic'):
                temp = self.fernet.decrypt( open(path.join(self.folder, f'{file}'), 'rb').read() ).decode('utf-8')

                for table in self.tables:
                    if table.__name__ == file.split('.')[0]:
                        self.fill_table( table, list(temp.split('\n')) )
        return 0


    def wipe_table(self, table):
        table.query.delete()
        #self.db.session.commit()
        with open(self.log_path, 'a') as logfile:
            logfile.write(self.create_log_entry(f'{table.__name__} table wiped into oblivion!', type=1))
            logfile.write('\n')
        return 0


    def fill_table(self, table, content):
        for rek in content:
            if rek == '':
                continue
            else:
                rekord = table()
                rekord.load(rek)
                self.db.session.add(rekord)
                #self.db.session.commit()
                with open(self.log_path, 'a') as logfile:
                    logfile.write(self.create_log_entry(f'{table.__name__} table restored from save', type=1))
                    logfile.write('\n')
        return 0


    def extract_all(self, **kwargs):
        print( path.join(self.backup_path) )
        with ZipFile(path.join(self.backup_path), 'r') as oldzip:
            oldzip.extractall(path.join(self.folder))
        if 'nodelete' not in kwargs or not kwargs.get('nodelete'):
            remove(self.backup_path)
        return 0


    def to_zip(self, fileobject_path):
        zipObj = ZipFile(self.backup_path, 'a')
        zipObj.write(fileobject_path, basename(fileobject_path))
        zipObj.close()
        return 0