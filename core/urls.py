from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search_train/', views.SearchTrain, name="search_train"),
    path('available_seat/', views.SeatPlan, name='seatplan'),
    path('buy_tiicket',views.BuyTicket,name="buyticket"),
    path('train_information/',views.train_info,name='train_info'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('ticket/',views.ticket,name='ticket'),
    path('download-ticket/',views.generate_ticket_pdf, name='download_ticket'),
    
    
]