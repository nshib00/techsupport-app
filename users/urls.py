from django.urls import path
from .views import CustomUserViewSet


urlpatterns = [
    path('register/', CustomUserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('me/', CustomUserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('reset-password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    path('reset-password-confirm/', CustomUserViewSet.as_view({'post': 'reset_password_confirm'}), name='reset-password-confirm'),
    
]

