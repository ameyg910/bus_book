from django.contrib import admin
from .models import User, Bus, SeatClass, Stop, Passenger, Booking

admin.site.register(User)
admin.site.register(Bus)
admin.site.register(SeatClass)
admin.site.register(Stop)
admin.site.register(Passenger)
admin.site.register(Booking)