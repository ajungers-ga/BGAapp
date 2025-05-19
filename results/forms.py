# File Purpose: Form definitions for the RESULTS app in the BGA Tour Tracker
# This file defines custom DJANGO forms used to create or update EVENT and SCORE entries.
# Adds a calendar widget and placeholder to the date field.
# - EventForm: for entering or editing tournaments
# - ScoreForm: for entering or editing player scores

# Widgets and attributes are used to control how fields appear in the browser.

#---------IMPORT DEPENDENCIES----------#
from django import forms
from .models import Score, Event
# from players.models import Player # COMMENTED OUT BC-
#(using player names in score form but treating player and teamate as plain charfields, not as model-bound fields)

#---------IMPORT DEPENDENCIES----------#



# ----------------------------------------Score form------------------------------------#
class ScoreForm(forms.ModelForm): # Results/#/Leaderboard/addNewScore form
    player = forms.CharField(
        label='Player',
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'}) # This enables the autocomplete suggestions
    )
    teammate = forms.CharField(
        label='Teammate',
        required=False,
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'}) # Matches an HTML <datalist> element
    )

    # META is a INNER class in DJANGO used to store CONFIGURATION for things like: 
    # forms, widgets, models & even serializers
    class Meta:         
        model = Score       # Telling DJANGO I want to use the SCORE model, 
        fields = ['score']  # but ONLY include the SCORE field, (not all)
                            # since the user MANUALLY CUSTOMIZES these fields, they are not included here
# ----------------------------------------Score form------------------------------------#




# -----------------------------Event form-----------------------------------------------#
class EventForm(forms.ModelForm): # /tourResults/createNewEvent form
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