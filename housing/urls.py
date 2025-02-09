from django.urls import path
from . import views
from django.urls import path
from .views import MapView, FilterHousesView, GetUniversityBuildingsView, GetOutdoorActivities,GetDistrictsWithHostels




urlpatterns = [
    path('map/', MapView.as_view(), name='map'),
    path('filter-houses/', FilterHousesView.as_view(), name='filter-houses'),
    path('get-university-buildings/', GetUniversityBuildingsView.as_view(), name='get-university-buildings'),
    path('get-outdoor-activities/', GetOutdoorActivities.as_view(), name='get-outdoor-activities'),
    path('get-districts/', GetDistrictsWithHostels.as_view(), name='get-districts')
]
