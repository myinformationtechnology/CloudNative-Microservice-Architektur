
```python
class Config:
    ######################### Globale Konfiguration #########################
    ENV = environ.get("TOYBOX_AYTHZ_ENV", "production")
    DEBUG = bool(int(environ.get("TOYBOX_AYTHZ_DEBUG", "0")))
    TESTING = bool(int(environ.get("TOYBOX_AYTHZ_TESTING", "0")))
    # Mindestens 256 Zeichen und komplex für die Produktion
    SECRET_KEY = environ.get("TOYBOX_AUTHZ_SECRET_KEY", "STARKES_GEHEIMES_SCHLÜSSELWORT")
    JSONIFY_PRETTYPRINT_REGULAR = True
    TIMEZONE = environ.get("TOYBOY_AUTHZ_TIMEZONE")

    ######################### Datenbankkonfiguration #########################
    SQLALCHEMY_DATABASE_URI = environ.get("TOYBOY_AUTHZ_DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG

    ########################### Benutzerkonfiguration ###########################
    USER_DEFAULT_EXPIRES_TIME = int(
        environ.get("TOYBOX_AUTHZ_USER_DEFAULT_EXPIRES_TIME", "365")
    )
    USER_DEFAULT_ROLE = environ.get("TOYBOX_AUTHZ_USER_DEFAULT_ROLE", "Mitglied")
    USER_DEFAULT_STATUS = int(environ.get("TOYBOX_AUTHZ_USER_DEFAULT_STATUS", "0"))

    ####################### Authentifizierungskonfiguration ######################
    JWT_TOKEN_DEFAULT_EXPIRY_TIME = int(
        environ.get("TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_EXPIRY_TIME", "86400")
    )
    JWT_TOKEN_DEFAULT_ALGORITHM = environ.get(
        "TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_ALGORITHM", "HS512"
    )
```
