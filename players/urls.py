# -------------------------------------------------------------------------------------------#
# FILE PURPOSE: Players app URL configuration for BGA Tour Tracker.
# This file defines routes for player-related pages, including:
# 1. Player list and detail views
# 2. Update and delete views for player profiles
# 3. A custom stats page showing career totals
# This app uses DJANGOS class based views for consistent structure and simplicity.
# -------------------------------------------------------------------------------------------#


#-------IMPORT DEPENDENCIES-------#
from django.urls import path
from . import views
from .views import PlayerStatsView
#-------IMPORT DEPENDENCIES-------#



#------------------------------DEFINE ROUTES------------------------------------------#
urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player_list'),
    # path('<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    # path('<int:pk>/update/', views.PlayerUpdateView.as_view(), name='player_update'),
    path('<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
    path('stats/', PlayerStatsView.as_view(), name='player_stats'),
]
#------------------------------DEFINE ROUTES------------------------------------------#

# WHAT IS <int:pk>?
# 1. Expect a NUMBER in the URL
# 2. Pass it to the VIEW as the variable (primary key) 
# 3. This is used ny DJANGOS built in generic views like (DetailView, UpdateView and DeleteView)