from django.urls import include, path
from custom_admin.views.admin.ticket_history import TicketHistoryView
from custom_admin.views.support.tickets import TicketAssignView, TicketListRetrieveView, TicketUpdateStatusView
from custom_admin.views.admin.ticket_categories import TicketCategoryViewSet
from custom_admin.views.admin.users import UserListView, UserUpdateRoleView
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('categories', TicketCategoryViewSet, basename='ticket-category') 

admin_urlpatterns = [
    # Пользователи
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/role/', UserUpdateRoleView.as_view(), name='change-user-role'),

    # История изменения тикетов
    path('tickets/history/', TicketHistoryView.as_view(), name='ticket-history'),
]
admin_urlpatterns += router.urls # Категории тикетов

support_urlpatterns = [
    # Тикеты
    path('tickets/', TicketListRetrieveView.as_view({'get': 'list'}), name='ticket-list'),
    path('tickets/<int:pk>/', TicketListRetrieveView.as_view({'get': 'retrieve'}), name='ticket-retrieve'),
    path('tickets/<int:pk>/status/', TicketUpdateStatusView.as_view(), name='ticket-status-update'), 
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
]


# объединение методов админа и поддержки с префиксами и пространствами имён
urlpatterns = [
    path('admin/', include(admin_urlpatterns)),
    path('support/', include(support_urlpatterns)),
]