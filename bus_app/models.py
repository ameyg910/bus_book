from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_passenger = models.BooleanField(default=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    email_verified = models.BooleanField(default=False)  # New: Tracks email verification
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)  # New: Token for link
    email_verification_expiry = models.DateTimeField(blank=True, null=True)  # New: Expiry for link

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Expiry time
    purpose = models.CharField(max_length=20)  # 'signup' or 'booking'

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.purpose} - {self.otp}"

class Bus(models.Model):
    bus_name = models.CharField(max_length=100)
    days_of_week = models.CharField(max_length=50)

    def __str__(self):
        return self.bus_name

class SeatClass(models.Model):
    SEAT_CLASSES = (
        ('General', 'General'),
        ('Sleeper', 'Sleeper'),
        ('Luxury', 'Luxury'),
    )
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seat_classes')
    class_type = models.CharField(max_length=10, choices=SEAT_CLASSES)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.class_type} - {self.bus.bus_name}"

class Stop(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='stops')
    location = models.CharField(max_length=100)
    arrival_time = models.DateTimeField()
    sequence = models.IntegerField()  # Order of stops (1 = first, 2 = second, etc.)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.location} ({self.bus.bus_name})"

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_time = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='start_bookings', null=True, blank=True)
    end_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='end_bookings', null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.user} for {self.bus} ({self.start_stop} to {self.end_stop})"