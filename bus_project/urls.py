from django.contrib import admin
from django.urls import path, include
from bus_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),  # Must be present
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logged-out/', views.CustomLogoutView.as_view(), name='logged_out'),
    path('', include('bus_app.urls')),
]