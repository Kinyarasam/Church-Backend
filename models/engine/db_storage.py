from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict
from config import Config

def Db(app):
    return SQLAlchemy(app)
from models.base_model import Base
from models.user import User
from models.event import Event


classes = {
    "User": User, "Event": Event
}


class DBStorage:
    _session = None
    _engine = None
    metadata = Base.metadata
    engine = None

    def __init__(self):
        self._engine = self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        # Base.metadata.drop_all(self._engine) # Remember to comment this in production code
        pass
        
    def all(self, cls=None) -> Dict[str, object]:
        tmp_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self._session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    tmp_dict[key] = obj
        return tmp_dict
    
    def get(self, cls = None, id: str = None):
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                all_cls = self._session.query(cls).all()
                for value in all_cls:
                    if value.id == id:
                        return value
        return None

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
