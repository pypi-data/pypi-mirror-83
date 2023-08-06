from sqlalchemy import Column, Integer, String, DateTime, Text
from .base import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    author = Column(String(255))
    latest_page = Column(Integer)
    book_path = Column(Text)
    stop_at_page = Column(Integer)
    last_read = Column(DateTime)

    def __repr__(self):
        return self.name
