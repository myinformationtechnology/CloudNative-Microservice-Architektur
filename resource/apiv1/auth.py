from flask_restful import Resource
from authz.controller.apiv1 import AuthTokenController
from flask import request, jsonify

class AuthTokenResource(Resource):
    def get(self):
        """
        GET /auth/tokens
        Überprüft das JWT-Token des Benutzers und gibt den Validierungsstatus zurück.
        """
        token = request.headers.get('Authorization')
        valid, response = AuthTokenController.verify_jwt_token(token)
        if valid:
            return jsonify(response), 200
        else:
            return jsonify(response), 401

    def post(self):
        """
        POST /auth/tokens
        Erstellt ein JWT-Token für einen authentifizierten Benutzer.
        """
        user_data = request.json
        token, response = AuthTokenController.create_jwt_token(user_data)
        if token:
            return jsonify({'token': token}), 201
        else:
            return jsonify(response), 400

