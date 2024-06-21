from typing import Dict, Tuple, Union, Literal
from models import storage
from models.user import User
from flask_jwt_extended import create_access_token


class AuthService:

    @staticmethod
    def register_user(user_data: Dict[str, str] = None) -> Tuple[Union[Literal[200, 400]], str]:
        if user_data is None:
            return None
        if not isinstance(user_data, dict):
            return None
        required = ["email", "password"]
        missing = [param for param in required if param not in user_data.keys()]
        if missing:
            return (400, "Missing `{}`".format(missing[0]))
        user = storage.find(User, email=user_data["email"])
        if user is None:
            new_user = User(**user_data)
            new_user.save()
            return (201, "User Created!")
        return (400, "User Already Exists!")
    
    @classmethod
    def login(cls, user_data: Dict[str, str] = None) -> Tuple:
        """
        Generate a user token
        """
        if user_data is None:
            return None, None
        if not isinstance(user_data, dict):
            return None, None
        
        required = ["email", "password"]
        missing = [param for param in required if param not in user_data.keys()]
        if missing:
            return (400, "Missing `{}`".format(missing[0]))
        user = cls.verify_user(user_data.get('email', None), user_data.get('password', None))
        if user[0] is None:
            return (404, "User Not Found!")
        response = user[1].to_dict()
        response["token"] = user[0]
        return (200, response)
    
    @staticmethod
    def verify_user(email: str, passwd: str) -> Tuple[str, User]:
        if email is None or passwd is None:
            return None, None
        if not isinstance(email, str) or not isinstance(passwd, str):
            return None, None
        user = storage.find(User, email=email)
        if user and user.verify_passwd(passwd):
            access_token = create_access_token(identity={'id': user.id, 'email': user.email})
            return (access_token, user)
        return None, None
            
        