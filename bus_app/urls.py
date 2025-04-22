from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_buses, name='home'),
    path('search/', views.search_buses, name='search_buses'),
    path('book/<int:bus_id>/', views.book_ticket, name='book_ticket'),
    path('my_trips/', views.my_trips, name='my_trips'),
    path('cancel_trip/<int:booking_id>/', views.cancel_trip, name='cancel_trip'),
    path('add_funds/', views.add_funds, name='add_funds'),
    path('wallet/', views.wallet, name='wallet'),
    path('profile/', views.profile, name='profile'),
    path('edit_booking/<int:booking_id>/', views.edit_booking_passengers, name='edit_booking_passengers'),
    path('verify-otp/<str:purpose>/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
]