#!/usr/bin/python3
"""
This module defines the FileStorage class for serializing and
deserializing instances to JSON files.
"""

import json
from typing import Dict, Optional, Type, Union
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Define a mapping of class names to corresponding class types
classes: Dict[str, Type[BaseModel]] = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """Serializes instances to a JSON file and
    deserializes JSON file to instances"""

    def __init__(self) -> None:
        """Initialize FileStorage with an empty dictionary for objects"""
        self.__file_path: str = "file.json"
        self.__objects: Dict[str, BaseModel] = {}

    def all(self) -> Dict[str, BaseModel]:
        """Returns the dictionary of stored objects"""
        return self.__objects

    def new(self, obj: BaseModel) -> None:
        """Adds a new object to the dictionary of stored objects"""
        key: str = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self) -> None:
        """Serializes the stored objects to a JSON file"""
        with open(self.__file_path, mode="w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self) -> None:
        """Deserializes the JSON file to populate the stored objects"""
        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as f:
                self.__objects = {k: classes[
                    k.split('.')[0]](**v) for k, v in json.load(f).items()}
        except FileNotFoundError:
            pass

    def delete(self, obj: Optional[BaseModel] = None) -> None:
        """Deletes an object from the stored objects dictionary"""
        if obj:
            key: str = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls: Type[BaseModel], id: str) -> Union[BaseModel, None]:
        """Retrieves an object from the stored objects dictionary"""
        key: str = f"{cls.__name__}.{id}"
        return self.__objects.get(key)

    def count(self, cls: Optional[Type[BaseModel]] = None) -> int:
        """Counts the number of objects in storage,
        optionally filtered by class type"""
        if cls:
            return sum(
                1 for obj in self.__objects.values() if isinstance(obj, cls))
        else:
            return len(self.__objects)

    def close(self) -> None:
        """Reloads the stored objects from the JSON file"""
        self.reload()
