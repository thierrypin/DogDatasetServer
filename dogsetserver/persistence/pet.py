# -*- coding: utf-8 -*-

import os
import json
import base64
import datetime

from enum import Enum

import psycopg2

from ..util.config import config
from ..model.pet import Pet
from ..log import Logger

class StatusCodes(Enum):
    SUCCESS = 0
    INSERTION_ERROR = 1
    PET_NOT_FOUND_ERROR = 2
    BROKEN_PET_ERROR = 3
    PET_ALREADY_EXISTS_ERROR = 4
    PET_LOAD_JSON_ERROR = 5

class PGConnection:
    def __init__(self):
        self.connector = None
        self.cursor = None
        self.params = config(section='postgresql')

        self.insert_pet_query = "insert into pet (name, breed, type, sex) values ('%s', '%s', '%s', '%s') returning id"
        self.insert_photo_query = "insert into photo (pet_id, path) values (%d, '%s') returning id"
    
    def __enter__(self):
        self.connector = psycopg2.connect(**self.params)
        self.cursor = self.connector.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.connector.commit()
        else:
            self.connector.rollback()
        self.cursor.close()
        self.connector.close()

    def save_pet(self, pet: Pet):
        query = self.insert_pet_query % (pet.name, pet.breed, pet.petType, pet.sex)
        status = None
        res = -1
        
        try:
            self.cursor.execute(query)
            res = self.cursor.fetchone()[0]
            
        except psycopg2.Error as e:
            Logger.error(e)
            status = StatusCodes.INSERTION_ERROR
        
        else:
            status = StatusCodes.SUCCESS

        finally:
            return status, res
    
    def save_photo(self, pet: Pet, path: str):
        status = None
        res = -1

        if pet.id is not None:
            query = self.insert_photo_query % (pet.id, path)

            try:
                self.cursor.execute(query)
                res = self.cursor.fetchone()[0]
            
            except psycopg2.Error as e:
                Logger.error(e)
                status = StatusCodes.INSERTION_ERROR
            
            else:
                status = StatusCodes.SUCCESS
        else:
            status = StatusCodes.PET_NOT_FOUND_ERROR

        return res





data_path = config(section='persistence')['data_path']

class DirDataset:
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

    def get_pet_folder(self, id: int):
        folder = self.format % id
        isdir = os.path.isdir(folder)
        return isdir, folder

    def get_pet(self, id: int):
        isdir, folder = get_pet_folder(id)
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
    
    def new_pet(self, pet: Pet):
        isdir, newpath = get_pet_folder(id)
        status = None

        if isdir:
            status = StatusCodes.PET_ALREADY_EXISTS_ERROR

        try:
            os.mkdir(newpath)

            with open(os.path.join(newpath, "info.json"), "wb") as f:
                json.dump(pet.to_json())
        
        except json.TypeError as e:
            Logger.error("Cant jsonify pet: %s" % pet.to_json())
            status = StatusCodes.PET_LOAD_JSON_ERROR
        
        else:
            status = StatusCodes.SUCCESS
        
        return status
    
    def new_photo(self, pet: Pet, content: str):
        isdir, folder = get_pet_folder(id)
        imgbytes = base64.b64decode(content)

        filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f.png')

        with open(filename, "wb") as f:
            f.write(imgbytes)

        return filename




