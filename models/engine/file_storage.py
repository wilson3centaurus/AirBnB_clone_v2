#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        if cls is None:
            return self.__objects
        return {key: value for key, value in self.__objects.items() if isinstance(value, cls)}

    def new(self, obj):
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        json_objects = {}
        for key, value in self.__objects.items():
            json_objects[key] = value.to_dict()

        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
            for key, value in json_objects.items():
                class_name = value["__class__"]
                class_instance = getattr(models, class_name)(**value)
                self.__objects[key] = class_instance
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        self.reload()

    def get(self, cls, id):
        """
        Retrieves an object based on its class and ID.

        Args:
            cls: The class of the object to retrieve.
            id: The ID of the object to retrieve.

        Returns:
            The object if found, otherwise None.
        """
        objects = self.all(cls)
        for obj in objects.values():
            if obj.id == id:
                return obj
        return None

     def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class.

        Args:
            cls: The class to count objects for (optional).

        Returns:
            The number of objects in storage matching the given class.
            If no class is provided, returns the count of all objects in storage.
        """
        if cls is None:
            return len(self.__objects)
        return sum(1 for obj in self.__objects.values() if isinstance(obj, cls))

