from flask_restful import Resource
from authz.controller.apiv1 import UserController

class UserResource(Resource):
    def get(self, user_id=None):
        """
        GET /users --> Liste der Benutzer abrufen.
        GET /users/<user_id> --> Benutzerinformationen abrufen.
        """
        if user_id is None:
            return UserController.get_user_list()  # Liste der Benutzer abrufen.
        else:
            return UserController.get_user(user_id)  # Benutzer abrufen

    def post(self):
        """
        POST /users --> Benutzer erstellen.
        POST /users/<user_id> --> Nicht erlaubt.
        """
        return UserController.create_user()  # Benutzer erstellen

    def patch(self, user_id):
        """
        PATCH /users --> Nicht erlaubt.
        PATCH /users/<user_id> --> Benutzer aktualisieren.
        """
        return UserController.update_user(user_id)  # Benutzer aktualisieren

    def delete(self, user_id):
        """
        DELETE /users --> Nicht erlaubt.
        DELETE /users/<user_id> --> Benutzer löschen.
        """
        return UserController.delete_user(user_id)  # Benutzer löschen

