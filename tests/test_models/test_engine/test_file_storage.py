#!usr/bin/python3
"""
    Test module for ``FileStorage`` class.
"""
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import unittest
from datetime import datetime
import os
import json


class TestFileStorage(unittest.TestCase):
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

    def test_instantiation(self):
        """
            test class instantiation with no arguments.
        """
        m1 = FileStorage()

    def test_filestorage_all_empty(self):
        """
            tests that FileStorage all method returns an empty dict
            if freshly instantiated.
        """
        f1 = FileStorage()
        all_before = f1.all()
        f1.reload()
        self.assertEqual(all_before, f1.all())

    def test_filestorage_all_after_new(self):
        """
            tests that FileStorage all method returns an updated dict
            if new method is called.
        """
        f1 = FileStorage()
        m1 = BaseModel()
        f1.new(m1)
        d1 = {(m1.__class__.__name__ + '.' + m1.id): m1}
        self.assertEqual(d1, f1.all())

    def test_filestorage_save(self):
        """
            tests that FileStorage .
        """
        m1 = BaseModel()
        m1.save()
        m2 = None
        with open("file.json") as f:
            m1_json = json.load(f)
        for key, value in m1_json.items():
            m2 = BaseModel(**value)
        self.assertIsNotNone(m2)
        self.assertEqual(m1.id, m2.id)

    def test_wrong_argument(self):
        """
            tests when instantiated with excess arguments.
        """
        with self.assertRaises(TypeError):
            m1 = FileStorage(1)
        with self.assertRaises(TypeError):
            m1 = FileStorage("str")
        with self.assertRaises(TypeError):
            m1 = FileStorage([])
        with self.assertRaises(TypeError):
            m1 = FileStorage(1, 2, 3, 4)

    def test_no_file_reload(self):
        """
            tests reload if file is not present.
        """
        try:
            os.remove("file.json")
        except OSError:
            pass
        f1 = FileStorage()
        f1.reload()
        with self.assertRaises(OSError):
            os.remove("file.json")

    def test_empty_reload(self):
        """
            tests reload if file is empty.
        """
        with open('file.json', 'w') as f:
            f.write("")
        f1 = FileStorage()
        all_before = f1.all()
        f1.reload()
        self.assertEqual(all_before, f1.all())

    def test_file_path_value(self):
        """Tests the value of file_path is not none"""
        f1 = FileStorage()
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_type(self):
        """Tests the value of __objects is a dictionary"""
        f1 = FileStorage()
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))
