from django.urls import path
from tickets.views import (
    TicketAssignView, TicketCommentView, TicketListCreateView, TicketUpdateStatusView, UserTicketsRetrieveView
)


urlpatterns = [
    path('', TicketListCreateView.as_view(), name='tickets-list-create'),
    path('<int:pk>/', UserTicketsRetrieveView.as_view(), name='ticket-detail'), 
    path('<int:pk>/update_status/', TicketUpdateStatusView.as_view(), name='ticket-status-update'), 
    path('<int:pk>/comments', TicketCommentView.as_view(), name='ticket-comments'),
    path('<int:pk>/assign', TicketAssignView.as_view(), name='ticket-assign'),
] 