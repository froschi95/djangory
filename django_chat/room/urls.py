from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
]
