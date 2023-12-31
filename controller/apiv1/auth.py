from authz.util import jsonify, now
from authz.authz import db
from authz.schema.apiv1 import UserSchema
from authz.model import User
from flask import request
from jwt import encode
from authz.config import Config
from time import time
from werkzeug.security import check_password_hash  # Import für sichere Passwortüberprüfung

class AuthTokenController:
    @staticmethod
    def verify_jwt_token():
        # Funktion zur Überprüfung des JWT-Tokens
        # Momentan ist die Implementierung noch ausstehend.
        # Rückgabe eines HTTP 501 Not Implemented Statuscodes.
        return jsonify(status=501, code=107)

    @staticmethod
    def create_jwt_token():
        # Funktion zur Erstellung eines neuen JWT-Tokens
        
        # Erstellung eines UserSchema-Objekts für die Validierung der Benutzerdaten.
        user_schema = UserSchema(only=["username", "password"])
        try:
            # Versuch, die Benutzerdaten aus der Anfrage zu laden und zu validieren.
            data = user_schema.load(request.get_json())
        except:
            # Rückgabe bei Validierungsfehlern.
            return jsonify(status=400, code=104)

        # Überprüfung, ob Benutzername und Passwort vorhanden sind.
        if not data["username"] or not data["password"]:
            return jsonify(status=400, code=105)  # Benutzername oder Passwort fehlen

        try:
            # Suche des Benutzers in der Datenbank anhand des Benutzernamens.
            user = User.query.filter_by(username=data["username"]).first()
        except:
            # Rückgabe bei Fehlern während der Datenbankabfrage.
            return jsonify(status=500, code=102)  # Datenbankfehler

        # Überprüfung, ob Benutzer existiert und das Passwort korrekt ist.
        if user is None or not check_password_hash(user.password, data["password"]):
            # Protokollierung des fehlgeschlagenen Authentifizierungsversuchs.
            user.failed_auth_at = now()
            user.failed_auth_count += 1
            db.session.commit()
            return jsonify(status=403, code=111)  # Falscher Benutzer und Passwort

        # Überprüfung, ob das Konto des Benutzers abgelaufen ist.
        if user.expires_at < now():
            return jsonify(status=403, code=108)  # Benutzerkonto abgelaufen

        # Überprüfung, ob der Benutzer den erforderlichen Status hat.
        if user.status != 3:
            return jsonify(status=403, code=109)  # Benutzer hat nicht den richtigen Status

        # Aktuelle Zeit für die Token-Erstellung.
        current_time = time()
        try:
            # JWT-Token mit Benutzerinformationen erstellen.
            user_jwt_token = encode(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role,
                        "expires_at": user.expires_at.isoformat(),
                    },
                    "sub": user.id,
                    "nbf": current_time,
                    "exp": current_time + Config.USER_DEFAULT_EXPIRES_TIME,
                },
                Config.SECRET_KEY,
                Config.JWT_TOKEN_DEFAULT_ALGORITHM,
            ).decode("utf8")
        except Exception as e:
            # Fehlerbehandlung bei der Token-Erstellung.
            print(e)
            return jsonify(status=500, code=110)  # Fehler bei der Token-Erstellung

        # Aktualisierung des letzten Login-Datums des Benutzers.
        user.last_login_at = now()
        try:
            # Speichern der Änderungen in der Datenbank.
            db.session.commit()
        except:
            # Rückgängigmachen der Änderungen bei einem Fehler.
            db.session.rollback()
            return jsonify(status=500, code=102)  # Datenbankfehler

        # Erneutes Serialisieren des Benutzerschemas und Rückgabe des Ergebnisses zusammen mit dem Token.
        user_schema = UserSchema()
        return jsonify(
            {"user": user_schema.dump(user)},
            status=201,
            headers={"X-Subject-Token": user_jwt_token},
        )
