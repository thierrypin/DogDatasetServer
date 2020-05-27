# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, jsonify, request, make_response, url_for

from .model.pet import Pet
from .persistence.pet import PGConnection, DirDataset

def start_server():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello World!'


    @app.route('/newpet', methods=['POST'])
    def newpet():
        # Must have json
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        # Parse json and build Pet object
        pet_params = json.loads(request.get_json())
        pet = Pet(**pet_params)
        print(pet, pet.name)

        # Save pet to database
        with PGConnection() as conn:
            status, id = conn.save_pet(pet)
        
        # Save pet into filesystem
        dds = DirDataset()
        dds.new_pet(pet)

        # Return status and id
        out = {"status": status, "id": id}
        return json.dumps(out)

    @app.route('/newphotos/<int:pet_id>', methods=['POST'])
    def newphotos(pet_id: int):
        # Must have json
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        # Json should have a pet id and a photo
        params = json.loads(request.get_json())
        pet_id = params['pet_id']
        photo = params['photo']

        # TODO save photos locally
        url = "test"

        with PGConnection() as conn:
            status, id = conn.save_photo(pet_id, url)

        out = {"status": status, "id": id}
        return json.dumps(out)

    app.run()
