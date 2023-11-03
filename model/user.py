from authz.authz import db
from authz.util import uuidgen, now, user_expires_at
from authz.config import Config


class Benutzer(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=uuidgen)
    benutzername = db.Column(db.String(128), unique=True, index=True)
    passwort = db.Column(db.String(256), nullable=False)
    rolle = db.Column(
        db.String(32), index=True, nullable=False, default=Config.USER_DEFAULT_ROLE
    )
    erstellt_am = db.Column(db.DateTime, nullable=False, default=now)
    abläuft_am = db.Column(db.DateTime, nullable=False, default=user_expires_at)
    letzter_login_am = db.Column(db.DateTime, default=None)
    letzter_aktiv_am = db.Column(db.DateTime, default=None)
    letzte_änderung_am = db.Column(db.DateTime, default=None)
    fehlgeschlagen_am = db.Column(db.DateTime, default=None)
    fehlgeschlagene_auth_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=Config.USER_DEFAULT_STATUS)

    def __repr__(self):
        return f"<Benutzer Benutzername={self.benutzername}, Rolle={self.rolle}, Erstellt am={self.erstellt_am}"

