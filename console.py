#!/usr/bin/python3
"""
    Module containing the ``HBNBCommand`` class.
"""
import cmd
import shlex
import re
import ast
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
import sys


class HBNBCommand(cmd.Cmd):
    """
        The ``HBNBCommand`` class which inherits from ``cmd`` class.
    """
    prompt = '(hbnb) '

    # def __init__(self, completekey='tab', stdin=None, stdout=None):
    #    """Override __init__. Sets sys.stdout to what CLI is initilized with.
    #    """

    #    super().__init__(completekey, stdin, stdout)
    #    if stdout is not None:
    #        sys.stdout = stdout

    def emptyline(self):
        """Override emptyline from Cmd."""
        pass

    def precmd(self, arg):
        """Override precmd."""
        cl = re.search(r'^(.*)\.', arg)
        if not cl:
            return arg
        cl = cl.group(1)
        try:
            act = re.search(r'\.(.*?)\(.*\)$', arg)
            if not act:
                return arg
            act = act.group(1)
            if act == 'count':
                HBNBCommand.count(self, cl)
                return ''
            par = re.search(r'.*?\((.*)\)$', arg)
            if not par:
                return arg
            par = par.group(1)
            if act == 'update':
                temp = shlex.split(par)
                if len(temp) > 1:
                    ide = temp[0].strip(',')
                    if temp[1][0] == '{':
                        tx = re.search(r'.+,\s+(\{.*?\}).*?', par).group(1)
                        attr_dict = ast.literal_eval(tx)
                        key_str = HBNBCommand.check_class(self, cl + ' ' + ide)
                        if key_str is None:
                            return ''
                        for key, val in attr_dict.items():
                            self.do_update(cl + ' ' + ide + ' ' + key + ' ' +
                                           str(val))
                        return ''
                    else:
                        par = ''
                        for word in temp:
                            par = par + ' ' + word.strip(',')
            return act + ' ' + cl + ' ' + par
        except (NameError, SyntaxError):
            return arg

    def onecmd(self, arg):
        """Override onecmd"""
        arg = self.precmd(arg)
        return super().onecmd(arg)

    def do_quit(self, arg):
        """Quit command to exit the program:  quit
        """
        return True

    def do_create(self, arg):
        """Create an instance of a class and saves instance attributes to a
        JSON file:  create BaseModel
        """
        try:
            clazz = eval(arg)
            if not isinstance(clazz, type) or not issubclass(clazz, BaseModel):
                raise NameError
            obj = clazz()
            print(obj.id)
            obj.save()
        except SyntaxError:
            print('** class name missing **')
            return
        except NameError:
            print('** class doesn\'t exist **')
            return

    def do_show(self, arg):
        """Displays the string representation of an instance based on class
        name and instance id:  show BaseModel 1234-1234-1234
        """
        key_str = HBNBCommand.check_class(self, arg)
        if key_str is not None:
            obj = storage.all()[key_str[0]]
            print(obj)

    def do_destroy(self, arg):
        """Destroys an instance based on class name and instance id:  destory
        BaseModel 1234-1234-1234
        """
        key_str = HBNBCommand.check_class(self, arg)
        if key_str is not None:
            del storage.all()[key_str[0]]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of instances based or not on class
        name:  all BaseModel
            :  all
        """
        s = shlex.split(arg)
        inst_list = []
        if len(s) is 0:
            for obj in storage.all().values():
                inst_list.append(obj.__str__())
        else:
            try:
                eval(s[0])
                for key, val in storage.all().items():
                    if s[0] in key:
                        inst_list.append(val.__str__())
            except (NameError, SyntaxError):
                print('** class doesn\'t exist **')
                return

        print(inst_list)

    def do_update(self, arg):
        """Updates instance based on classname and id by adding/updating an
        attribute
        """
        key_str = HBNBCommand.check_class(self, arg)
        if key_str is None:
            return
        s = key_str[1]
        s_len = len(s)
        if s_len < 3:
            print('** attribute name missing **')
            return
        elif s_len < 4:
            print('** value missing **')
            return
        obj = storage.all()[key_str[0]]
        attr = s[2]
        val = s[3]
        if attr in obj.__dict__.keys():
            if type(obj.__dict__[attr]) is str:
                obj.__dict__[attr] = val
                setattr(obj, attr, val)
            elif type(obj.__dict__[attr]) is int:
                obj.__dict__[attr] = int(val)
            elif type(obj.__dict__[attr]) is float:
                obj.__dict__[attr] = float(val)
        else:
            obj.__dict__[attr] = val
        storage.save()

    def count(self, arg):
        """Get the number of instances of a class"""
        count = 0
        try:
            clazz = eval(arg)
            if not isinstance(clazz, type) or not issubclass(clazz, BaseModel):
                raise NameError
        except (NameError, SyntaxError):
            print('** class doesn\'t exist **')
            return

        for key in storage.all().keys():
            if arg in key:
                count += 1
        print(count)

    def check_class(self, arg):
        """Check if arg contains, a valid class, and id.

        Returns:
            A tuple containing the key(classname.id) and parsed arg.
            None if arg does not contain a valid class, and id.
        """
        s = shlex.split(arg)
        slen = len(s)
        if slen is 0:
            print('** class name missing **')
            return None
        try:
            clazz = eval(s[0])
            if not isinstance(clazz, type) or not issubclass(clazz, BaseModel):
                raise NameError
        except (NameError, SyntaxError):
            print('** class doesn\'t exist **')
            return None
        if len(s) < 2:
            print('** instance id missing **')
            return None
        key = s[0] + '.' + s[1]
        if key not in storage.all().keys():
            print('** no instance found **')
            return None

        return (key, s)

    do_EOF = do_quit

if __name__ == '__main__':
    HBNBCommand().cmdloop()
