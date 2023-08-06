import cx_Oracle
from sqlalchemy import create_engine


class Oracle():

    def __init__(self, user, password, host, port, service_name, engine='oracle'):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name

        if engine == 'sqlalchemy':
            self.create_engine_sqlalchemy()
        else:
            self.create_engine_cx_oracle()

    def create_engine_cx_oracle(self):

        self.dns = f"(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = {self.host})(PORT = {self.port})) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = {self.service_name})))"

        self.connection = cx_Oracle.connect(
            self.user, 
            self.password, 
            self.dns, 
            encoding="UTF-8"
        )

    def create_engine_sqlalchemy(self):

        self.connection = create_engine(
            f"oracle+cx_oracle://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}",
            max_identifier_length=128
        )

    def get_engine(self):
        return self.connection