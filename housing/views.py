
from django.shortcuts import render
from django.core.serializers import serialize
from .models import filter_houses
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


# Render HTML page
class MapView(TemplateView):
    template_name = 'housing/index.html'  

# View for the API endpoint
class FilterHousesView(View):
    def get(self, request):
        near_bus_stop = request.GET.get('near_bus_stop', '').lower() == 'true'
        near_outdoor_activities = request.GET.get('near_outdoor_activities', '').lower() == 'true'
        #near_university = request.GET.get('near_university', '').lower() == 'true'
        #near_green_spaces = request.GET.get('near_green_spaces', '').lower() == 'true'
       

        houses = filter_houses(
            near_bus_stop=near_bus_stop,
            near_outdoor_activities=near_outdoor_activities,
            #near_university=near_university,
            #near_green_spaces=near_green_spaces,
           
        )

        # Serialize the results
        results = [
            {
                'id': house.id,
                'name': house.name,
                'latitude': house.geom.y,
                'longitude': house.geom.x,
            }
            for house in houses
        ]

        return JsonResponse(results, safe=False)
    







