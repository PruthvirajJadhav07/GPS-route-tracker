from django.db import models
from django.contrib.auth.models import User

class RouteLog(models.Model):
    user         = models.ForeignKey(
                       User,
                       on_delete=models.CASCADE,
                       related_name='routes'
                   )
    created_at   = models.DateTimeField(auto_now_add=True)
    start_lat    = models.FloatField()
    start_lon    = models.FloatField()
    end_lat      = models.FloatField()
    end_lon      = models.FloatField()
    route_points = models.JSONField(default=list)
    total_points = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Route by {self.user.username} on {self.created_at}'


class Device(models.Model):
    """
    Represents a registered tracking device (Android phone).
    Each device gets a unique device_id used to tag its location pings.
    """
    device_id   = models.CharField(max_length=255, unique=True)
    name        = models.CharField(max_length=255, blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.device_id


class LocationLog(models.Model):
    """
    A single GPS coordinate ping sent from a tracked device.
    Stores latitude, longitude, speed, and the timestamp from the device.
    """
    device      = models.ForeignKey(
                      Device,
                      on_delete=models.CASCADE,
                      related_name='locations'
                  )
    latitude    = models.FloatField()
    longitude   = models.FloatField()
    speed       = models.FloatField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.device} @ {self.latitude},{self.longitude}'

class LiveHeartbeat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='heartbeats')
    lat = models.FloatField()
    lon = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    battery_level = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Heartbeat: {self.user.username} - {self.status} at {self.last_updated}'


class MockGPSViolation(models.Model):
    """
    Logs every instance when an employee is caught using a
    fake/mock GPS location provider (e.g., Fake GPS app).
    Visible to superadmin/manager in the admin panel.
    """
    user       = models.ForeignKey(
                     User,
                     on_delete=models.CASCADE,
                     related_name='mock_violations'
                 )
    latitude   = models.FloatField(null=True, blank=True)
    longitude  = models.FloatField(null=True, blank=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    device_info = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f'⛔ MOCK GPS: {self.user.username} at {self.detected_at}'


class SpeedingViolation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speeding_violations')
    speed = models.FloatField() # Speed in km/h
    latitude = models.FloatField()
    longitude = models.FloatField()
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f'Speeding: {self.user.username} at {self.speed:.1f}km/h'


class Geofence(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_meters = models.FloatField(default=100.0)

    def __str__(self):
        return self.name


class GeofenceEvent(models.Model):
    ACTION_CHOICES = (
        ('enter', 'Entered'),
        ('exit', 'Exited'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='geofence_events')
    geofence = models.ForeignKey(Geofence, on_delete=models.CASCADE, related_name='events')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} {self.action} {self.geofence.name}'


class UserGeofenceState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    geofence = models.ForeignKey(Geofence, on_delete=models.CASCADE)
    is_inside = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'geofence')
