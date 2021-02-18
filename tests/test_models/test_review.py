#!usr/bin/python3
"""
    Test module for Review class.
"""
from models.base_model import BaseModel
from models.review import Review
import unittest
from datetime import datetime


class TestReview(unittest.TestCase):
    """
        test class for review class.
    """

    def test_empty(self):
        """
            test class instantiation with no arguments.
        """
        m1 = Review()

    def test_if_base_model(self):
        """
            tests if user is an instance of BaseModel
        """
        m1 = Review()
        self.assertTrue(isinstance(m1, BaseModel))

    def test_id_unique(self):
        """
            tests if an id is unique.
        """
        m1 = Review()
        m2 = Review()
        self.assertNotEqual(m1.id, m2.id)

    def test_id_type(self):
        """
            tests if generated id is of type string.
        """
        m1 = Review()
        self.assertEqual(type(m1.id), str)

    def test_change_id(self):
        """
            tests when id is changed manually.
        """
        m1 = Review()
        m2 = Review()
        m1.id = m2.id
        self.assertEqual(m1.id, m2.id)

    def test_type_created_at(self):
        """
            tests the type of attribute created_at.
        """
        m1 = Review()
        self.assertEqual(type(m1.created_at), datetime)

    def test_type_updated_at(self):
        """
            tests the type of attribute updated_at.
        """
        m1 = Review()
        self.assertEqual(type(m1.updated_at), datetime)

    def test_created_updated_compared(self):
        """
            tests that created at is not greater than updated at
            when instantiated and when updated.
        """
        m1 = Review()
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
        m1 = Review()
        m2 = Review()
        date1 = m1.created_at
        date2 = m2.created_at
        self.assertLess(date1, date2)

    def test_str_return(self):
        """
            tests the str return of class Review.
        """
        m1 = Review()
        class_name = "Review"
        m1_id = str(m1.id)
        m1_dict = str(m1.__dict__)
        str_m1 = "[{}] ({}) {}".format(class_name, m1_id, m1_dict)
        self.assertEqual(str_m1, str(m1))

    def test_str_return_new_id(self):
        """
            tests that str will update with an updated id.
        """
        m1 = Review()
        class_name = "Review"
        m1.id = "1"
        m1_dict = str(m1.__dict__)
        str_m1 = "[{}] (1) {}".format(class_name, m1_dict)
        self.assertEqual(str_m1, str(m1))

    def test_save(self):
        """
            tests the save method and if the updated_at is
            greater than the created_at attribute after update.
        """
        m1 = Review()
        date1 = m1.created_at
        m1.save()
        date2 = m1.updated_at
        self.assertGreater(date2, date1)

    def test_to_dict(self):
        """
            tests the method to_dict and if it matches self.__dict__.
        """
        m1 = Review()
        class_dict = {"id": m1.id, "__class__": "Review"}
        self.assertTrue(set(class_dict.items()).issubset(
                        set(m1.to_dict().items())))

    def test_to_dict_createdupdated(self):
        """
            tests if to_dict contains str iso of created_at
            and updated_at public attributes.
        """
        m1 = Review()
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
        m1 = Review()
        m2 = Review(**m1.to_dict())
        self.assertTrue(set(m1.__dict__.items()).issubset(
                        set(m2.__dict__.items())))

    def test_copy_kwargs_none(self):
        """
            tests when kwargs is none in a class instantiation.
        """
        m1 = Review()
        testing = {}
        m2 = Review(**testing)
        self.assertFalse(set(m1.__dict__.items()).issubset(
            set(m2.__dict__.items())))

    def test_user_id(self):
        """
            tests the class attribute user_id type.
        """
        self.assertEqual(type(Review.user_id), str)

    def test_place_id(self):
        """
            tests the class attribute place_id type.
        """
        self.assertEqual(type(Review.place_id), str)

    def test_text(self):
        """
            tests the class attribute text type.
        """
        self.assertEqual(type(Review.text), str)
