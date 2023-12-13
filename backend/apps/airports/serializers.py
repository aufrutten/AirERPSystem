
from rest_framework import serializers
from . import models


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Airport
        fields = '__all__'
