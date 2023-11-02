from flask import current_app

DEBUG_MSG_CODES = {
    "100": "OK",
    "101": "Nicht unterstützter Medientyp",
    "102": "Datenbankfehler",
    "103": "Ressource nicht gefunden",
    "104": "Anforderungsvalidierung fehlgeschlagen",
    "105": "Leere Felder",
    "106": "Ressourcenkonflikt",
    "107": "Nicht implementiert",
    "108": "Ressource abgelaufen",
    "109": "Ungültiger Status",
    "110": "Token-Verschlüsselungsfehler",
    "111": "Ressource nicht gefunden",
    "112": "Header nicht angegeben",
    "113": "Token-Validierungsfehler",
    "114": "Ungültige Token-Daten",
    "115": "Controller-zugelassene Regeln nicht gefunden",
    "116": "Zugriff auf Ressource verweigert",
    "117": "Rolle nicht gefunden",
}

def jsonify(state={}, metadata={}, status=200, code=100, headers={}):
    data = state
    data.update(metadata
    if current_app.debug:
        data["MELDUNGEN"] = DEBUG_MSG_CODES[str(code)]
    data["code"] = code
    return data, status, headers

