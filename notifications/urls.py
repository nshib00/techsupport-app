from django.urls import path
from notifications.consumers.support import SupportNotificationConsumer
from notifications.consumers.user import UserNotificationConsumer
from notifications.views import NotificationListView, NotificationUpdateView


urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/mark-as-read/', NotificationUpdateView.as_view(), name='mark-notification-as-read'),
]

websocket_urlpatterns = [
    path("ws/users/notifications/", UserNotificationConsumer.as_asgi()),
    path("ws/support/notifications/", SupportNotificationConsumer.as_asgi()),
]