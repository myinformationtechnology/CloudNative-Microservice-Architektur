
    # Importieren der notwendigen Module aus dem Flask-Framework und projektinternen Hilfsfunktionen
from flask import Flask, request
from authz.util import jsonify
from authz.config import Config

def check_request_content_type():
    """
    Funktion zur Überprüfung des Content-Types der eingehenden Anfragen.
    Stellt sicher, dass alle Anfragen den Content-Type 'application/json' haben.
    
    Returns:
        - JSON-Antwort mit Statuscode 415 (Unsupported Media Type), 
          wenn der Content-Type nicht 'application/json' ist.
        - None, wenn der Content-Type korrekt ist, um die weitere Verarbeitung zu ermöglichen.
    """
    # Überprüfung des Content-Types der Anfrage
    if request.content_type != "application/json":
        # Rückgabe einer JSON-Antwort mit Statuscode 415, wenn der Content-Type nicht korrekt ist
        return jsonify(status=415, code=101)
    # Keine Aktion erforderlich, wenn der Content-Type korrekt ist
    return None

# Hier können weitere Funktionen oder Konfigurationen für die Flask-Anwendung hinzugefügt werden

