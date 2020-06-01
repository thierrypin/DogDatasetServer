# -*- coding: utf-8 -*-

import os
import json
import base64
import datetime

from enum import Enum

from orator import DatabaseManager, Model

from ..util.config import config
from ..model.pet import Pet, Photo
from ..log import Logger



class StatusCodes(Enum):
    SUCCESS = 0
    INSERTION_ERROR = 1
    PET_NOT_FOUND_ERROR = 2
    BROKEN_PET_ERROR = 3
    PET_ALREADY_EXISTS_ERROR = 4
    PET_DOES_NOT_EXIST_ERROR = 5
    PET_LOAD_JSON_ERROR = 6
    DISK_ERROR = 7


def set_values(obj, args):
    for key in args:
        setattr(obj, key, args[key])



class PetPersistence:
    """
    Singleton class that handles persistence
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PetPersistence.__instance == None:
            PetPersistence()
        return PetPersistence.__instance


    def __init__(self):
        self.fsm = FSManager()

        self.db_config = {'postgres': config(section='postgresql')}
        self.db = DatabaseManager(self.db_config)
        Model.set_connection_resolver(self.db)

        if PetPersistence.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PetPersistence.__instance = self
    
    def save_pet(self, pet_params: dict):
        # Create pet and save it on DB
        pet = Pet(**pet_params)
        pet.save()  #TODO Catch exceptions

        # Use newly created pet id to make the fs folder
        status = self.fsm.save_pet(pet)

        return status, pet.id 
    
    def update_pet(self, pet_params: dict):
        # Fetch pet, update its values and save it on DB
        pet = Pet.find(pet_params['id'])
        set_values(pet, pet_params)
        pet.save()  #TODO Catch exceptions

    
    def save_photo(self, pet_id: int, content: str):
        photo_id = -1
        status, path = self.fsm.save_photo(pet_id, content)

        if status == StatusCodes.SUCCESS:
            pet = Pet.find(pet_id)

            if pet is None:
                status = StatusCodes.PET_DOES_NOT_EXIST_ERROR
            else:
                photo = Photo(path=path, pet_id=pet_id)
                photo.save() #TODO Catch exceptions
                photo_id = photo.id
        
        return status, photo_id
        



data_path = config(section='persistence')['data_path']

class FSManager:
    """
    Class that handles photo persistence using pets as folders in the filesystem
    """
    def __init__(self):
        # Get parameters from .ini file
        
        self.path = data_path

        # Check if given path is dir
        assert(os.path.isdir(self.path))

        # Each folder inside the path is a dog.
        self.format = os.path.join(self.path, "%06d")

    def get_pet_folder(self, pet_id: int):
        folder = self.format % pet_id
        isdir = os.path.isdir(folder)
        return isdir, folder

    def get_pet(self, pet_id: int):
        isdir, folder = self.get_pet_folder(pet_id)
        info = os.path.join(folder, "info.json")
        status = None
        
        if os.path.isfile(info) and isdir:
            try:
                with open(info) as f:
                    pet_json = json.load(f)
                return Pet(**pet_json)
            
            except json.JSONDecodeError as e:
                Logger.error("Cant decode pet: %s" % pet_json)
                status = StatusCodes.BROKEN_PET_ERROR
            
            else:
                status = StatusCodes.SUCCESS
        else:
            status = StatusCodes.PET_NOT_FOUND_ERROR
        
        return status
    
    def save_pet(self, pet: Pet):
        isdir, newpath = self.get_pet_folder(pet.id)
        status = None

        if isdir:
            status = StatusCodes.PET_ALREADY_EXISTS_ERROR

        try:
            os.mkdir(newpath)

            with open(os.path.join(newpath, "info.json"), "w") as f:
                json.dump(pet.to_json(), f)
        
        except Exception as e:
            Logger.error("Cant jsonify pet: %s" % pet.to_json())
            status = StatusCodes.PET_LOAD_JSON_ERROR
        
        else:
            status = StatusCodes.SUCCESS
        
        return status
    
    def save_photo(self, pet_id: int, content: str):
        status = None
        photo_id = -1

        isdir, folder = self.get_pet_folder(pet_id)
        if isdir:
            try:
                imgbytes = base64.b64decode(content)

                filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f.png')
                filename = os.path.join(self.format % pet_id, filename)

                with open(filename, "wb") as f:
                    f.write(imgbytes)
                    
            except Exception as e:
                print("ERRO", e)
                status = StatusCodes.DISK_ERROR
            
            else:
                status = StatusCodes.SUCCESS
        else:
            status = StatusCodes.PET_DOES_NOT_EXIST_ERROR

        return status, photo_id




