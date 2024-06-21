from sqlalchemy import Column, String, Text
from models.base_model import BaseModel, Base
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel, Base):
    __tablename__ = "users"

    email = Column(String(60))
    phone_number = Column(String(12))
    password = Column(Text)
    role = Column(String(60))

    def __setattr__(self, __name, __value):
        ROLES = ["basic", "user", "admin", "super_admin"]
        if __name == "role" and str(__value).lower() not in ROLES:
            __value = "basic"

        if __name == "password":
            __value = bcrypt.generate_password_hash(__value).decode('utf-8')
        return super().__setattr__(__name, __value)
    
    def verify_passwd(self, passwd: str = None) -> bool:
        if passwd is None:
            return False
        if not isinstance(passwd, str):
            return False
        return bcrypt.check_password_hash(self.password, passwd)

