from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),    
    path('prueba/', views.prueba),
    path('eliminar/', views.eliminar),
    ]