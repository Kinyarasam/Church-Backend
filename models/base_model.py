from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from datetime import datetime
import models
from uuid import uuid4


Base = declarative_base()
t_format = "%Y-%m-%dT%H:%M:%S%z"


class BaseModel:
    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DATETIME, nullable=False, default=datetime.now())
    updated_at = Column(DATETIME, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        print(kwargs)
        if kwargs:
            for key, val in kwargs.items():
                if type(val) == datetime:
                    setattr(self, key, datetime.strptime(val, t_format))
                else:
                    setattr(self, key, val)
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
            if kwargs.get("created_at", None) and isinstance(kwargs['created_at'] ,str):
                self.created_at = datetime.strptime(kwargs["created_at"], t_format)
            else:
                self.created_at = datetime.now()

            if kwargs.get("updated_at", None) and isinstance(kwargs['updated_at'] ,str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], t_format)
            else:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def save(self):
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        new_dict = self.__dict__.copy()

        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        if save_fs is None:
            if 'password' in new_dict:
                del new_dict['password']
        return new_dict


