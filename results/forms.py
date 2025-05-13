# File Purpose:
# Defines the EventForm used to create and edit Event model entries.
# Adds a calendar widget and placeholder to the date field.
# attrs is short for HTML attrbutes, in this case type and placeholder are used

from django import forms
from .models import Event, Score

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',               # shows clickable calendar in supported browsers
                'placeholder': 'MM/DD/YYYY'   # gives user a hint of the expected format
            })
        }

# This form is used to enter player scores for a specific event
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['player', 'teammate', 'score']
