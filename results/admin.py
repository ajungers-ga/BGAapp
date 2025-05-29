# File Purpose: Admin configuration for the RESULTS app in the BGA Tour Tracker
# This file controls how EVENT and SCORE models appear in the Django Admin Panel
# - Adds useful columns to the admin tables (via list_display)
# - Makes it easier to enter and manage past tournament results manually
# - Includes MAJOR LABEL field for reusing major tournament names season-to-season
# - Helps with backfilling 2019–2024 seasons cleanly

#---------IMPORT DEPENDENCIES----------#
from django.contrib import admin
from .models import Event, Score
#---------IMPORT DEPENDENCIES----------#

# ----------------------------------EventAdmin Class-----------------------------------------#
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'course_name',
        'season',
        'is_major',
        'major_label',
        'finalized'
    )
    fields = ('name', 'date', 'course_name', 'season', 'is_team_event', 'is_major', 'major_label', 'finalized', 'notes')
# ----------------------------------EventAdmin Class-----------------------------------------#

# ----------------------------------ScoreAdmin Class-----------------------------------------#
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'player',
        'teammate',
        'third_player',
        'fourth_player',
        'score',
        'to_par',
        'placement'
    )
    search_fields = ('player__first_name', 'player__last_name', 'teammate__first_name', 'teammate__last_name')
    list_filter = ('event', 'placement')
    ordering = ('event', 'score')  # Lowest scores appear first within each event
# ----------------------------------ScoreAdmin Class-----------------------------------------#
