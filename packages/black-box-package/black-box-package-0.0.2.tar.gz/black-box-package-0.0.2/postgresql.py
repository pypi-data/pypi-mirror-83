from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker


class PostgreSql():
    
    def __init__(self, user, password, host, port, database):
        self.connection = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection)

    def get_engine(self):
        return self.engine

    def create_session(self):
        try:
            self.Session = sessionmaker(self.engine)
            self.session = self.Session()
            return self.session
        except Exception as error:
            return str(error)

    def close_session(self):
        try:
            self.session.close()
            return 'Session closed'
        except Exception as error:
            return str(error)
