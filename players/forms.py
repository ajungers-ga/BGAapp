# File Purpose: Form definitions for the PLAYERS app in the BGA Tour Tracker
# This file defines a custom DJANGO form used to create or update PLAYER profiles.

# - PlayerForm: allows users to enter or edit player data (name, nickname, hometown, HOF status, etc.)
 
# This form pulls all fields from the Player model automatically.
# It is actively used in views like /players/new/ and /players/<id>/edit/




#---------IMPORT DEPENDENCIES----------#
from django import forms
from .models import Player
#---------IMPORT DEPENDENCIES----------#


# ------------------------------Player Form-------------------------------#
class PlayerForm(forms.ModelForm):  # Used in player create/edit views
    class Meta:
        model = Player             # Ties this form to the Player model
        fields = '__all__'         # Includes all fields (first_name, last_name, nickname, etc.)
                                   # Form will render default widgets for each field
# ------------------------------Player Form-------------------------------#96