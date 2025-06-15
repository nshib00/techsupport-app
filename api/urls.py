from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.views import LoginView, LogoutView, RefreshView, VerifyView


urlpatterns = [
    # Документация drf-spectacular
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Приложения
    path('tickets/', include('tickets.urls')),
    path('users/', include('users.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', include('custom_admin.urls')),

    # Аутентификация
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/jwt/refresh/', RefreshView.as_view(), name='refresh-jwt'),
    path('auth/jwt/verify/', VerifyView.as_view(), name='verify-jwt'),
]