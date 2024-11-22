from rest_framework import serializers
from .models import Destination, Schedule


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    destinations = DestinationSerializer(many=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        
