# File Purpose:
# Defines the EventForm used to create and edit Event model entries.
# Adds a calendar widget and placeholder to the date field.
# attrs is short for HTML attrbutes, in this case type and placeholder are used

from django import forms
from .models import Score, Event
from players.models import Player

# ------- Score form ------- #
class ScoreForm(forms.ModelForm):
    player = forms.CharField(
        label='Player',
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})
    )
    teammate = forms.CharField(
        label='Teammate',
        required=False,
        widget=forms.TextInput(attrs={'list': 'player-options', 'class': 'form-control'})
    )

    class Meta:
        model = Score
        fields = ['score']

# ------- Event form ------- #
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'  # or ['name', 'date', 'course', 'format', etc.]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control'
            })
        }