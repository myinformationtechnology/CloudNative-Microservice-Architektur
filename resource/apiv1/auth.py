from flask_restful import Resource
from authz.controller.apiv1 import AuthTokenController

class AuthTokenResource(Resource):
    def get(self):
        """
        GET /auth/tokens --> Benutzer JWT-Token überprüfen
        """
        return AuthTokenController.verify_jwt_token()  # Benutzer JWT-Token überprüfen

    def post(self):
        """
        POST /auth/tokens --> Benutzer JWT-Token erstellen
        """
        return AuthTokenController.create_jwt_token()  # Benutzer JWT-Token erstellen

