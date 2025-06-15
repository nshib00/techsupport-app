from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from users.serializers import LogoutSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    post=extend_schema(
        summary="Выход и добавление токена в чёрный список (blacklist)",
    )
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.get_or_create(token=outstanding_token)

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Token not found in outstanding tokens."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    @extend_schema(
        summary="Вход по email и паролю",
        description="Возвращает access и refresh токены, если аутентификация выполнена успешно.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @extend_schema(
        summary="Обновление access токена",
        description="Принимает refresh токен и возвращает новый access токен.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    


class VerifyView(TokenObtainPairView):
    serializer_class = TokenVerifySerializer

    @extend_schema(
        summary="Проверка валидности access токена",
        description="Позволяет проверить, действителен ли access токен.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создание нового пользователя по email, имени и паролю.",
        responses={201: None}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение информации о текущем пользователе",
        description="Возвращает информацию о текущем авторизованном пользователе.",
        responses={200: None}
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @extend_schema(
        summary="Запрос на сброс пароля",
        description="Отправляет письмо на email с ссылкой для восстановления пароля.",
        responses={204: None}
    )
    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)

    @extend_schema(
        summary="Подтверждение сброса пароля",
        description="Завершает процесс восстановления пароля с помощью uid и token.",
        responses={204: None}
        # параметры: uid, token, new_password
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        return super().reset_password_confirm(request, *args, **kwargs)

    

