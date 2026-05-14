from rest_framework import serializers
from .models import Device, LocationLog


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Device
        fields = ['id', 'device_id', 'name', 'created_at']


class LocationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LocationLog
        fields = ['id', 'device', 'latitude', 'longitude', 'speed', 'timestamp']
