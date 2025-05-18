# FILE PURPOSE = project level URL config for the BGA Tour Tracker app.

# ANALOGY - config/urls.py is like a traffic control center - 
# When a user visits an events url like /results/5 - This file directs that request to result/ urls.py, 
# which passes it to the correct view (leaderboard_view)

# This file defines the ROOT URLS paths and gives routing to the respective apps:
# 1. CORE - Homepage and static content
# 2. PLAYERS - PLAYER data and stats
# 3. RESULTS - EVENT data & LEADERBOARD VIEWS 
# 4. LEGACY - Past season data
# 5. API end points for SCHEDULE and PLAYERS

# WHY IS THIS FILE IMPORTANT? 

# 1.1 This file connects the whole app. It wires the root URL paths to the correct DJANGO apps. 
# 1.2 W/o this file, DJANGO wouldnt know where to send incoming requests.

# 2.1 It keeps the whole app MODULAR. 
# 2.2 Instead of putting all URLS in one file - I am delegating the routing of each app using include()
# 2.3 This keeps the project orgainized and scalable, which is helpful bc there are multiple apps tied together

# 3.1 It handles GLOBAL routes and APIs.
# 3.2 It handles HIGH LEVEL routes that DONT belong to a single app (api/schedule/)
# 3.3 This file gives FLEXIBILITY to mix moth HTML VIEWS and JSON API endpoints

# 4.1 It mirrors my project architecture - 
# 4.2 Every app has its own urls.py, views.py and models.py
# 4.3 This root file ties them all together, acting like a table of contents for the entire site/project


#-----------------IMPORT DEPENDENCIES-----------------#
from django.contrib import admin
from django.urls import path, include
from results.views import schedule_view
from results.api_views import schedule_api
from players.api_views import players_api
#-----------------IMPORT DEPENDENCIES-----------------#


#-----------------------------------------DEFINE PATHS-------------------------------------------------------#
urlpatterns = [
    path('admin/', admin.site.urls),                            # DJANGO admin interface
    path('', include('core.urls')),                             # Home page and other static pages
    path('players/', include('players.urls')),                  # All PLAYER related routes (CRUD and Stats)
    path('results/', include('results.urls')),                  # All EVENT & LEADERBOARD routes
    path('legacy/', include('legacy.urls')),                    # Historical season stats pages
    path('schedule/', schedule_view, name='schedule'),          # Rendering the SCHEDULE html page (views.py)
    path('api/schedule/', schedule_api, name='schedule_api'),   # API end point for SCHEDULE data  (json)
    path('api/players/', players_api, name='players_api'),      # API end point for PLAYER data (json)
]
#-----------------------------------------DEFINE PATHS--------------------------------------------------------#