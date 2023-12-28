from flask import request
from authz.authz import db
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import jsonify
from authz.decorator.apiv1 import auth_required

class UserController:
    def __init__(self):
        # Initialisierung der UserSchema-Instanzen für einzelne und mehrere Benutzer.
        self.user_schema = UserSchema()
        self.user_list_schema = UserSchema(many=True)

    @auth_required
    def get_user_list(self):
        # Abruf aller Benutzer aus der Datenbank und Rückgabe als JSON.
        users = User.query.all()
        return jsonify({"Users": self.user_list_schema.dump(users)})

    @auth_required
    def get_user(self, user_id):
        # Abruf eines einzelnen Benutzers anhand der Benutzer-ID.
        user = User.query.get(user_id)
        if not user:
            # Rückgabe eines Fehlers, wenn der Benutzer nicht existiert.
            return jsonify(status=404, code=103)
        return jsonify({"User": self.user_schema.dump(user)})

    def create_user(self):
        # Erfassung und Validierung der Benutzerdaten aus der Anfrage.
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            # Rückgabe eines Fehlers bei ungültigen Eingabedaten.
            return jsonify(status=400, code=105)

        # Überprüfung, ob der Benutzername bereits existiert.
        if User.query.filter_by(username=data["username"]).first():
            return jsonify(status=409, code=106)

        # Erstellung und Speicherung eines neuen Benutzers.
        new_user = User(username=data["username"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"User": self.user_schema.dump(new_user)}, status=201)

    @auth_required
    def update_user(self, user_id):
        # Aktualisierung der Benutzerdaten.
        user = User.query.get(user_id)
        if not user:
            # Rückgabe eines Fehlers, wenn der Benutzer nicht existiert.
            return jsonify(status=404, code=103)

        data = request.get_json()
        user.password = data.get("password", user.password)
        db.session.commit()
        return jsonify({"User": self.user_schema.dump(user)})

    @auth_required
    def delete_user(self, user_id):
        # Löschen eines Benutzers anhand der Benutzer-ID.
        user = User.query.get(user_id)
        if not user:
            # Rückgabe eines Fehlers, wenn der Benutzer nicht existiert.
            return jsonify(status=404, code=103)

        db.session.delete(user)
        db.session.commit()
        return jsonify(status=200)



