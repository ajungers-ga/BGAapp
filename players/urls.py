from django.urls import path
from . import views
from .views import PlayerStatsView


urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player_list'),
    path('<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('<int:pk>/update/', views.PlayerUpdateView.as_view(), name='player_update'),
    path('<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
    path('stats/', PlayerStatsView.as_view(), name='player_stats'),
]
