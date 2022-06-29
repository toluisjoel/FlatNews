from django.urls import path, include
from .forms import CustomLoginForm
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.registration, name='register'),
    path('edit/', views.edit, name='edit'),
]
