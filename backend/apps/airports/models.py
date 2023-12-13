

from django.db import models
from django.db.models.manager import Manager


class AirportManager(Manager):
    pass


class Airport(models.Model):
    objects = AirportManager()

    id = models.CharField(primary_key=True, max_length=10)
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    iata_code = models.CharField(max_length=4, null=True, blank=True)

    latitude_deg = models.FloatField()
    longitude_deg = models.FloatField()

    continent = models.CharField(max_length=3)
    iso_country = models.CharField(max_length=3)
    iso_region = models.CharField(max_length=8)
    municipality = models.CharField(max_length=128)

    scheduled_service = models.BooleanField(default=False)
    keywords = models.CharField(max_length=256, null=True, blank=True)

    last_update = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.iata_code} {self.name}"
