from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from allauth.socialaccount.models import SocialAccount
from django.db import transaction
from .models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.is_passenger = True
        user.is_admin = False
        return user

    @transaction.atomic
    def save_user(self, request, sociallogin, form=None):
        """
        Override to handle existing users with the same email
        """
        user = sociallogin.user
        email = user.email
        
        # Check if a user with this email already exists
        existing_user = User.objects.filter(email=email).first()
        
        if existing_user:
            # If user exists, check if they already have a social account
            existing_social_accounts = SocialAccount.objects.filter(user=existing_user, provider='google')
            
            if existing_social_accounts.exists():
                # If social accounts exist, update the first one and delete others
                first_account = existing_social_accounts.first()
                first_account.uid = sociallogin.account.uid
                first_account.extra_data = sociallogin.account.extra_data
                first_account.save()
                
                # Delete other social accounts for this user
                existing_social_accounts.exclude(id=first_account.id).delete()
                
                sociallogin.account = first_account
            else:
                # If no social account exists, connect it
                sociallogin.connect(request, existing_user)
            
            return existing_user
            
        # If no existing user, proceed with normal save
        return super().save_user(request, sociallogin, form)

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Enable auto signup for social accounts
        """
        return True

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        """
        try:
            # Get the user's email from the social login
            email = sociallogin.account.extra_data.get('email')
            if email:
                # Check if a user with this email already exists
                existing_user = User.objects.filter(email=email).first()
                if existing_user:
                    # If user exists, connect the social account to the existing user
                    sociallogin.connect(request, existing_user)
        except Exception as e:
            print(f"Error in pre_social_login: {str(e)}")