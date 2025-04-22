from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bus, SeatClass, Stop, Passenger, Booking

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_passenger', 'wallet_balance', 'email_verified')
    list_filter = ('is_staff', 'is_passenger', 'email_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_passenger', 'wallet_balance', 'email_verified')}),
    )

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'days_of_week')
    search_fields = ('bus_name',)

@admin.register(SeatClass)
class SeatClassAdmin(admin.ModelAdmin):
    list_display = ('bus', 'class_type', 'total_seats', 'available_seats', 'fare')
    list_filter = ('class_type',)

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('bus', 'location', 'arrival_time', 'sequence')
    list_filter = ('bus',)
    ordering = ('sequence',)

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'seat_class', 'total_cost')
    list_filter = ('seat_class', 'bus')
    search_fields = ('user__username', 'bus__bus_name')

admin.site.register(User, CustomUserAdmin)