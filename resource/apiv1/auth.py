from flask_restful import Resource
from authz.controller.apiv1 import AuthTokenController
from flask import request, jsonify

class AuthTokenResource(Resource):
    def get(self):
        """
        GET /auth/tokens
        Überprüft das JWT-Token des Benutzers und gibt den Validierungsstatus zurück.
        Extrahiert das Token aus dem Authorization-Header und validiert es.
        Gibt bei erfolgreicher Validierung eine positive Antwort zurück,
        sonst eine Fehlermeldung.
        """
        # Extrahiert das Token aus dem Authorization-Header
        token = request.headers.get('Authorization')

        # Überprüft, ob ein Token vorhanden ist
        if not token:
            return jsonify({'message': 'Authorization token is missing'}), 401

        # Validiert das Token
        valid, response = AuthTokenController.verify_jwt_token(token)

        # Gibt entsprechende Antwort basierend auf der Validierung zurück
        if valid:
            return jsonify(response), 200
        else:
            return jsonify(response), 401

    def post(self):
        """
        POST /auth/tokens
        Erstellt ein JWT-Token für einen authentifizierten Benutzer.
        Nimmt Benutzerdaten aus dem Request-Body und generiert ein JWT-Token.
        Gibt das Token bei erfolgreicher Erstellung zurück,
        sonst eine Fehlermeldung.
        """
        # Extrahiert Benutzerdaten aus dem Request-Body
        user_data = request.json

        # Überprüft, ob Benutzerdaten vorhanden sind
        if not user_data:
            return jsonify({'message': 'No data provided'}), 400

        # Erstellt ein JWT-Token mit den Benutzerdaten
        token, response = AuthTokenController.create_jwt_token(user_data)

        # Gibt das erstellte Token oder eine Fehlermeldung zurück
        if token:
            return jsonify({'token': token}), 201
        else:
            return jsonify(response), 400



