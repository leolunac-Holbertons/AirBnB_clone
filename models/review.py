#!/usr/bin/python3
"""
    Module containing the ``Review`` class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
        The ``Review`` class which inherits from ``BaseModel`` class.
    """
    place_id = ""
    user_id = ""
    text = ""
