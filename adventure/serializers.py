from adventure.models import Vehicle
from rest_framework import serializers


class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()
   

"""    
class CreateVehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField()           
    name = serializers.CharField()
    passengers = serializers.IntegerField()
    vehicle_type = serializers.CharField()
"""