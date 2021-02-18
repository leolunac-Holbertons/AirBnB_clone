#!/usr/bin/python3
"""
    The __init__ module, initializes a ``FileStorage`` instance and loads, JSON
    file into a dictionary.
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
