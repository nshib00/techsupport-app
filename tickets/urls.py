from django.urls import path
from tickets.views.ticket_comments import TicketCommentView
from tickets.views.tickets import TicketListCreateView, UserTicketsRetrieveView
from tickets.views.ticket_categories import TicketCategoryListView


urlpatterns = [
    path('', TicketListCreateView.as_view(), name='tickets-list-create'),
    path('<int:pk>/', UserTicketsRetrieveView.as_view(), name='ticket-detail'), 
    path('<int:pk>/comments/', TicketCommentView.as_view(), name='ticket-comments'),  
    path('categories/', TicketCategoryListView.as_view(), name='ticket-categories'),
] 