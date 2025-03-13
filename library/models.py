from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    status = Column(String)

    @property
    def is_available(self):
        return self.status == 'available'

    @classmethod
    def create(cls, session, name, status='available'):
        book = cls(name=name, status=status)
        session.add(book)
        session.commit()
        return book

    @classmethod
    def delete(cls, session, book_id):
        book = session.query(cls).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, book_id):
        return session.query(cls).filter_by(id=book_id).first()

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    book_name = Column(String, ForeignKey('books.name'))

    @classmethod
    def create(cls, session, student_name, book_name):
        track = cls(student_name=student_name, book_name=book_name)
        session.add(track)
        session.commit()
        return track

    @classmethod
    def delete(cls, session, track_id):
        track = session.query(cls).filter_by(id=track_id).first()
        if track:
            session.delete(track)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, track_id):
        return session.query(cls).filter_by(id=track_id).first()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

    @classmethod
    def create(cls, session, username, password):
        user = cls(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, username):
        return session.query(cls).filter_by(username=username).first()