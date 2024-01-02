from functools import wraps
from flask import request
from jwt import decode, DecodeError, ExpiredSignatureError  # Verbesserter Import für spezifische JWT-Ausnahmen

from authz.model import User
from authz.config import Config
from authz.util import jsonify, now
from authz.rule.apiv1 import ControllerAccessRules

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Überprüfen, ob X-Auth-Token im Header vorhanden ist
        if "X-Auth-Token" not in request.headers:
            return jsonify(status=403, code=112)  # Fehlercode, wenn X-Auth-Token fehlt

        try:
            # JWT-Token dekodieren
            user_jwt_data = decode(
                request.headers["X-Auth-Token"],
                Config.SECRET_KEY,
                Config.JWT_TOKEN_DEFAULT_ALGORITHM,
            )
        except DecodeError:
            return jsonify(status=403, code=113)  # Fehlercode für ungültiges JWT-Token
        except ExpiredSignatureError:
            return jsonify(status=403, code=111)  # Fehlercode für abgelaufenes JWT-Token (neu hinzugefügt)

        try:
            # Benutzer anhand der ID aus dem Token in der Datenbank suchen
            user = User.query.get(user_jwt_data["user"]["id"])
        except Exception as e:  # Spezifische Ausnahme fangen und loggen
            print(f"Datenbankfehler: {e}")  # Logging hinzufügen
            return jsonify(status=500, code=102)  # Fehlercode bei Datenbankfehler

        if user is None:
            return jsonify(status=403, code=103)  # Fehlercode, wenn Benutzer nicht gefunden wird

        # Überprüfen der Benutzerrolle und weiterer Eigenschaften
        if user.role != user_jwt_data["user"]["role"] or user.expires_at < now() or user.status != 3:
            return jsonify(status=403, code=114)  # Allgemeiner Fehlercode für ungültige Benutzereigenschaften

        try:
            # Ermitteln der erlaubten Rollen für den Controller
            allowed_roles = ControllerAccessRules.get_controller_allowed_rules(f.__name__)
        except Exception as e:
            print(f"Fehler bei der Ermittlung der Zugriffsregeln: {e}")  # Logging hinzufügen
            return jsonify(status=500, code=115)  # Fehlercode, wenn keine Zugriffsregel gefunden wird

        # Überprüfen, ob die Benutzerrolle Zugriff hat
        if user.role in allowed_roles:
            return f(*args, **kwargs)  # Aufruf der Originalfunktion, wenn Benutzer autorisiert ist
        elif user.role == "member" and "member:user_id" in allowed_roles:
            # Spezielle Behandlung für Mitglieder mit der Rolle 'member:user_id'
            if user.id == args[f.__code__.co_varnames.index("user_id")]:
                return f(*args, **kwargs)  # Aufruf der Originalfunktion, wenn Benutzer-ID übereinstimmt
            else:
                return jsonify(status=403, code=116)  # Fehlercode, wenn Benutzer-ID nicht übereinstimmt
        else:
            return jsonify(status=403, code=117)  # Fehlercode, wenn Benutzerrolle keinen Zugriff hat

    return wrapper
