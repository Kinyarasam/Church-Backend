import unittest
import inspect
import pep8
from models import user
from models.base_model import BaseModel


User = user.User


class TestUserDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user/user.py',
                                    'models/user/__init__.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docsctring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[1]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[1]))


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
