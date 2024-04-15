#!/usr/bin/python3
"""Console module"""

import cmd
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex

cls_dict = {
    "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class CommandPrompt(cmd.Cmd):
    """HBNH prompt"""
    prompt = '(hbnb) '

    def do_EOF(self, _):
        """Exit console"""
        return True

    def emptyline(self):
        """Ignore empty"""
        return False

    def do_quit(self, _):
        """Exit program"""
        return True

    def parse_kv(self, arg_list):
        """Dictionary from string list"""
        new_dict = {}
        for element in arg_list:
            if '=' in element:
                k, v = element.split('=', 1)
                if v[0] == v[-1] == '"':
                    v = shlex.split(v)[0].replace('_', ' ')
                else:
                    v = self.convert_value(v)
                new_dict[k] = v
        return new_dict

    @staticmethod
    def convert_value(value):
        """Convert string to int/float"""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def do_create(self, arg):
        """Instantiate class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return False
        if args[0] in cls_dict:
            new_dict = self.parse_kv(args[1:])
            instance = cls_dict[args[0]](**new_dict)
            print(instance.id)
            instance.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Print instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return False
        if args[0] in cls_dict:
            self.print_instance(args)
        else:
            print("** class doesn't exist **")

    def print_instance(self, args):
        """Prints instance string"""
        if len(args) > 1:
            key = f"{args[0]}.{args[1]}"
            all_objs = storage.all()
            if key in all_objs:
                print(all_objs[key])
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")

    def do_destroy(self, arg):
        """Delete instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] in cls_dict:
            self.delete_instance(args)
        else:
            print("** class doesn't exist **")

    def delete_instance(self, args):
        """Deletes instance"""
        if len(args) > 1:
            key = f"{args[0]}.{args[1]}"
            all_objs = storage.all()
            if key in all_objs:
                all_objs.pop(key)
                storage.save()
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")

    def do_all(self, arg):
        """List instances"""
        args = shlex.split(arg)
        if not args:
            obj_dict = storage.all()
        elif args[0] in cls_dict:
            obj_dict = storage.all(cls_dict[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        self.print_all(obj_dict)

    @staticmethod
    def print_all(obj_dict):
        """Prints all objects"""
        obj_list = [str(obj) for obj in obj_dict.values()]
        print(f"[{', '.join(obj_list)}]")

    def do_update(self, arg):
        """Modify instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] in cls_dict:
            self.update_instance(args)
        else:
            print("** class doesn't exist **")

    def update_instance(self, args):
        """Updates instance"""
        if len(args) > 1:
            key = f"{args[0]}.{args[1]}"
            all_objs = storage.all()
            if key in all_objs:
                self.set_attribute(all_objs[key], args)
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")

    def set_attribute(self, obj, args):
        """Set attr value"""
        if len(args) > 2:
            if len(args) > 3:
                self.convert_attribute(args)
                setattr(obj, args[2], args[3])
                obj.save()
            else:
                print("** value missing **")
        else:
            print("** attribute name missing **")

    @staticmethod
    def convert_attribute(args):
        """Converts attributes"""
        integers = {"number_rooms", "number_bathrooms",
                    "max_guest", "price_by_night"}
        floats = {"latitude", "longitude"}
        if args[0] == "Place":
            if args[2] in integers:
                args[3] = int(args[3])
            elif args[2] in floats:
                args[3] = float(args[3])


if __name__ == '__main__':
    CommandPrompt().cmdloop()
