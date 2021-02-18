#!/usr/bin/python3
"""
    Module containing the ``User`` class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
        The ``User`` class which inherits from ``BaseModel`` class.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
