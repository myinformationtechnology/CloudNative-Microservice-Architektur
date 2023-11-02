from authz.util import jsonify, now
from authz.authz import db
from authz.schema.apiv1 import UserSchema
from authz.model import User
from flask import request
from jwt import encode
from authz.config import Config
from datetime import datetime
from time import time

class AuthTokenController:
    @staticmethod
    def verify_jwt_token():
        # Funktion zur Überprüfung des JWT-Tokens
        return jsonify(status=501, code=107)

    @staticmethod
    def create_jwt_token():
        # Funktion zur Erstellung eines neuen JWT-Tokens

        # Erstellen eines UserSchema-Objekts mit den gewünschten Feldern
        user_schema = UserSchema(only=["username", "password"])
        try:
            # Validierung der Benutzerdaten aus der Anfrage
            data = user_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=104)  # Validierung fehlgeschlagen

        # Überprüfen, ob Benutzername und Passwort nicht leer sind
        if not data["username"] or not data["password"]:
            return jsonify(status=400, code=105)

        try:
            # Suchen des Benutzers in der Datenbank anhand des Benutzernamens
            user = User.query.filter_by(username=data["username"]).first()
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler

        if user is None:
            return jsonify(status=403, code=103)  # Benutzer nicht gefunden (Zugriff verweigert)

        if user.password == data["password"]:
            if user.expires_at < now():
                return jsonify(status=403, code=108)  # Benutzer ist abgelaufen

            if user.status != 3:
                return jsonify(status=403, code=109)  # Benutzer hat nicht den gewünschten Status

            current_datetime = now()
            current_time = time()

            try:
                # Erstellen eines neuen JWT-Tokens mit den Benutzerinformationen
                user_jwt_token = encode(
                    {
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "role": user.role,
                            "expires_at": datetime.isoformat(user.expires_at),
                        },
                        "sub": user.id,
                        "nbf": current_time,
                        "exp": current_time + Config.USER_DEFAULT_EXPIRES_TIME,
                    },
                    Config.SECRET_KEY,
                    Config.JWT_TOKEN_DEFAULT_ALGORITHM,
                ).encode("utf8")
            except Exception as e:
                print(e)
                return jsonify(status=500, code=110)  # Fehler bei der Token-Erstellung

            # Aktualisieren des letzten Login-Datums des Benutzers
            user.last_login_at = current_datetime

            try:
                db.session.commit()  # Datenbankaktualisierung
            except:
                db.session.rollback()  # Änderungen rückgängig machen
                return jsonify(status=500, code=102)  # Datenbankfehler

            # Erneutes Serialisieren des Benutzerschemas und Rückgabe des Ergebnisses
            user_schema = UserSchema()
            return jsonify(
                {"user": user_schema.dump(user)},
                status=201,
                headers={"X-Subject-Token": user_jwt_token},
            )

        else:
            user.failed_auth_at = now()
            user.failed_auth_count = +1

            try:
                db.session.commit()  # Datenbankaktualisierung
            except:
                db.session.rollback()  # Änderungen rückgängig machen
                return jsonify(status=500, code=102)  # Datenbankfehler

            return jsonify(status=403, code=111)  # Falscher Benutzer und Passwort

