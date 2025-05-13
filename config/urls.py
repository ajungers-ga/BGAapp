from django.contrib import admin
from django.urls import path, include
from results.views import schedule_view
from results.api_views import schedule_api
from players.api_views import players_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('players/', include('players.urls')),
    path('results/', include('results.urls')),
    path('legacy/', include('legacy.urls')),
    path('schedule/', schedule_view, name='schedule'),
    path('api/schedule/', schedule_api, name='schedule_api'),
    path('api/players/', players_api, name='players_api'),


]
