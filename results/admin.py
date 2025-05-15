from django.contrib import admin
from .models import Event, Score

# BELOW = 
# ensuring the major_label field is visiable when editing an event in the admin
# trying to find an easy way to asign Event Names for major Tournaments. 
# The goal is when I manually enter all of the events from the 6 years I will be able to REUSE these STATIC Tournament names...
# w/o hardcoding the event name every time. 
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'course_name', 'season', 'is_major', 'major_label', 'finalized')
    fields = ('name', 'date', 'course_name', 'season', 'is_team_event', 'is_major', 'major_label', 'finalized', 'notes')


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('event', 'player', 'teammate', 'score', 'to_par', 'placement')