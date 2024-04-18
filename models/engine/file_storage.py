#!/usr/bin/python3
'''
    Module for FileStorage class
'''
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary of all classes
classes = {"Amenity": Amenity, "BaseModel": BaseModel,
           "City": City, "Place": Place,
           "Review": Review, "State": State,
           "User": User}


class FileStorage:
    '''
        A class for FileStorage
    '''
    # Private class attributes
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            A method to return a dictionary of objects.
        '''
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        '''
            A method to set in __objects the obj with key <obj class name>.id
        '''
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        '''
            A method to serialize __objects to
            the JSON file (path: __file_path)
        '''
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        '''
            A method to deserialize the JSON file to __objects
        '''
        try:
            with open(self.__file_path, 'r') as f:
                js_f = json.load(f)
            for key in js_f:
                self.__objects[key] = classes[js_f[key]
                                              ["__class__"]](**js_f[key])
        except FileNotFoundError:
            print("File not found.")  # Handle file not found error
        except json.JSONDecodeError:
            print("Error decoding JSON file.")  # Handle JSON decode error

    def delete(self, obj=None):
        '''
            A method to delete obj from __objects if it’s inside
        '''
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        '''
            A method to retrieve one object
            Returns object based on the class and its ID,
            or None if not found
        '''
        if cls in classes.values() and id:
            key = str(cls.__name__) + "." + id
            if key in self.__objects.keys():
                return self.__objects[key]
            else:
                return None

    def count(self, cls=None):
        '''
            A method to count the number of objects in storage
        '''
        if cls is None:
            return len(self.__objects)

        else:
            if cls in classes.values():
                total_objs = 0
                keys = self.__objects.keys()
                for key in keys:
                    if str(cls.__name__) in key:
                        total_objs += 1
                return total_objs

    def close(self):
        '''
            A method to call reload method for
            deserializing the JSON file to __objects
        '''
        self.reload()
