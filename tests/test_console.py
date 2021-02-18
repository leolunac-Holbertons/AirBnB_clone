#!/usr/bin/python3
"""
    Test module for console.
"""
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from unittest.mock import create_autospec
from console import HBNBCommand
import unittest
import json
import os
import models.engine.file_storage
import sys


class TestConsole(unittest.TestCase):
    """
        Test class for HBNBCommandClass.
    """

    def setUp(self):
        """setup for tests."""

        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        sys.stdout = self.mock_stdout
        try:
            os.remove('file.json')
        except OSError:
            pass

        f1 = models.engine.file_storage.FileStorage()
        f1.reload()

    def tearDown(self):
        """teardown for tests."""
        sys.stdout = sys.__stdout__
        try:
            os.remove('file.json')
        except OSError:
            pass

    def create(self):
        """Return a console object that uses `mock_stdin` and `mock_stdout`."""

        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def _last_write(self, nr=None):
        """Returns last `n` output lines."""

        if nr is None:
            return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[:]))
            # return self.mock_stdout.write.call_args[0][0]

        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-nr:]))

    def test_empty(self):
        """Test empty input"""
        cli = self.create()
        self.assertIsNone(cli.onecmd(""))
        self.assertEqual("", self._last_write())

    def test_create_0(self):
        """Test create command without arguments"""
        cli = self.create()
        ex_o = "** class name missing **\n"
        cli.onecmd("create")
        self.assertEqual(ex_o, self._last_write())

    def test_create_1(self):
        """Test create command with invalid class name"""
        cli = self.create()
        ex_o = "** class doesn't exist **\n"
        cli.onecmd("create DontExist")
        self.assertEqual(ex_o, self._last_write())

    def test_create_2(self):
        """Test create command with valid class"""
        cli = self.create()
        cli.onecmd("create User")
        self.assertNotEqual('', self._last_write())

    def test_help_command(self):
        """Test help"""
        cli = self.create()
        cli.onecmd("help")
        ex_o = "\nDocumented commands (type help <topic>):\n" \
            "========================================\n" \
            "EOF  all  create  destroy  help  quit  show  update\n\n"
        self.assertEqual(ex_o, self._last_write())

    def test_EOF_help(self):
        """Test help for EOF command"""
        cli = self.create()
        cli.onecmd("help EOF")
        self.assertIsNotNone(self._last_write())

    def test_all_help(self):
        """Test help for all command"""
        cli = self.create()
        cli.onecmd("help all")
        self.assertIsNotNone(self._last_write())

    def test_create_help(self):
        """Test help for create command"""
        cli = self.create()
        cli.onecmd("help create")
        self.assertIsNotNone(self._last_write())

    def test_destroy_help(self):
        """Test help for destroy command"""
        cli = self.create()
        cli.onecmd("help destroy")
        self.assertIsNotNone(self._last_write())

    def test_help_help(self):
        """Test help for help command"""
        cli = self.create()
        cli.onecmd("help help")
        self.assertIsNotNone(self._last_write())

    def test_quit_help(self):
        """Test help for quit command"""
        cli = self.create()
        cli.onecmd("help quit")
        self.assertIsNotNone(self._last_write())

    def test_show_help(self):
        """Test help for show command"""
        cli = self.create()
        cli.onecmd("help show")
        self.assertIsNotNone(self._last_write())

    def test_update_help(self):
        """Test help for update command"""
        cli = self.create()
        cli.onecmd("help update")
        self.assertIsNotNone(self._last_write())

    def test_quit(self):
        """Test quit command"""
        cli = self.create()
        cli.onecmd("quit")
        self.assertEqual("", self._last_write())

    def test_EOF(self):
        """Test EOF command"""
        cli = self.create()
        cli.onecmd("EOF")
        self.assertEqual("", self._last_write())

    def test_show_0(self):
        """Test show command without arguments"""
        cli = self.create()
        ex_o = "** class name missing **\n"
        cli.onecmd("show")
        self.assertEqual(ex_o, self._last_write())

    def test_show_1(self):
        """Test show command with invalid class name"""
        cli = self.create()
        ex_o = "** class doesn't exist **\n"
        cli.onecmd("show DontExist")
        self.assertEqual(ex_o, self._last_write())

    def test_show_2(self):
        """Test show command with valid class, no id"""
        cli = self.create()
        cli.onecmd("show User")
        self.assertEqual('** instance id missing **\n', self._last_write())

    def test_show_3(self):
        """Test show command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("show User 1010101")
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_show_4(self):
        """Test show command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("show User")
        cmp_str = '** instance id missing **\n'
        self.assertEqual(cmp_str, self._last_write())

    def test_show_5(self):
        """Test show() command with invalid class name"""
        cli = self.create()
        ex_o = "** class doesn't exist **\n"
        cli.onecmd("DontExist.show()")
        self.assertEqual(ex_o, self._last_write())

    def test_show_6(self):
        """Test show() command with valid class, no id"""
        cli = self.create()
        cli.onecmd("User.show()")
        self.assertEqual('** instance id missing **\n', self._last_write())

    def test_show_7(self):
        """Test show() command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("User.show(1010101)")
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_show_8(self):
        """Test show() command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("DontExist.show(")
        self.assertEqual('*** Unknown syntax: DontExist.show(\n',
                         self._last_write())

    def test_show_9(self):
        """Test show() command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("create User")
        id_user = self._last_write()
        self.mock_stdout.reset_mock()
        cli.onecmd("User.show({})".format(id_user))
        cmp_str = '** instance id missing **\n'
        self.assertNotEqual(cmp_str, self._last_write())

    def test_show_10(self):
        """Test show() with BaseModel"""
        cli = self.create()
        cli.onecmd('create BaseModel')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('BaseModel.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_show_11(self):
        """Test show() with State"""
        cli = self.create()
        cli.onecmd('create State')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('State.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_show_12(self):
        """Test show() with City"""
        cli = self.create()
        cli.onecmd('create City')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('City.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_show_13(self):
        """Test show() with Amenity"""
        cli = self.create()
        cli.onecmd('create Amenity')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('Amenity.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_show_14(self):
        """Test show() with Place"""
        cli = self.create()
        cli.onecmd('create Place')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('Place.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_show_15(self):
        """Test show() with Review"""
        cli = self.create()
        cli.onecmd('create Review')
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('Review.show({})'.format(o_id))
        self.assertIn(o_id, self._last_write())

    def test_destroy_0(self):
        """Test show command without arguments"""
        cli = self.create()
        ex_o = "** class name missing **\n"
        cli.onecmd("destroy")
        self.assertEqual(ex_o, self._last_write())

    def test_destroy_1(self):
        """Test destroy command with invalid class name"""
        cli = self.create()
        ex_o = "** class doesn't exist **\n"
        cli.onecmd("destroy DontExist")
        self.assertEqual(ex_o, self._last_write())

    def test_destroy_2(self):
        """Test destroy command with valid class, no id"""
        cli = self.create()
        cli.onecmd("destroy User")
        self.assertEqual('** instance id missing **\n', self._last_write())

    def test_destroy_3(self):
        """Test destroy command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("destroy User 1010101")
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_4(self):
        """Test destroy command with valid input"""
        cli = self.create()
        cli.onecmd("destroy User")
        cli.onecmd("destroy User {}".format(self._last_write()))
        self.assertNotEqual('** instance id missing **\n', self._last_write())

    def test_destroy_5(self):
        """Test destroy() command with invalid class name"""
        cli = self.create()
        ex_o = "** class doesn't exist **\n"
        cli.onecmd("DontExist.destroy()")
        self.assertEqual(ex_o, self._last_write())

    def test_destroy_6(self):
        """Test destroy() command with valid class, no id"""
        cli = self.create()
        cli.onecmd("User.destroy()")
        self.assertEqual('** instance id missing **\n', self._last_write())

    def test_destroy_7(self):
        """Test destroy() command with valid class but invalid id"""
        cli = self.create()
        cli.onecmd("User.destroy(1010101)")
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_8(self):
        """Test destroy() command with valid input"""
        cli = self.create()
        cli.onecmd("create User")
        id_user = self._last_write()
        self.mock_stdout.reset_mock()
        cli.onecmd("User.destroy(\"{}\")".format(id_user[:-1]))
        self.assertEqual('', self._last_write())

    def test_destroy_9(self):
        """Test destroy() with BaseModel"""
        cli = self.create()
        cl = 'BaseModel'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_10(self):
        """Test destroy() with State"""
        cli = self.create()
        cl = 'State'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_11(self):
        """Test destroy() with Place"""
        cli = self.create()
        cl = 'Place'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_12(self):
        """Test destroy() with Amenity"""
        cli = self.create()
        cl = 'Amenity'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_13(self):
        """Test destroy() with Review"""
        cli = self.create()
        cl = 'Review'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_destroy_14(self):
        """Test destroy() with Review"""
        cli = self.create()
        cl = 'City'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.destroy({})'.format(cl, o_id))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertEqual('** no instance found **\n', self._last_write())

    def test_all_0(self):
        """Test all command without arguments"""
        cli = self.create()
        cli.onecmd("create User")
        self.mock_stdout.reset_mock()
        with open('file.json') as f:
            s = json.load(f)
        test_dict = {}
        test_list = []
        for key, val in s.items():
            test_dict[key] = eval(val["__class__"])(**val)
        for obj in test_dict.values():
            test_list.append(obj.__str__())
        cli.onecmd("all")
        self.assertEqual(str(test_list), self._last_write()[:-1])

    def test_all_1(self):
        """Test all() with BaseModel"""
        cli = self.create()
        cli.onecmd('create BaseModel')
        self.mock_stdout.reset_mock()
        cli.onecmd('BaseModel.all()')
        self.assertIn('[BaseModel]', self._last_write())

    def test_all_2(self):
        """Test all() with Review"""
        cli = self.create()
        cli.onecmd('create Review')
        self.mock_stdout.reset_mock()
        cli.onecmd('Review.all()')
        self.assertIn('[Review]', self._last_write())

    def test_all_3(self):
        """Test all() with User"""
        cli = self.create()
        cli.onecmd('create User')
        self.mock_stdout.reset_mock()
        cli.onecmd('User.all()')
        self.assertIn('[User]', self._last_write())

    def test_all_4(self):
        """Test all() with State"""
        cli = self.create()
        cli.onecmd('create State')
        self.mock_stdout.reset_mock()
        cli.onecmd('State.all()')
        self.assertIn('[State]', self._last_write())

    def test_all_5(self):
        """Test all() with City"""
        cli = self.create()
        cli.onecmd('create City')
        self.mock_stdout.reset_mock()
        cli.onecmd('City.all()')
        self.assertIn('[City]', self._last_write())

    def test_all_6(self):
        """Test all() with Amenity"""
        cli = self.create()
        cli.onecmd('create Amenity')
        self.mock_stdout.reset_mock()
        cli.onecmd('Amenity.all()')
        self.assertIn('[Amenity]', self._last_write())

    def test_all_7(self):
        """Test all() with Place"""
        cli = self.create()
        cli.onecmd('create Place')
        self.mock_stdout.reset_mock()
        cli.onecmd('Place.all()')
        self.assertIn('[Place]', self._last_write())

    def test_count_0(self):
        """Test count() with BaseModel"""
        cli = self.create()
        cli.onecmd('create BaseModel')
        self.mock_stdout.reset_mock()
        cli.onecmd('BaseModel.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_1(self):
        """Test count() with User"""
        cli = self.create()
        cli.onecmd('create User')
        self.mock_stdout.reset_mock()
        cli.onecmd('User.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_2(self):
        """Test count() with State"""
        cli = self.create()
        cli.onecmd('create State')
        self.mock_stdout.reset_mock()
        cli.onecmd('State.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_3(self):
        """Test count() with Place"""
        cli = self.create()
        cli.onecmd('create Place')
        self.mock_stdout.reset_mock()
        cli.onecmd('Place.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_4(self):
        """Test count() with City"""
        cli = self.create()
        cli.onecmd('create City')
        self.mock_stdout.reset_mock()
        cli.onecmd('City.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_5(self):
        """Test count() with Amenity"""
        cli = self.create()
        cli.onecmd('create Amenity')
        self.mock_stdout.reset_mock()
        cli.onecmd('Amenity.count()')
        self.assertEqual('1\n', self._last_write())

    def test_count_6(self):
        """Test count() with Review"""
        cli = self.create()
        cli.onecmd('create Review')
        self.mock_stdout.reset_mock()
        cli.onecmd('Review.count()')
        self.assertEqual('1\n', self._last_write())

    def test_update_0(self):
        """Test update on BaseModel with valid input"""
        cli = self.create()
        cli.onecmd('create BaseModel')
        id_base = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('update BaseModel {} email wow'.format(id_base))
        cli.onecmd('show BaseModel {}'.format(id_base))
        self.assertIn("'email': 'wow'", self._last_write()[:-1])

    def test_update_1(self):
        """Test update() with BaseModel"""
        cli = self.create()
        cl = 'BaseModel'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_2(self):
        """Test update() with User"""
        cli = self.create()
        cl = 'User'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_3(self):
        """Test update() with State"""
        cli = self.create()
        cl = 'State'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_4(self):
        """Test update() with City"""
        cli = self.create()
        cl = 'City'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_5(self):
        """Test update() with Place"""
        cli = self.create()
        cl = 'Place'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_6(self):
        """Test update() with Amenity"""
        cli = self.create()
        cl = 'Amenity'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_7(self):
        """Test update() with Review"""
        cli = self.create()
        cl = 'Review'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {}, {})'.format(cl, o_id, 'hi', 'there'))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_8(self):
        """Test update() with BaseModel"""
        cli = self.create()
        cl = 'BaseModel'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_9(self):
        """Test update() with User"""
        cli = self.create()
        cl = 'User'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_10(self):
        """Test update() with State"""
        cli = self.create()
        cl = 'State'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_11(self):
        """Test update() with Amenity"""
        cli = self.create()
        cl = 'Amenity'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_12(self):
        """Test update() with City"""
        cli = self.create()
        cl = 'City'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_13(self):
        """Test update() with Place"""
        cli = self.create()
        cl = 'Place'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())

    def test_update_14(self):
        """Test update() with Review"""
        cli = self.create()
        cl = 'Review'
        cli.onecmd('create {}'.format(cl))
        o_id = self._last_write()[:-1]
        self.mock_stdout.reset_mock()
        cli.onecmd('{}.update({}, {})'.format(cl, o_id, "{ 'hi': 'there' }"))
        cli.onecmd('{}.show({})'.format(cl, o_id))
        self.assertIn("'hi': 'there'", self._last_write())
