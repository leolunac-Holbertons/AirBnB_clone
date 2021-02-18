#!/usr/bin/python3
"""
    Module containing the ``City`` class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
        The ``City`` class which inherits from ``BaseModel`` class.
    """
    state_id = ""
    name = ""
