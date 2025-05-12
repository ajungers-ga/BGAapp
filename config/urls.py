from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('players/', include('players.urls')),
    path('results/', include('results.urls')),
    path('legacy/', include('legacy.urls')),


]
