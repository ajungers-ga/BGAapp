# File Purpose: URL patterns for the Tour Results section of BGAapp
from django.urls import path
from . import views
from results.views import schedule_view

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
]
