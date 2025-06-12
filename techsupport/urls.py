"""
URL configuration for techsupport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import LoginView, LogoutView, RefreshView, VerifyView

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/tickets/', include('tickets.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/notifications/', include('notifications.urls')),

    path('api/v1/auth/login/', LoginView.as_view(), name='login'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/auth/jwt/refresh/', RefreshView.as_view(), name='refresh-jwt'),
    path('api/v1/auth/jwt/verify/', VerifyView.as_view(), name='verify-jwt'),
    
    # Документация drf-spectacular
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
