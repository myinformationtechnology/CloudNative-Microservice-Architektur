
    class ControllerAccessRules:
    # Dieses private Dictionary definiert die Zugriffsregeln für verschiedene Funktionen im System.
    # Die Schlüssel sind die Namen der Funktionen und die Werte sind Listen von Rollen, 
    # die Zugriff auf diese Funktionen haben.
    __Controller_allowed_rules = {
        "get_user_list": ["admin", "service"],
        "get_user": ["admin", "service", "member:user_id"],
        "create_user": ["all"],
        "update_user": ["admin", "member:user_id"],
        "delete_user": ["admin"],
    }

    # Diese Methode gibt die erlaubten Rollen für eine gegebene Funktion zurück.
    # Sie nimmt den Namen der Funktion als Parameter und gibt die entsprechende Liste von erlaubten Rollen zurück.
    def get_controller_allowed_rules(f):
        return ControllerAccessRules.__Controller_allowed_rules[f]

