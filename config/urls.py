from django.contrib import admin
from django.urls import path, include
from tracker.urls import api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),              # login, register, logout
    path('', include('tracker.urls')),            # home, snap, save_route etc
    path('superadmin/', include('admin_panel.urls')),
    path('api/', include((api_urlpatterns, 'tracker-api'))),
]