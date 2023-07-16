from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = "mysql+mysqlconnector://709i2uqaelp9ga69jil1:pscale_pw_PXSDpQ235GXkfXubFM15zLw5tctdxkfMimDkJSy8VLF@aws.connect.psdb.cloud:3306/onibus"
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
