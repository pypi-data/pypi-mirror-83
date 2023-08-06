from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Settings:
    def __init__(self, *args, **kwargs):
        self.sql_engine = create_engine("sqlite:///books.db")
        self.sql_engine.connect()
        self.Session = sessionmaker(bind=self.sql_engine)
