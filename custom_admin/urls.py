from django.urls import include, path
from custom_admin.views.support.tickets import TicketAssignView, TicketListRetrieveView, TicketUpdateStatusView
from custom_admin.views.admin.ticket_categories import TicketCategoryCreateView
from custom_admin.views.admin.users import UserListView, UserUpdateRoleView


admin_urlpatterns = [
    # Категории тикетов
    path('tickets/categories/', TicketCategoryCreateView.as_view(), name='ticket-categories'),

    # Пользователи
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/role/', UserUpdateRoleView.as_view(), name='change-user-role'),
]

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