#!/usr/bin/python3
"""
    Module containing the ``FileStorage`` class.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
        The ``FileStorage`` class.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
            Returns the class `__objects` variable.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
            Adds a key/value pair to class `__objects` variable.

            Args:
                obj: (:obj:`BaseModel`): A `BaseModel` instance.
        """
        key_obj = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key_obj] = obj

    def save(self):
        """
            Serializes `__object` to the JSON file specified by `__file_path`.
        """
        try:
            with open(FileStorage.__file_path, 'w') as f:
                obj_dict = {}
                for key, val in FileStorage.__objects.items():
                    obj_dict[key] = val.to_dict()
                json.dump(obj_dict, f)
        except IOError:
            pass

    def reload(self):
        """
            Deserialize the JSON file specified by `__file_path` to `__objects`
            .
        """
        try:
            FileStorage.__objects.clear()
            with open('file.json', 'r') as f:
                all_obj = json.load(f)
                for key, val in all_obj.items():
                    FileStorage.__objects[key] = eval(val["__class__"])(**val)
        except (IOError, ValueError):
            pass
