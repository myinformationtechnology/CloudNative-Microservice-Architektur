from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from authz.util import check_request_content_type

from authz.config import Config

db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()

apiv1_bp = Blueprint("apiv1", __name__, url_prefix="/api/v1")
apiv1 = Api(apiv1_bp)

from authz import resource  # Muss an dieser Stelle stehen, nach apiv1.

def create_app():
    print("Starte")
    app = Flask(__name__)
    app.config.from_object(Config)  # Lädt die Konfiguration aus Umgebungsvariablen.
    app.before_request_funcs[None].append(
        check_request_content_type
    )  # Überprüft den Content-Type für jede Anfrage.
    db.init_app(app)  # Initialisiert das SQLAlchemy-Datenbankobjekt.
    mg.init_app(app, db)  # Initialisiert das Datenbankmanagement und das Migrate-Objekt.
    ma.init_app(app)  # Initialisiert das Marshmallow-Objekt.
    app.register_blueprint(apiv1_bp)
    return app
