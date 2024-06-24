from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Channel(BaseModel, Base):
    __tablename__ = 'channels'
    
    name = Column(String(128), nullable=False)
    members = relationship("User",
                           secondary="channel_members",
                           viewonly=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
