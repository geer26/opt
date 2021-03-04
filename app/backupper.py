import json
from os import path, listdir, remove
from os.path import basename
from datetime import datetime
from zipfile import ZipFile

from flask_login import current_user

class Backupper():

    def __init__(self,
                 folder,  #backup folder - mandatory
                 db,  #db from app - mandatory
                 acrhive_name = 'backup.zip',  #name of the backup file - optional
                 log_name = 'log.file',  #log name - optional
                 socket = None,  #inherited socket object to communicate on - optional
                 event_code = None  #ws event code to send messages thorough - optional
                 ):
        self.folder = folder
        self.db = db
        self.archive_name = acrhive_name
        self.log_name = log_name
        self.socket = socket
        self.event_code = event_code

        self.backup_path = path.join(self.folder, self.archive_name)
        self.log_path = path.join(self.folder, self.log_name)
        self.temp_log_path = path.join(self.folder, f'temp_{self.log_name}')

        self.log_type = {0: 'INFO', 1: 'WARNING', 2: 'ERROR', 3: 'FATAL ERROR'}
        #self.check()


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