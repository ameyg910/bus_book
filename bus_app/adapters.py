from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.is_passenger = True
        user.is_admin = False
        return user