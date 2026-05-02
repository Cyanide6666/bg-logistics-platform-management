from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('cliente/', views.panel_cliente, name='panel_cliente'),  
]