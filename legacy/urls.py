# -------------------------------------------------------------------------------------------#
# FILE PURPOSE: Legacy app URL configuration for BGA Tour Tracker.
# This file defines routes for historical season pages, including:
# 1. A landing page showing all available seasons (tour_legacy)
# 2. A detail page showing results for a selected season (season_detail)
# The legacy app focuses exclusively on static season-by-season data from 2019–2024.
# -------------------------------------------------------------------------------------------#

# WHY IS THIS FILE SO SMALL?
# This app has 1 job: let users browse historical BGA Tour results
# All complex logic and dynamic updates happen in the RESULTS app instead

#-------IMPORT DEPENDENCIES-------#
from django.urls import path
from . import views
#-------IMPORT DEPENDENCIES-------#


#--------------------DEFINE ROUTES--------------------------#
urlpatterns = [
    path('', views.tour_legacy, name='tour_legacy'),              # /legacy/
    path('<int:season>/', views.season_detail, name='season_detail'),  
]

# using <int:season>/ to DYNAMICALLY convert a value(int=number), to a specificic season page
# views.season_detail = the VIEW function that will run when someone visits /legacy/2022 or /legacy/2023
# season_detail = a named route that can be used in templates like {% url 'season_detail' 2023 %}

# EXAMPLE BELOW

# 1. A user visits a url like /legacy/2021
# 2. It matches this pattern <int:season>/
# 3. which means (season = 2021)
# 4. so DJANGO calls: season_detail(request, season=2021)
#--------------------DEFINE ROUTES--------------------------#
