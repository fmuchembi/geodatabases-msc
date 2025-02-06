from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.core.serializers import serialize
from .models import Address

def address_map(request):
    addresses = Address.objects.all()
    address_geojson = serialize('geojson', addresses,
        geometry_field='geom',
        fields=('name',))
    
    return render(request, 'housing/map.html', {
        'address_data': address_geojson,
    })