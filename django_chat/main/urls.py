from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, register


urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
