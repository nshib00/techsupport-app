import logging
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from rest_framework_simplejwt.exceptions import InvalidToken 
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import PermissionDenied
import traceback
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError, NotAuthenticated, AuthenticationFailed, NotFound

from techsupport.exceptions import ConflictAPIException


logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user(validated_token):
    return JWTAuthentication().get_user(validated_token)


class JWTWebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if not token:
            logger.warning("WebSocket connection denied: no token provided.")
            await self.__reject_connection(send, code=4001)
            return

        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            user = await get_user(validated_token)

            if isinstance(user, AnonymousUser):
                logger.warning("WebSocket connection denied: user resolution failed.")
                await self.__reject_connection(send, code=4003)
                return

            scope["user"] = user

        except (InvalidToken, TokenError, PermissionDenied) as e:
            logger.warning(f"WebSocket connection denied: auth failed: {e.__class__.__name__}: {e}")
            await self.__reject_connection(send, code=4002)
            return

        except Exception as e:
            logger.error(f"Unexpected error during WebSocket auth: {e.__class__.__name__}: {e}")
            await self.__reject_connection(send, code=4500)
            return

        return await super().__call__(scope, receive, send)

    async def __reject_connection(self, send, code=4000):
        await send({
            "type": "websocket.close",
            "code": code
        })


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)

        except ValidationError as e:
            logger.warning("Validation error: %s", e)
            return JsonResponse({'detail': e.detail}, status=400)

        except (NotAuthenticated, AuthenticationFailed) as e:
            logger.warning("Authentication error: %s", e)
            return JsonResponse({'detail': str(e)}, status=401)

        except PermissionDenied as e:
            logger.warning("Permission denied: %s", e)
            return JsonResponse({'detail': str(e)}, status=403)

        except (Http404, NotFound) as e:
            logger.warning("Not found: %s", e)
            return JsonResponse({'detail': 'Страница не найдена'}, status=404)
        
        except ConflictAPIException as e:
            logger.warning("Data conflict error: %s", e)
            return JsonResponse({'detail': e.detail}, status=409)

        except Exception as e:
            logger.error("Unexpected error: %s\n%s", str(e), traceback.format_exc()) # логируем полную трассировку
            return JsonResponse(
                {'detail': 'Произошла внутренняя ошибка сервера'},
                status=500
            )
