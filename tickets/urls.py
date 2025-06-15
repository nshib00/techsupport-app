from django.urls import path
from tickets.views import (
    TicketCommentView, TicketListCreateView, UserTicketsRetrieveView
)


urlpatterns = [
    path('', TicketListCreateView.as_view(), name='tickets-list-create'),
    path('<int:pk>/', UserTicketsRetrieveView.as_view(), name='ticket-detail'), 
    path('<int:pk>/comments/', TicketCommentView.as_view(), name='ticket-comments'),  
] 