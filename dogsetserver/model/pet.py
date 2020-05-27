# -*- coding: utf-8 -*-

from enum import Enum

class PetType(Enum):
    none = None
    cat = "cat"
    dog = "dog"
    

class Sex(Enum):
    none = None
    masc = "masc"
    fem = "fem"


class Pet:
    def __init__(self, id=None, name="", breed="", petType=PetType.none, sex=Sex.none, photos=[]):
        self.id = id;
        self.name = name;
        self.breed = breed;
        self.petType = petType;
        self.sex = sex;
        self.photos = photos;
        print(PetType.cat)

    def to_json(self):
        return {"id": self.id, "name": self.name, "breed": self.breed, "petType": self.petType, "sex": self.sex}


