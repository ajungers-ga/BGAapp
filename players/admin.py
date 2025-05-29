# File Purpose: Admin configuration for the PLAYERS app in the BGA Tour Tracker
# This file registers the PLAYER model so it can be managed via the Django Admin Panel
# - Allows me to view, add, or edit player info manually
# - Useful for debugging name typos or adding players who weren’t created through the form

#---------IMPORT DEPENDENCIES----------#
from django.contrib import admin
from .models import Player
#---------IMPORT DEPENDENCIES----------#

# ------------------------PlayerAdmin Class-----------------------------#
# Registers the PLAYER model with the admin panel using modern decorator syntax
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'nickname')  # Show useful columns
    search_fields = ('first_name', 'last_name')             # Add a search bar
    ordering = ('last_name', 'first_name')                  # Sort alphabetically by last name
# ------------------------PlayerAdmin Class-----------------------------#
