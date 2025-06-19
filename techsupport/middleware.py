from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from jwt import InvalidTokenError


@database_sync_to_async
def get_user(validated_token):
    try:
        return JWTAuthentication().get_user(validated_token)
    except Exception:
        return AnonymousUser()

class JWTWebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            scope["user"] = await get_user(validated_token)
        except InvalidTokenError:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
