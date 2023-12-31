from os import environ

class Config:
    # Globale Konfiguration
    # Umgebungsvariablen werden verwendet, um die Konfiguration flexibel zu gestalten
    ENV = environ.get("TOYBOX_AUTHZ_ENV", "production")  # Standardmäßig 'production'
    DEBUG = environ.get("TOYBOX_AUTHZ_DEBUG", "0") == "1"  # Aktiviert Debug-Modus wenn '1'
    TESTING = environ.get("TOYBOX_AUTHZ_TESTING", "0") == "1"  # Aktiviert Test-Modus wenn '1'

    # Sicherheitsschlüssel für die Anwendung
    SECRET_KEY = environ.get("TOYBOX_AUTHZ_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("Kein SECRET_KEY für die Toybox-Authz-Konfiguration festgelegt")

    JSONIFY_PRETTYPRINT_REGULAR = True  # Schöne Formatierung von JSON-Antworten
    TIMEZONE = environ.get("TOYBOX_AUTHZ_TIMEZONE", "UTC")  # Standardzeitzone ist UTC

    # Datenbankkonfiguration
    SQLALCHEMY_DATABASE_URI = environ.get("TOYBOX_AUTHZ_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("Kein DATABASE_URI für die Toybox-Authz-Konfiguration festgelegt")
    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG  # Trackt Modifikationen im Debug-Modus

    # Benutzerkonfiguration
    USER_DEFAULT_EXPIRES_TIME = int(environ.get("TOYBOX_AUTHZ_USER_DEFAULT_EXPIRES_TIME", "365"))  # Standard-Ablaufzeit für Benutzer
    USER_DEFAULT_ROLE = environ.get("TOYBOX_AUTHZ_USER_DEFAULT_ROLE", "Mitglied")  # Standardrolle für neue Benutzer
    USER_DEFAULT_STATUS = int(environ.get("TOYBOX_AUTHZ_USER_DEFAULT_STATUS", "0"))  # Standardstatus für neue Benutzer

    # Authentifizierungskonfiguration
    JWT_TOKEN_DEFAULT_EXPIRY_TIME = int(environ.get("TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_EXPIRY_TIME", "86400"))  # Standard-Ablaufzeit für JWT-Tokens
    JWT_TOKEN_DEFAULT_ALGORITHM = environ.get("TOYBOX_AUTHZ_JWT_TOKEN_DEFAULT_ALGORITHM", "HS512")  # Standard-Algorithmus für JWT-Tokens
