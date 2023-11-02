from authz.authz import db
from authz.decorator.apiv1 import auth_required
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import jsonify, now
from flask import request

class UserController:
    @auth_required
    def get_user_list():
        try:
            users = User.query.all()  # Abfrage von Benutzern aus der Datenbank
        except:
            return jsonify(status=500, code=102)
        users_schema = UserSchema(many=True)  # Erstellung eines Serialisierungsobjekts für die Liste der Benutzer
        return jsonify({"Users": users_schema.dump(users)})  # Rückgabe der Liste der Benutzer

    @auth_required
    def get_user(user_id):
        try:
            user = User.query.get(user_id)  # Abrufen eines Benutzers
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler
        if user is None:
            return jsonify(status=404, code=103)  # Benutzer wurde nicht gefunden
        user_schema = UserSchema()
        return jsonify({"User": user_schema.dump(user)})  # Rückgabe eines Benutzers

    def create_user():
        user_schema = UserSchema(only=["username", "password"])
        try:
            data = user_schema.load(request.get_json())  # Validierung der Benutzerdaten
        except:
            return jsonify(status=400, code=104)  # Validierung fehlgeschlagen
        if not data["username"] or nicht data["password"]:  # Überprüfung auf nicht leere Felder
            return jsonify(status=400, code=105)
        try:
            user = User.query.filter_by(username=data["username"]).first()  # Überprüfen auf Benutzernamenduplikate
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler
        if user is not None:
            return jsonify(status=409, code=106)  # Ressourcenkonflikt
        user = User(username=data["username"], password=data["password"])
        db.session.add(user)  # Auswahl des Benutzers zur Einfügung in die Datenbank
        try:
            db.session.commit()  # Einfügen des Benutzers in die Datenbank
        except:
            db.session.rollback()  # Rollback im Falle eines Datenbankfehlers
            return jsonify(status=500, code=102)  # Datenbankfehler
        user_schema = UserSchema()
        return jsonify({"User": user_schema.dump(user)}, status=201)  # Rückgabe eines neuen Benutzers

    @auth_required
    def update_user(user_id):
        user_schema = UserSchema(only=["password"])
        try:
            data = user_schema.load(request.get_json())  # Validierung der Benutzerdaten
        except:
            return jsonify(status=400, code=104)  # Validierung fehlgeschlagen
        if not data["password"]:  # Überprüfung auf nicht leeres Feld
            return jsonify(status=400, code=105)
        try:
            user = User.query.get(user_id)  # Auswahl des Benutzers
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler
        if user is None:
            return jsonify(status=404, code=103)  # Benutzer wurde nicht gefunden
        user.password = data["password"]
        user.last_change_at = now()
        db.session.add(user)
        try:
            db.session.commit()  # Aktualisieren des Benutzerpassworts in der Datenbank
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)
        user_schema = UserSchema()
        return jsonify({"user": user_schema.dump(user)})

    @auth_required
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)  # Auswahl des Benutzers
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler
        if user is None:
            return jsonify(status=404, code=103)  # Benutzer wurde nicht gefunden
        db.session.delete(user)
        try:
            db.session.commit()  # Aktualisieren des Benutzerpassworts in der Datenbank
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)
        return jsonify()

