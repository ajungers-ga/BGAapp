# -------------------------------------------------------------------------------------------#
# FILE PURPOSE: URL configuration for the Tour Results section of BGAapp.
# This file defines all routes related to current-season BGA events:
# 1. Event list, update, and delete views
# 2. Leaderboard view for each event
# 3. Score editing and deletion
# 4. A schedule view for viewing all upcoming/played events
#
# This is one of the most dynamic parts of the app and drives the real-time tournament logic.
# 
# See the NOTABLE DYNAMIC ROUTES COMMENTS below the routes
# -------------------------------------------------------------------------------------------#

#---------IMPORT DEPENDENCIES----------#
from django.urls import path
from . import views
from results.views import schedule_view
#---------IMPORT DEPENDENCIES----------#


#----------------------------------DEFINE ROUTES----------------------------------#
urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('<int:pk>/leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('score/<int:score_id>/edit/', views.edit_score_view, name='edit_score'),
    path('score/<int:pk>/delete/', views.delete_score, name='delete_score'),
    path('schedule/', schedule_view, name='schedule'),
]
#----------------------------------DEFINE ROUTES----------------------------------#

# NOTABLE DYNAMIC ROUTES
#
# 1. <int:pk>/leaderboard/
# This shows the RESULTS table for that event
#
# 2. score/<int:score_id>/edit/
# Lets users edit a score (used in admin or UI forms)
#
# 3. score/<int:pk>/delete/
# Deletes a SPECIFIC score
#
# 4. schedule/ 
# Mirrors the top level /schedule/ for internal reuse (though im not sure i need it right now)