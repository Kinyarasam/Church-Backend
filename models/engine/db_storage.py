from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from models.base_model import Base
from models.user import User


class DBStorage:
    _session = None
    _engine = None

    def __init__(self):
        self._engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Base.metadata.drop_all(self._engine) # Remember to comment this in production code

    def find(self, cls=None, *args, **kwargs):
        result = None
        if kwargs:
            result = self._session.query(cls).filter_by(**kwargs).first()
        return result
    
    def new(self, obj=None):
        if obj is None:
            return
        self._session.add(obj)
        self._session.flush()
        self._session.refresh(obj)

    def save(self):
        self._session.commit()

    def reload(self):
        Base.metadata.create_all(self._engine)
        session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self._session = Session
