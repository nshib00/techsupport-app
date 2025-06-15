from django.urls import path
from custom_admin.views.tickets import TicketAssignView
from custom_admin.views.ticket_categories import TicketCategoryCreateView


urlpatterns = [
    path('tickets/int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/categories/', TicketCategoryCreateView.as_view(), name='ticket-categories'),
]