from django.contrib import admin
from django.urls import path, include
from results.views import schedule_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('players/', include('players.urls')),
    path('results/', include('results.urls')),
    path('legacy/', include('legacy.urls')),
    path('schedule/', schedule_view, name='schedule'),


]
