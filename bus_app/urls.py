from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_bus/', views.add_bus, name='add_bus'),
    path('cancel_bus/<int:bus_id>/', views.cancel_bus, name='cancel_bus'),
    path('', views.search_buses, name='search_buses'),
    path('book/<int:bus_id>/', views.book_ticket, name='book_ticket'),
    path('my_trips/', views.my_trips, name='my_trips'),
    path('cancel_trip/<int:booking_id>/', views.cancel_trip, name='cancel_trip'),
    path('add_funds/', views.add_funds, name='add_funds'),
    path('bus_bookings/<int:bus_id>/', views.bus_bookings, name='bus_bookings'),
    path('update_bus/<int:bus_id>/', views.update_bus, name='update_bus'),
    path('edit_booking/<int:booking_id>/', views.edit_booking_passengers, name='edit_booking_passengers'),
    path('export_bookings/<int:bus_id>/', views.export_bookings, name='export_bookings'),
    path('verify-otp/<str:purpose>/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
]