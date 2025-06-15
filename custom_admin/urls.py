from django.urls import path
from custom_admin.views.tickets import TicketAssignView, TicketUpdateStatusView
from custom_admin.views.ticket_categories import TicketCategoryCreateView
from custom_admin.views.users import UserListView


urlpatterns = [
    # Тикеты
    path('tickets/<int:pk>/status/', TicketUpdateStatusView.as_view(), name='ticket-status-update'), 
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/categories/', TicketCategoryCreateView.as_view(), name='ticket-categories'),

    # Пользователи
    path('users/', UserListView.as_view(), name='users-list'),
]