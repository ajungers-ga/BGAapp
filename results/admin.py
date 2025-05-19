# File Purpose: Admin configuration for the RESULTS app in the BGA Tour Tracker
# This file controls how EVENT and SCORE models appear in the Django Admin Panel
# - Adds useful columns to the admin tables (via list_display)
# - Makes it easier to enter and manage past tournament results manually, or so i hope...
# - Includes MAJOR LABEL field for reusing major tournament names season-to-season
# - Helps with backfilling 2019–2024 seasons cleanly



#---------IMPORT DEPENDENCIES----------#
from django.contrib import admin
from .models import Event, Score
#---------IMPORT DEPENDENCIES----------#




# BELOW = 
# ensuring the major_label field is visiable when editing an event in the admin
# trying to find an easy way to asign Event Names for major Tournaments. 
# The goal is when I manually enter all of the events from the 6 years I will be able to REUSE these STATIC Tournament names...
# w/o hardcoding the event name every time. 

# ----------------------------------EventAdmin Class-----------------------------------------#
# Customize how EVENTS are displayed and edited in the admin panel
@admin.register(Event) # using PYTHON DECORATOR (@)ti decorate the class to AUTO register. = clean way of registering a DJANGO model with admin site
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',             # optional, only used for Major Tournaments
        'date',             # Date of the event
        'course_name',      # Course where the EVENT was held 
        'season',           # The year/bga season the EVENT was held    
        'is_major',         # Boonlean, to recognize Major Tournament from Scramble Tournament
        'major_label',      # Label for reusing EVENT names year to year
        'finalized'         # NEEDS WORK (Used to trigger medals and lock scores for stats)
        )
    
    # Control the fields shown on the add/edit FORM for EVENTS
    fields = ('name', 'date', 'course_name', 'season', 'is_team_event', 'is_major', 'major_label', 'finalized', 'notes')
# ----------------------------------EventAdmin Class-----------------------------------------#




# ------------------------ScoreAdmin Class-----------------------------#
# Customize how SCORES are displayed in the admin panel
# This helps me quickly view scorecards for each event and troubleshoot player data
# - 'player' and 'teammate' appear as plain text — they are CharFields, not foreign keys
# - placement, to_par, and score help visually confirm correct leaderboard results

@admin.register(Score)  # Using PYTHON DECORATOR to decorate the class to auto register the SCORE model w/ this class
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'event',        # FK (foreign key) to Event — links the score to its tournament
        'player',       # Primary player name (manual entry in the form)
        'teammate',     # Optional teammate name (if event is a team format/scramble)
        'score',        # Total number of strokes (raw score)
        'to_par',       # Score relative to par — used to sort leaderboard (NEEDS WORK. Not every course is par72)
        'placement'     # Final placement (1st, 2nd, etc.) — used for medal logic (NEEDS WORK. Why are medals awarded to lower scores?)
    )
# ------------------------ScoreAdmin Class-----------------------------#