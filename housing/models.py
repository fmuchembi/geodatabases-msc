from django.db import models
from django.contrib.gis.db import models



class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.GeometryField()
    name = models.CharField(max_length=254)

    class Meta:
        managed = False 
        db_table = 'hostel'  

    def __str__(self):
        return self.name