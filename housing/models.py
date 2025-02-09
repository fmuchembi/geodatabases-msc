from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Transform
from django.db.models import Q



class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.GeometryField(srid=25832)
    name = models.CharField(max_length=254)

    class Meta:
        managed = False 
        db_table = 'hostel'  

    def __str__(self):
        return self.name


class OutdoorActivities(models.Model):
    ACTIVITY_TYPES = [
        ('soccer', 'soccer'),
        ('basketball', 'basketball'),
        ('volleyball', 'volleyball'),
        ('athletics', 'athletics'),
    ]
    id = models.CharField(max_length=255, primary_key=True)
    geom = models.GeometryField(srid=25832)
    sport = models.CharField(max_length=254, choices=ACTIVITY_TYPES)

    class Meta:
        managed = False 
        db_table = 'outdoor_activities'  

    def __str__(self):
        return self.id 


class BusStop(models.Model):
    id = models.AutoField(primary_key=True)
    geom = models.PointField(srid=25832)
    stop_id = models.CharField(max_length=255)
    stop_name = models.CharField(max_length=255)

    class Meta:
        managed = False 
        db_table = 'bus_stops'  

    def __str__(self):
        return self.stop_name
    

class Buildings(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  
    addr_postc = models.CharField(max_length=255)  
    geom = models.GeometryField(srid=25832)
    addr_stree = models.CharField(max_length=255)  
    building = models.CharField(max_length=255)  
    name = models.CharField(max_length=255)  

    class Meta:
        managed = False 
        db_table = 'university_buildings' 

    def __str__(self):
        return self.name
    

class Districts(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.GeometryField(srid=25832)
    name = models.CharField(max_length=254)

    class Meta:
        managed = False 
        db_table = 'districts'  

    def __str__(self):
        return self.name
    


def filter_houses(
    near_bus_stop=False,
    max_distance_bus_stop=100,
    activity_type=None, 
    university_building_name=None,
    district = None
):
    houses = Address.objects.annotate(transformed_location=Transform('geom', 25832))

    # Filter houses near bus stops
    if near_bus_stop:
        bus_stops = BusStop.objects.annotate(transformed_geom=Transform('geom', 25832))
        house_ids_near_bus_stops = set()
        for bus_stop in bus_stops:
            nearby_houses = houses.filter(
                transformed_location__distance_lte=(bus_stop.transformed_geom, D(m=max_distance_bus_stop))
            )
            house_ids_near_bus_stops.update(nearby_houses.values_list('id', flat=True))
        houses = houses.filter(id__in=house_ids_near_bus_stops)

    # Filter houses near a university building
    if university_building_name:
        try:
            university_building = Buildings.objects.get(name=university_building_name)
            university_building_geom = Transform(university_building.geom, 25832)
            houses = houses.filter(
                transformed_location__distance_lte=(university_building_geom, D(m=500))
            )
        except Buildings.DoesNotExist:
            houses = houses.none()

    
    # Filter with Districts
    if district:
        try:
            district_name = Districts.objects.get(name=district) 
            district_geom = Transform(district_name.geom, 25832) 

            houses = houses.filter(
                Q(transformed_location__within=district_geom) | 
                Q(transformed_location__intersects=district_geom)
            )

        except Districts.DoesNotExist:
            houses = houses.none()  

    # Filter houses near outdoor activities
    if  activity_type:
        try:
            outdoor_activities = OutdoorActivities.objects.get(sport=activity_type)
            outdoor_activities_geom = Transform(outdoor_activities.geom, 25832)
            houses = houses.filter(
                    transformed_location__distance_lte=(outdoor_activities_geom , D(m=100))
            )
        except OutdoorActivities.DoesNotExist:
                houses = houses.none()
    
    return houses
    

