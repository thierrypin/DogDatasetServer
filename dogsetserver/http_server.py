# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, jsonify, request, make_response, url_for

from .model.pet import Pet
from .persis.tense import PetPersistence


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

        persistence = PetPersistence.getInstance()
        status, pet_id = persistence.save_pet(pet_params)

        out = {"status": status.value, "id": pet_id}
        return json.dumps(out)

    @app.route('/newphoto/<int:pet_id>', methods=['POST'])
    def newphoto(pet_id: int):
        # Must have json
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        # Json should have a pet id and a photo
        params = json.loads(request.get_json())
        content = params['photo']

        persistence = PetPersistence.getInstance()
        status, photo_id = persistence.save_photo(pet_id, content)

        out = {"status": status.value, "photo_id": photo_id}
        return json.dumps(out)

    app.run()
