from .models import Ride,Ride_Event
from rest_framework import serializers
from user.serializers import CustomUserSerializer

from datetime import timedelta
from django.utils.timezone import now


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride_Event
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    ride_event_set = RideEventSerializer(many=True,read_only=True)
    id_driver = CustomUserSerializer(read_only=True)
    id_rider = CustomUserSerializer(read_only=True)
    todays_ride_events = RideEventSerializer(many=True,read_only=True)
    
    class Meta:
        model = Ride
        fields = ['id_ride','status','pickup_latitude','id_driver','id_rider',
                  'pickup_longitude','dropoff_latitude','dropoff_longitude',
                  'pickup_time','ride_event_set','todays_ride_events']


    def get_todays_ride_events(self, obj):
        """Filter ride events that were created in the last 24 hours."""
        return RideEventSerializer(obj.ride_event_set.filter(created_at__gte=now()-timedelta(hours=24)), many=True).data