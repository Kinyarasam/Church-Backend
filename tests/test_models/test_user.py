import unittest
import inspect
from models import user
from models.base_model import BaseModel


User = user.User


class TestUserDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_f = inspect.getmembers(User, inspect.isfunction)
        

class TestUser(unittest.TestCase):
    def test_is_subclass(self):
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))
        
    def test_email_attribute(self):
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, None)
        
    def test_first_name_attribute(self):
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, None)

    def test_last_name_attribute(self):
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, None)

    def test_password_attribute(self):
        user = User()
        self.assertTrue(user, "password")
        self.assertEqual(user.password, None)
        
    def test_role_attribute(self):
        user = User()
        self.assertTrue(user, "role")
        self.assertEqual(user.role, None)
        
    def test_to_dict_creates_dict(self):
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))
        
    def test_str(self):
        user = User()
        string = "[User] ({}) {}".format(user.id, user.to_dict())
        self.assertEqual(string, str(user))
