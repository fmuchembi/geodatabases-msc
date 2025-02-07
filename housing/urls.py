from django.urls import path
from . import views
from django.urls import path
from .views import MapView, FilterHousesView




urlpatterns = [
    path('map/', MapView.as_view(), name='map'),
    path('filter-houses/', FilterHousesView.as_view(), name='filter-houses'),
]
