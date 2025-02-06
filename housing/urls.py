from django.urls import path
from . import views

urlpatterns = [
    path('addresses/', views.address_map, name='address_map'),
]