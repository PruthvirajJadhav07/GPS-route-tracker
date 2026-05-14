from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('snap_point/', views.snap_point, name='snap_point'),
    path('snap_chunk/', views.snap_chunk, name='snap_chunk'),
    path('save_route/', views.save_route, name='save_route'),
    path('route_history/', views.route_history, name='route_history'),
    path('get_road_path/', views.get_road_path, name='get_road_path'),
    path('embed/', views.tracker_embed, name='tracker-embed'),
    path('delete_route/<int:route_id>/', views.delete_route, name='delete-route'),
    path('live_heartbeat/', views.live_heartbeat, name='live_heartbeat'),
    path('report_mock_gps/', views.report_mock_gps, name='report_mock_gps'),
]

# ── REST API endpoints for Android GPS Tracker ──
# These are included in config/urls.py under /api/ prefix
api_urlpatterns = [
    path('devices/',                        views.DeviceListCreate.as_view(),   name='device-list'),
    path('locations/',                      views.LocationLogCreate.as_view(),  name='location-create'),
    path('devices/<int:device_id>/locations/', views.DeviceLocationList.as_view(), name='device-locations'),
    path('snap/',                           views.snap_chunk_api,               name='api-snap'),  # ← ADD
]
