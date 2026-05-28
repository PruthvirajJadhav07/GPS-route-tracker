from django.contrib import admin
from .models import RouteLog, LiveHeartbeat, Geofence, GeofenceEvent, SpeedingViolation

admin.site.register(Geofence)
admin.site.register(GeofenceEvent)
admin.site.register(SpeedingViolation)

admin.site.register(RouteLog)
class RouteLogAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_points")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(LiveHeartbeat)
class LiveHeartbeatAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "speed", "battery_level", "last_updated")
    list_filter = ("status", "last_updated")
    search_fields = ("user__username",)
    ordering = ("-last_updated",)
