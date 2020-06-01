# -*- coding: utf-8 -*-

from enum import Enum
from orator import Model, SoftDeletes
from orator.orm import has_many, belongs_to

# class PetType(Enum):
#     none = None
#     cat = "cat"
#     dog = "dog"
    

# class Sex(Enum):
#     none = None
#     masc = "masc"
#     fem = "fem"


class Pet(SoftDeletes, Model):
    __table__ = 'pet'
    __fillable__ = ['name', 'breed', 'petType', 'sex']
    __timestamps__ = True
    __dates__ = ['deleted_at']

    @has_many('pet_id', 'id')
    def photos(self):
        return Photo

    def __init__(self, *args, **kwargs):
        super().__init__()

        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def to_json(self):
        return {"id": self.id, "name": self.name, "breed": self.breed, "petType": self.petType, "sex": self.sex}




class Photo(SoftDeletes, Model):
    __table__ = 'photo'
    __fillable__ = ['path']
    __timestamps__ = True
    __dates__ = ['deleted_at']
    __with__ = ['pet']

    @belongs_to('pet_id', 'id')
    def pet(self):
        return Pet

    def __init__(self, *args, **kwargs):
        super().__init__()

        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def to_json(self):
        return {"id": self.id, "path": self.path, "pet_id": self.pet_id}


