import random
from django.core.mail import send_mail
from django.utils import timezone
from bus_project.settings import EMAIL_HOST_USER
import uuid
from .models import OTP

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))  # Generates a 6-digit OTP

def send_otp_email(user, purpose):
    otp = generate_otp()
    expires_at = timezone.now() + timezone.timedelta(minutes=10)  # 10-minute expiry
    OTP.objects.create(user=user, otp=otp, expires_at=expires_at, purpose=purpose)
    subject = f"Your OTP for {purpose.capitalize()}"
    message = f"Dear {user.username},\n\nYour OTP is {otp}. It expires in 10 minutes.\n\nHappy traveling!"
    send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)

def send_verification_email(user):
    token = str(uuid.uuid4())  # Unique token
    user.email_verification_token = token
    user.email_verification_expiry = timezone.now() + timezone.timedelta(hours=24)  # 24-hour expiry
    user.save()
    verification_url = f"http://127.0.0.1:8000/verify-email/{token}/"
    subject = "Verify Your Email"
    message = f"Dear {user.username},\n\nClick this link to verify your email: {verification_url}\nIt expires in 24 hours.\n\nWelcome aboard!"
    send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)
"""
def send_booking_confirmation_email(booking):
    subject = "Booking Confirmation"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.bus.bus_name} ({booking.seat_class.class_type}) from {booking.start_stop.location} to {booking.end_stop.location} is confirmed!\nTotal Cost: ${booking.total_cost}\n\nEnjoy your trip!"
    send_mail(subject, message, EMAIL_HOST_USER, [booking.user.email], fail_silently=False)
"""
def send_booking_confirmation_email(booking):
    send_mail(
        'Booking Confirmation',
        f"Your booking for {booking.bus.bus_name} is confirmed!",
        EMAIL_HOST_USER,  # From .env
        [booking.user.email],
        fail_silently=False
    )