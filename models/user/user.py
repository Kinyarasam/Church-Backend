from sqlalchemy import Column, String, Text
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    __tablename__ = "users"

    email = Column(String(60))
    phone_number = Column(String(60))
    password = Column(Text)
