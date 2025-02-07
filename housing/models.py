from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Transform


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
    id = models.CharField(max_length=255, primary_key=True)
    geom = models.GeometryField(srid=25832)
    name = models.CharField(max_length=254, null=True, blank=True)
    sport = models.CharField(max_length=254)

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




def filter_houses(
    near_bus_stop=False,
    max_distance_bus_stop=100,
    near_outdoor_activities=False,
    max_distance_outdoor_activities=200,
  
   
):
    houses = Address.objects.annotate(transformed_location=Transform('geom', 25832))

    if near_bus_stop:
        bus_stops = BusStop.objects.annotate(transformed_geom=Transform('geom', 25832))
        house_ids_near_bus_stops = set()
        for bus_stop in bus_stops:
            nearby_houses = houses.filter(
                transformed_location__distance_lte=(bus_stop.transformed_geom, D(m=max_distance_bus_stop))
            )
            house_ids_near_bus_stops.update(nearby_houses.values_list('id', flat=True))
        houses = houses.filter(id__in=house_ids_near_bus_stops)

    if near_outdoor_activities:
        outdoor_activities = OutdoorActivities.objects.annotate(transformed_geom=Transform('geom', 25832))
        house_ids_near_outdoor_activities = set()
        for activity in outdoor_activities:
            nearby_houses = houses.filter(
                transformed_location__distance_lte=(activity.transformed_geom, D(m=max_distance_outdoor_activities))
            )
            house_ids_near_outdoor_activities.update(nearby_houses.values_list('id', flat=True))
        houses = houses.filter(id__in=house_ids_near_outdoor_activities)

    return houses































    


    































'''def filter_houses(
    near_bus_stop=False,
    max_distance_bus_stop=50,
    near_outdoor_activities=False,
    max_distance_outdoor_activities=200,
):
    houses = Address.objects.annotate(transformed_location=Transform('geom', 25832))

    if near_bus_stop:
        bus_stops = BusStop.objects.annotate(transformed_geom=Transform('geom', 25832))
        houses = houses.filter(
            Q(transformed_location__distance_lte=(bus_stops.values_list("transformed_geom", flat=True).first(), D(m=max_distance_bus_stop)))
        )

    if near_outdoor_activities:
        outdoor_activities = OutdoorActivities.objects.annotate(transformed_geom=Transform('geom', 25832))
        houses = houses.filter(
            Q(transformed_location__distance_lte=(outdoor_activities.values_list("transformed_geom", flat=True).first(), D(m=max_distance_outdoor_activities)))
        )

    return houses'''


