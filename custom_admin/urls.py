from django.urls import path
from custom_admin.views.tickets import TicketAssignView, TicketListRetrieveView, TicketUpdateStatusView
from custom_admin.views.ticket_categories import TicketCategoryCreateView
from custom_admin.views.users import UserListView


urlpatterns = [
    # Тикеты
    path('tickets/<int:pk>/status/', TicketUpdateStatusView.as_view(), name='ticket-status-update'), 
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/categories/', TicketCategoryCreateView.as_view(), name='ticket-categories'),
    path('tickets/', TicketListRetrieveView.as_view({'get': 'list'}), name='ticket-list'),
    path('tickets/<int:pk>/', TicketListRetrieveView.as_view({'get': 'retrieve'}), name='ticket-retrieve'),

    # Пользователи
    path('users/', UserListView.as_view(), name='users-list'),
]