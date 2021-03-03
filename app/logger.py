import json
from os.path import basename
from zipfile import ZipFile
from os import listdir, path, stat, rename, remove
from datetime import datetime

from flask_login import current_user


class Logger():


    def __init__(self,
                 folder,
                 maxsize = 5120,
                 maxlength = 5000,
                 maxdue = 7,
                 name = 'log.file',
                 archive_name = 'log_archive.zip'
                 ):
        self.folder = folder
        self.maxsize = maxsize*1024  #file size in bytes
        self.maxlength = maxlength  #max number of lines in file
        self.maxdue = maxdue  #max time the logfile lives in days
        self.name = name   #the name of the logfile
        self.archive_name = archive_name  #the name of the zipped archive

        self.logfile_path = path.join(self.folder, self.name)
        self.archive_path = path.join(self.folder, self.archive_name)

        self.log_type = {0: 'INFO', 1: 'WARNING', 2: 'ERROR', 3: 'FATAL ERROR'}

        self.check()  #init logfile
        return

    #TODO finish or refractor!
    def check(self):
        """
        Init logfile. If not exists, creates it
        Checks limit and if reached, archives it, and creates a new one
        :return: 0 if OK
        """
        files = listdir(self.folder)
        logfile_path = path.join(self.folder, self.name)
        archive_path = path.join(self.folder, self.archive_name)

        # check if logfile exists, if not, create it
        if self.name not in files:
            with open(logfile_path, "w") as logfile:
                logfile.write(f'LOGFILE LÉTREHOZVA: {datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}')
                logfile.write('\n')

        # check if archive exists, if not, create it
        if self.archive_name not in files:
            with ZipFile(archive_path, 'w') as archive:
                pass

        # check if logfile reached sizelimit, if so archive it and recall __init__
        size = stat(logfile_path).st_size
        if size >= self.maxsize:
            with ZipFile(archive_path, 'r') as archive:
                filecount = len(archive.infolist())

            new_path = path.join(self.folder, f'archive_{filecount+1}')
            rename(logfile_path, new_path)

            with ZipFile(logfile_path, 'a') as archive:
                archive.write(new_path, basename(new_path))
            remove(new_path)
            self.check()

        # check if logfile reached linelimit, if so archive it and recall check
        with open(logfile_path,'r') as logfile:
            lines = len(logfile.readlines())
        if lines >= self.maxlength:
            with ZipFile(archive_path, 'r') as archive:
                filecount = len(archive.infolist())

            new_path = path.join(self.folder, f'archive_{filecount+1}')
            rename(logfile_path, new_path)

            with ZipFile(logfile_path, 'a') as archive:
                archive.write(new_path, basename(new_path))
            remove(new_path)
            self.check()

        # check if logfile reached timelimit, if so archive it and recall check
        #TODO implement later!
        return 0


    def upd_log(self, log_text, type = 0):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        message = {
            'type': self.log_type[type],
            'timestamp': f'{datetime.now().timestamp()}',
            'datetime': f'{datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}',
            'executor': f'{username}',
            'event': f'{log_text}'
        }

        with open(self.logfile_path, 'a+') as logfile:
            logfile.write(json.dumps(message))
            logfile.write('\n')

        self.check()

        return 0
