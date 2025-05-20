# File Purpose: View logic for LEGACY TOUR HISTORY in the BGA Tour Tracker
# This file powers the "Tour Legacy" section of the site, accessible via the navbar
# Users can view a list of past seasons (2019–2024), then click into each one to see the events played
# Template 1 = legacy/tour_legacy.html → shows a list of all past seasons
# Template 2 = legacy/season_detail.html → shows events for one specific season
# Context = list of seasons, list of events (filtered by season)





#----------------------------------IMPORT DEPENDENCIES----------------------------------#

from django.shortcuts import render           # Used to render templates with context
from results.models import Event              # Pulling from Event model in the RESULTS app

#----------------------------------IMPORT DEPENDENCIES----------------------------------#






#----------------------------TOUR LEGACY (SEASON LIST VIEW)----------------------------#
def tour_legacy(request):
    # BELOW = gives a FLAT list of all UNIQUE seasons from the Event table
    # .values_list('season', flat=True) = Get only the season field, not the whole object
    # .distinct() = Only show each season once (no duplicates)
    # .order_by('-season') = Sort from most recent to oldest (top-down)
    seasons = Event.objects.values_list('season', flat=True).distinct().order_by('-season')

    # Render the legacy homepage and pass in the list of unique seasons
    return render(request, 'legacy/tour_legacy.html', {
        'seasons': seasons  # This will be looped through to create clickable buttons
    })
#----------------------------TOUR LEGACY (SEASON LIST VIEW)----------------------------#






#----------------------------SEASON DETAIL (EVENT LIST VIEW)----------------------------#
def season_detail(request, season):
    # Below = pull all events from the given season, sorted by date
    # season = dynamic value captured from the URL (e.g. /legacy/2021/)
    # .filter(season=season) = get only events from that specific season
    # .order_by('date') = show them chronologically from first to last
    events = Event.objects.filter(season=season).order_by('date')

    # Render the detail page for that season and pass both the year & list of events
    return render(request, 'legacy/season_detail.html', {
        'season': season,  # CONTEXT VARIABLE 1: This is just the year like 2021
        'events': events   # CONTEXT VARIABLE 2: This is a list of all events played that season
    })
#----------------------------SEASON DETAIL (EVENT LIST VIEW)----------------------------#
