from os import listdir, remove, path
from zipfile import ZipFile
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
        self.log_type = {0: 'INFO', 1: 'WRITE', 2: 'READ', 3: 'ERROR'}

        return


    def init_app(self, app, tables,  **kwargs):
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

        self.check()
        self.backup_all()


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
                archive.write(self.log_path, basename(self.log_path))
            remove(self.log_path)

        return


    def create_log_entry(self, message, type = 0):
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


    def flush_table(self, table):
        return 0


    def restore_table(self, table):
        return 0


    def backup_all(self):

        #TODO solve this!
        #1. extract archive to folder
        '''with open(self.backup_path,'r') as z:
            oldzip = ZipFile.open(z, 'r')
        print(oldzip)
        oldzip.close()'''

        #2. delete old zip
        '''os.remove(self.backup_path)'''

        #3. create table saves with overwrite
        '''for table in self.tables:
                    tablename = table.__name__
                    with open(path.join(self.folder, f'{tablename}.pic'), 'w') as tempfile:
                        for rekord in table.query.all():
                            tempfile.write(rekord.dump())
                            tempfile.write('\n')'''

        #4. write all.pic and .file files into a new archive

        '''with ZipFile.open(path.join(self.folder, self.archive_name), 'r') as oldzip:
            oldzip.extractall()'''

        return 0


    def restore_all(self):
        return 0


    def zip_all(self):
        return 0