from typing import Dict, Tuple, Union, Literal
from models import storage
from models.user import User


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
        user = storage.find(User, user_data["email"])
        if user is None:
            new_user = User(**user_data)
            print(new_user.__dict__)
            print(new_user.to_dict(save_fs=1))
            return (200, "User Created!")
        return (400, "User Already Exists!")
        
            
        