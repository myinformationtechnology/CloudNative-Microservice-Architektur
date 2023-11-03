from authz.authz import apiv1 as api  # bezieht sich auf apiv1 in der Datei authz
from authz.resource.apiv1.user import UserResource
from authz.resource.apiv1.auth import AuthTokenResource

# Füge die AuthTokenResource zum API hinzu
api.add_resource(
    AuthTokenResource, "/auth/tokens", methods=["GET", "POST"], endpoint="auth_tokens"
)

# Füge die UserResource zum API hinzu
api.add_resource(UserResource, "/users", methods=["GET", "POST"], endpoint="users")

# Füge die UserResource zum API hinzu, wobei <user_id> ein Platzhalter für den Benutzer ist
api.add_resource(
    UserResource,
    "/users/<user_id>",  # kann als <user_id>:string|int|uuid... festgelegt werden
    methods=["GET", "PATCH", "DELETE"],
    endpoint="user",
)

