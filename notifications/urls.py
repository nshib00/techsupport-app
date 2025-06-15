from django.urls import path
from notifications.views import NotificationListView, NotificationUpdateView


urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/mark-as-read/', NotificationUpdateView.as_view(), name='mark-notification-as-read'),
]