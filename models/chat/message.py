from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base_model import BaseModel, Base


class Message(BaseModel, Base):
    __tablename__ = "messages"
    
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    channel_id = Column(String(60), ForeignKey('channels.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
    
    # relationships
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)