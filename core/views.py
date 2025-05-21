# FILE Purpose: View logic for general pages in the BGA Tour Tracker
# This file is part of the CORE app and powers the homepage (`home.html`)
# It pulls data from the RESULTS app and displays upcoming and recent events
# Uses Django’s built-in timezone support
# Template = core/home.html
# Context = next_event (upcoming), last_event (most recent)
# The COUNTDOWN TRACKER is not found in this file, It exists entirely in the core/home.html, NOT in PYTHONviews




#----------------------------------IMPORT DEPENDENCIES----------------------------------#

from django.shortcuts import render     # Needed to render HTML templates with context
from django.utils import timezone       # Provides timezone-aware datetime objects
from results.models import Event        # importing Event model from results app

#----------------------------------IMPORT DEPENDENCIES----------------------------------#





# BELOW = This view handles the HOME page logic
# It checks todays date and pulls the next upcoming event (date >= today)
# and the last event that already happened (date < today)
# These are passed to the template so they can be displayed in highlight cards

#-----------------------------HOME PAGE VIEW--------------------------------#
# The COUNTDOWN TRACKER is not found in this file, It exists entirely in the core/home.html, NOT in PYTHONviews


def home(request):
    today = timezone.now().date() 
    # timzeone.now = DJANGOS timezone-aware FUNCTION to get the EXACT time in USERS location
    # .date() = EXTRACTING just the date part of the date/time
    # calling two METHODS ABOVE,
    # both need parentheses because they're FUNCTIONS in PYTHON
    

    # Get the next upcoming event--------------------------------------------#
    next_event = Event.objects.filter(date__gte=today).order_by('date').first()
    # Event.objects = access the EVENT models data using DJANGOS OBJECT RELATIONAL MAPPING (lets me interact w/database using PYTHON instead of writing raw SQL)
    # .filter(date__gte=today) = filter EVENTS where the DATE is greater than to today (today or in the future)
    # date__gte? -underscores are DJANGO way of CHAINING look up - (lookup MODIFIER meaning greater than or equal to)
    # .order_by('date') = sort through those EVENTS ascending in order by date (soonest first and so on)
    # .first = return only the FIRST EVENT in the sorted list aka the NEXT EVENT
    #------------------------------------------------------------------------#
    
    
    # Get the last completed event---------------------------------------------#
    last_event = Event.objects.filter(date__lt=today).order_by('-date').first()
    # Event.objects = access the EVENT models data using DJANGOS OBJECT RELATIONAL MAPPING (ORM)
    # .filter(date__lt=today) = filter EVENTS where the DATE is less than today (aka events that already happened)
    # date__lt? -underscores are DJANGO way of CHAINING look up - (lookup MODIFIER meaning LESS THAN)
    # .order_by('-date') = sort those EVENTS in descending order (most recent first, going backwards)
    # .first = return only the FIRST EVENT in that list — aka the LAST EVENT that was played
    #--------------------------------------------------------------------------#


    # Return an HTTP response rendered from the 'core/home.html' template-----#
    # request = the incoming HTTP request from the browser
    # core/home.html = the template being loaded from the core app
    # { context } = a dictionary of dynamic data sent to the template
    # which can be accessed using {{ next_event }} and {{ last_event }} in the template    
    return render(request, 'core/home.html', {
    'next_event': next_event,   # context variable #1 → passed into the template
    'last_event': last_event    # context variable #2 → also used in the homepage display
})
    #---------------------------------------------------------------------------#

#-----------------------------HOME PAGE VIEW--------------------------------#