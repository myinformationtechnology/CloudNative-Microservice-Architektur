from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import logging  # Ersetzt 'print' durch das Logging-Modul

from authz.config import Config
from authz.util import check_request_content_type

# Initialisierung der Flask-Erweiterungen
db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()

# Erstellung des Blueprints für die API
apiv1_bp = Blueprint("apiv1", __name__, url_prefix="/api/v1")
apiv1 = Api(apiv1_bp)

# Import der Ressourcen; muss nach der Initialisierung von 'apiv1' erfolgen
from authz import resource

def create_app():
    """
    Erstellt und konfiguriert die Flask-Anwendung.

    Returns:
        app: Die erstellte Flask-Anwendung.
    """
    # Verwenden des Logging-Moduls für bessere Nachrichtenverwaltung
    logging.info("Starte die Flask-Anwendung")

    app = Flask(__name__)
    app.config.from_object(Config)  # Konfiguration aus der Config-Klasse laden

    # Hinzufügen der Content-Type-Überprüfung als vorherige Anforderungsfunktion
    app.before_request_funcs.setdefault(None, []).append(check_request_content_type)

    # Initialisierung der Flask-Erweiterungen mit der App-Instanz
    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)

    # Registrierung des Blueprints bei der App
    app.register_blueprint(apiv1_bp)

    return app
