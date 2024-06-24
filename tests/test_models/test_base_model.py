import time
import unittest
from unittest import mock
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModelDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

class TestBaseModel(unittest.TestCase):
    def test_instantiation(self):
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Test Instance"
        inst.number = 89
        attr_types = {
            "id": str,
            "created_at": datetime,
            "created_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attr_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Test Instance")
        self.assertEqual(inst.number, 89)
        
    def test_datetime_attributes(self):
        tic = datetime.now()
        inst1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)
        
    def test_uuid(self):
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
            self.assertNotEqual(inst1.id, inst2.id)
            
    def test_to_dict(self):
        my_model = BaseModel()
        my_model.name = "Test Model"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], 'Test Model')
        self.assertEqual(d['my_number'], 89)
        
    def test_to_dict_values(self):
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        bm = BaseModel()
        string = "[BaseModel] ({}) {}".format(bm.id, bm.to_dict())
        self.assertEqual(string, str(bm))
        
    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)