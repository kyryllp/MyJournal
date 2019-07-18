from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .models import User

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout')
]