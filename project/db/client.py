import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from configs import ProductionConfig, TestingConfig

class SingletonMetaclass(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

class DBClient(metaclass=SingletonMetaclass):
    """
    DBClient is singleton so can only be create once
    every connection will be use same connect session
    """
    session = None
    def __init__(self,connection_str='sqlite://'):
        self._id = id(self)
        self.connection_str = connection_str
        self.engine = create_engine(connection_str,echo=False)
        
    def get_id(self):
        return self._id

    def connect(self):
        if self.session is None:
            self.session = Session(self.engine)

    def commit(self):
        self.session.commit()

    def query(self,table_object):
        self.connect()
        result = self.session.query(table_object)
        return result
        
    def update(self,stat):
        self.connect()
        self.session.add(stat)
        self.commit()

    def create_tables(self,base):
        self.connect()
        base.metadata.create_all(self.engine)
        self.commit()

def get_db_client():
    if os.environ.get('mode')!='test':
        config = ProductionConfig
    else:
        config = TestingConfig
    connection_str = config.DB_CONNECTION_STR
    db_client = DBClient(connection_str=connection_str)
    return db_client