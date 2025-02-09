#from django.core.serializers import serialize
from .models import filter_houses
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Buildings,OutdoorActivities, Address, Districts
from django.contrib.gis.db.models.functions import Transform
from django.db.models import Q


# Render HTML page
class MapView(TemplateView):
    template_name = 'housing/index.html'  

# View for the API endpoint
class FilterHousesView(View):
    def get(self, request):
        near_bus_stop = request.GET.get('near_bus_stop', '').lower() == 'true'
        activity_type = request.GET.get('activity_type', None)  
        university_building_name = request.GET.get('university_building_name', None)
        district = request.GET.get('district', None)
       

       
        houses = filter_houses(
            near_bus_stop=near_bus_stop,
            activity_type=activity_type,  
            university_building_name = university_building_name,
            district = district
        )

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
    
   
class GetUniversityBuildingsView(View):
    def get(self, request):
        buildings = Buildings.objects.filter(name__icontains="institut").values('name').distinct()
        return JsonResponse(list(buildings), safe=False)
    
class GetOutdoorActivities(View):
    def get(self, request):
        outdoor_activities = OutdoorActivities.objects.values('sport').distinct()
        return JsonResponse(list(outdoor_activities), safe=False)
    
class GetDistrictsWithHostels(View):
    def get(self, request):
        districts = Districts.objects.annotate(
            transformed_geom=Transform('geom', 25832)
        )
        
        districts_with_addresses = set()
        for district in districts:
            has_address = Address.objects.annotate(
                transformed_point=Transform('geom', 25832)
            ).filter(
                Q(transformed_point__within=district.transformed_geom) |
                Q(transformed_point__intersects=district.transformed_geom)
            ).exists()
            
            if has_address:
                districts_with_addresses.add(district.name)
        
        results = [{'name': name} for name in districts_with_addresses]
        
        print(f"Found {len(results)} districts containing addresses")
        
        return JsonResponse({
            'status': 'success',
            'count': len(results),
            'districts': results
        }, safe=False)
 









    







































