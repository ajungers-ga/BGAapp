# -------------------------------------------------------------------------------------------#
# FILE PURPOSE: Core app URL configuration for BGA Tour Tracker.
# This file defines routes for static or site-wide pages — currently just the homepage.
# The core app acts as the landing page and base layout provider for the overall site.
# This file is minimal by design because most of the routing lives in other feature apps
# like RESULTS, PLAYERS, LEGACY
# -------------------------------------------------------------------------------------------#

# WHY IS THIS FILE SO SMALL?
# This file has 2 simple jobs
# 1. Provide a landing page (home.html)
# 2. Provide a BASE layout (base.html)

#-------IMPORT DEPENDENCIES-------#
from django.urls import path
from . import views
from .views import mattydinv_view
#-------IMPORT DEPENDENCIES-------#




#--------------------DEFINE ROUTES--------------------------#
urlpatterns = [
    path('', views.home, name='home'),  # Route for homepage
    path('mattydinv/', mattydinv_view, name='mattydinv'),
]
#--------------------DEFINE ROUTES--------------------------#