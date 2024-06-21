from sqlalchemy import Column, String, Text
from models.base_model import BaseModel, Base


class Event(BaseModel, Base):
    __tablename__ = "events"
    
    location = Column(Text)
    venue = Column(Text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
