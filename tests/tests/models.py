from django.contrib.gis.db import models

class City(models.Model):
    name = models.CharField(max_length=128)
    location = models.PointField()
