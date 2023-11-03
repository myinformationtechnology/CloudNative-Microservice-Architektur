from functools import wraps
from flask import request
from jwt import decode

from authz.model import User
from authz.config import Config
from authz.util import jsonify, now
from authz.rule.apiv1 import ControllerAccessRules


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "X-Auth-Token" not in request.headers:
            return jsonify(status=403, code=112)  # X-Auth-Token wurde nicht angegeben
        try:
            user_jwt_data = decode(
                request.headers["X-Auth-Token"],
                Config.SECRET_KEY,
                Config.JWT_TOKEN_DEFAULT_ALGORITHM,
            )
        except:
            return jsonify(status=403, code=113)  # Ungültiges JWT-Token
        try:
            user = User.query.get(user_jwt_data["user"]["id"])  # Benutzer auswählen
        except:
            return jsonify(status=500, code=102)  # Datenbankfehler
        if user is None:
            return jsonify(status=403, code=103)  # Benutzer nicht gefunden
        if user.role != user_jwt_data["user"]["role"]:
            return jsonify(status=403, code=114)
        if user.expires_at < now():
            return jsonify(status=403, code=108)  # Benutzer ist abgelaufen
        if user.status != 3:
            return jsonify(status=403, code=109)  # Benutzer hat den gewünschten Status nicht
        try:
            # Ermitteln der Rollen für den angegebenen Controller
            allowed_roles = ControllerAccessRules.get_controller_allowed_rules(
                f.__name__
            )
        except:
            return jsonify(status=500, code=115)  # Zugelassene Regel für den Controller wurde nicht gefunden
        if user.role in allowed_roles:
            return f(*args, **kwargs)  # Aufruf der Originalfunktion
        elif user.role == "member" and "member:user_id" in allowed_roles:
            if user.id == args[f.__code__.co_varnames.index("user_id")]:
                return f(*args, **kwargs)  # Aufruf der Originalfunktion
            else:
                return jsonify(status=403, code=116)
        else:
            return jsonify(status=403, code=117)

    return wrapper

