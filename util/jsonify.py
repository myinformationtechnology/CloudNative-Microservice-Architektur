from flask import current_app

# Definition der Debug-Nachrichtencodes für verschiedene Zustände und Fehler.
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
    """
    Erstellt eine JSON-Antwort mit gegebenen Daten, Status und optionalen Headern.

    Args:
        state (dict): Hauptdaten, die in der Antwort zurückgegeben werden sollen.
        metadata (dict): Zusätzliche Metadaten für die Antwort.
        status (int): HTTP-Statuscode der Antwort (Standard: 200).
        code (int): Anwendungsspezifischer Statuscode (Standard: 100).
        headers (dict): Optionale HTTP-Header für die Antwort.

    Returns:
        tuple: Ein Tupel aus Daten, Statuscode und Headern für die HTTP-Antwort.
    """
    # Kombinieren von 'state' und 'metadata' in einem einzigen Antwort-Objekt.
    data = state
    data.update(metadata)

    # Hinzufügen der Debug-Nachricht, wenn im Debug-Modus.
    if current_app.debug:
        data["MELDUNGEN"] = DEBUG_MSG_CODES[str(code)]

    # Hinzufügen des Codes zur Antwort.
    data["code"] = code

    # Rückgabe des zusammengesetzten Antwortobjekts zusammen mit Status und Headern.
    return data, status, headers

