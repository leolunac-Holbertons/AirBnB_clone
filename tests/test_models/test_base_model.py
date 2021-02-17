#!usr/bin/python3
"""
    Test module for BaseModel class.
"""
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import unittest
from datetime import datetime
import json
import os


class TestBaseModel(unittest.TestCase):
    """
        test class for base_model class.
    """

    def setUp(self):
        """
            sets up for all test_ functions.
        """
        try:
            os.rename('file.json', 'temp.json')
        except OSError:
            pass
        with open('file.json', 'w') as f:
            json.dump({}, f)
        f1 = FileStorage()
        f1.reload()

    def tearDown(self):
        """
            tears down for all test_ functions.
        """
        try:
            os.remove('file.json')
            os.rename('temp.json', 'file.json')
        except OSError:
            pass

    def test_file_all_empty(self):
        """
            tests that FileStorage all method returns an empty dict
            if freshly instantiated.
        """
        f1 = FileStorage()
        f1.reload()
        m1 = BaseModel()
        all_before = models.storage.all()
        name = "BaseModel." + m1.id
        self.assertEqual(all_before, {name: m1})

    def test_file_all_after_new(self):
        """
            tests that FileStorage all method returns an updated dict
            if new method is called.
        """
        m2 = BaseModel()
        models.storage.new(m2)
        d1 = {(m2.__class__.__name__ + '.' + m2.id): m2}
        self.assertEqual(d1, models.storage.all())

    def test_empty(self):
        """
            test class instantiation with no arguments.
        """
        m1 = BaseModel()
        self.assertIsInstance(m1, BaseModel)

    def test_init_new(self):
        """
            test save method and relation to file.models.storage
        """
        m1 = BaseModel()
        with open('file.json') as f:
            temp = json.load(f)
        m1.save()
        with open('file.json') as f:
            temp2 = json.load(f)
        self.assertNotEqual(temp, temp2)

    def test_id_unique(self):
        """
            tests if an id is unique.
        """
        m1 = BaseModel()
        m2 = BaseModel()
        self.assertNotEqual(m1.id, m2.id)

    def test_id_type(self):
        """
            tests if generated id is of type string.
        """
        m1 = BaseModel()
        self.assertEqual(type(m1.id), str)

    def test_change_id(self):
        """
            tests when id is changed manually.
        """
        m1 = BaseModel()
        m2 = BaseModel()
        m1.id = m2.id
        self.assertEqual(m1.id, m2.id)

    def test_type_created_at(self):
        """
            tests the type of attribute created_at.
        """
        m1 = BaseModel()
        self.assertEqual(type(m1.created_at), datetime)

    def test_type_updated_at(self):
        """
            tests the type of attribute updated_at.
        """
        m1 = BaseModel()
        self.assertEqual(type(m1.updated_at), datetime)

    def test_created_updated_compared(self):
        """
            tests that created at is not greater than updated at
            when instantiated and when updated.
        """
        m1 = BaseModel()
        self.assertEqual(m1.updated_at, m1.created_at)
        m1.save()
        date1 = m1.created_at
        date2 = m1.updated_at
        self.assertLess(date1, date2)

    def test_createdat_two_objects(self):
        """
            tests that created_at is greater for a second created
            object than the first.
        """
        m1 = BaseModel()
        m2 = BaseModel()
        date1 = m1.created_at
        date2 = m2.created_at
        self.assertLess(date1, date2)

    def test_str_return(self):
        """
            tests the str return of class BaseModel.
        """
        m1 = BaseModel()
        class_name = "BaseModel"
        m1_id = str(m1.id)
        m1_dict = str(m1.__dict__)
        str_m1 = "[{}] ({}) {}".format(class_name, m1_id, m1_dict)
        self.assertEqual(str_m1, str(m1))

    def test_str_return_new_id(self):
        """
            tests that str will update with an updated id.
        """
        m1 = BaseModel()
        class_name = "BaseModel"
        m1.id = "1"
        m1_dict = str(m1.__dict__)
        str_m1 = "[{}] (1) {}".format(class_name, m1_dict)
        self.assertEqual(str_m1, str(m1))

    def test_save(self):
        """
            tests the save method and if the updated_at is
            greater than the created_at attribute after update.
        """
        m1 = BaseModel()
        date1 = m1.created_at
        m1.save()
        date2 = m1.updated_at
        self.assertGreater(date2, date1)

    def test_to_dict(self):
        """
            tests the method to_dict and if it matches self.__dict__.
        """
        m1 = BaseModel()
        class_dict = {"id": m1.id, "__class__": "BaseModel"}
        self.assertTrue(set(class_dict.items()).issubset(
                        set(m1.to_dict().items())))

    def test_to_dict_createdupdated(self):
        """
            tests if to_dict contains str iso of created_at
            and updated_at public attributes.
        """
        m1 = BaseModel()
        date1 = m1.updated_at.isoformat()
        date2 = m1.created_at.isoformat()
        class_dict = {"updated_at": date1, "created_at": date2}
        self.assertTrue(set(class_dict.items()).issubset(
                        set(m1.to_dict().items())))

    def test_copy_from_dict(self):
        """
            tests if copy made from to_dict has same __dict__ as
            the class it was copied from.
        """
        m1 = BaseModel()
        m2 = BaseModel(**m1.to_dict())
        self.assertTrue(set(m1.__dict__.items()).issubset(
                        set(m2.__dict__.items())))

    def test_copy_kwargs_none(self):
        """
            tests when kwargs is none in a class instantiation.
        """
        m1 = BaseModel()
        testing = {}
        m2 = BaseModel(**testing)
        self.assertFalse(set(m1.__dict__.items()).issubset(
            set(m2.__dict__.items())))

    def test_id_type(self):
        """
            tests the type of id.
        """
        m1 = BaseModel()
        self.assertIsInstance(m1.id, str)

    def test_updated_at_type(self):
        """
            tests the type of id.
        """
        m1 = BaseModel()
        self.assertIsInstance(m1.updated_at, datetime)

    def test_created_at_type(self):
        """
            tests the type of id.
        """
        m1 = BaseModel()
        self.assertIsInstance(m1.created_at, datetime)

    def test_models_storage_type(self):
        """
            tests the type of models.storage
        """
        m1 = BaseModel()
        self.assertIsInstance(models.storage, FileStorage)
