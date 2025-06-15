from django.urls import path
from custom_admin.views.tickets import TicketAssignView


urlpatterns = [
    path('tickets/int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
]