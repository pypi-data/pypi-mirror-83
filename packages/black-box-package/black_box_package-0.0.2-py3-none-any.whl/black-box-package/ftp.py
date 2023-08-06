from ftplib import FTP

class Ftp():

    def __init__(self, host, user, password, port):
        self.ftp = FTP()
        self.ftp.connect(
            host=host,
            port=port
        )
        self.ftp.login(
            user=user, 
            passwd=password
        )

    def cd(self, path):
        try:
            self.ftp.cwd(path)
            return 'Success'
        except Exception as error:
            return str(error)

    def upload(self, name, file):
        try:
            self.ftp.storbinary(
                'STOR ' + name, 
                file
            )
            return 'Success'
        except Exception as error:
            return str(error)

    def close_connection(self):
        try:
            self.ftp.close()
            return 'Success'
        except Exception as error:
            return str(error)

