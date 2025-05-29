# File Purpose: Form definitions for the RESULTS app in the BGA Tour Tracker
# This file defines custom DJANGO forms used to create or update EVENT and SCORE entries.
# Adds a calendar widget and placeholder to the date field.
# - EventForm: for entering or editing tournaments
# - ScoreForm: for entering or editing player scores

# Widgets and attributes let me control how each form field shows up in the browser
# i define them inside the Meta class using a widgets = {} dictionary
# For example:
# - 'date': forms.DateInput - makes the DATE field show up as a calendar input (<input type="date">)
# - 'notes': forms.Textarea - makes the NOTES field a bigger text box (instead of a small single line)

# Inside each widget, I use attrs={} to fine-tune how the field looks:
# - 'class': lets me apply Bootstrap styling (like 'form-control' or 'form-check-input')
# - 'placeholder': adds helper text inside the input to guide the user
# - 'type': lets me force the HTML input type (like 'date', 'text', etc.)

# These widgets dont change the actual model or form logic — they just control the frontend experience





#---------IMPORT DEPENDENCIES----------#
from django import forms
from .models import Score, Event
# from players.models import Player  # COMMENTED OUT BC-
# (using player names in score form but treating player and teammate as plain charfields, not as model-bound fields)
#---------IMPORT DEPENDENCIES----------#



# ----------------------------------------Score form------------------------------------#
class ScoreForm(forms.ModelForm):  # Results/#/Leaderboard/addNewScore form
    player = forms.CharField(
        label='Player',
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})  # Enables the autocomplete suggestions
    )
    teammate = forms.CharField(
        label='Teammate',
        required=False,
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})  # Matches an HTML <datalist> element
    )
    third_player = forms.CharField(
        label='Third Player',
        required=False,
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})  # Optional input
    )
    fourth_player = forms.CharField(
        label='Fourth Player',
        required=False,
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})  # Optional input
    )

    # META is an INNER class in DJANGO used to store CONFIGURATION for things like: 
    # forms, widgets, models & even serializers
    class Meta:         
        model = Score         # Telling DJANGO we want to use the SCORE model
        fields = ['score']    # Only include SCORE field here (others are manually customized)
# ----------------------------------------Score form------------------------------------#



# -----------------------------Event form-----------------------------------------------#
class EventForm(forms.ModelForm):  # /tourResults/createNewEvent form
    class Meta:     
        model = Event
        fields = '__all__'  # or ['name', 'date', 'course', 'format', etc.]
        # BELOW = customize how the DATE field appears in the browser
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control'
            })
        }
# -----------------------------Event form-----------------------------------------------#
