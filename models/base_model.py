#!/usr/bin/python3
"""
    Module containing the ``BaseModel`` class.
"""
import models
from datetime import datetime
import uuid


class BaseModel:
    """
        BaseModel Class.
    """

    def __init__(self, *args, **kwargs):
        """Initializing an instance of ``BaseModel``.

        Args:
            *args (:obj:`list`): A list that wont be used but must be present
                to use **kwargs.
            **kwargs (:obj:`dict`): A dictionary. If set will use its key/value
                pairs to instantiate an object.
        """

        form = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs and len(kwargs) is not 0:
            for key, value in kwargs.items():
                if key == "updated_at":
                    self.updated_at = datetime.strptime(value, form)
                elif key == "created_at":
                    self.created_at = datetime.strptime(value, form)
                elif key != "__class__":
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Returns a string representation of ``BaseModel`` instance."""

        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def __setattr__(self, var, val):
        """Checks if `var` is a class variable in `self`, if so add it into
        `self.__dict__` after casting it into the correct type based on the
        class variable's type. Otherwise add var and val like normal.

        Args:
            var: The variable key to add into __dict__
            val: The corresponding value to add into __dict__
        """

        cl_dict = self.__class__.__dict__
        if var in cl_dict:
            self.__dict__[var] = type(cl_dict[var])(val)
        else:
            self.__dict__[var] = val

    def save(self):
        """Updates `updated_at`."""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing instance dict, instance __class__,
        but also, created_at, updated_at in ISO format."""

        i_dict = {}
        for key, val in self.__dict__.items():
            i_dict[key] = val
        i_dict['__class__'] = self.__class__.__name__
        i_dict['created_at'] = self.created_at.isoformat()
        i_dict['updated_at'] = self.updated_at.isoformat()

        return i_dict
