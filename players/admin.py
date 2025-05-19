# File Purpose: Admin configuration for the PLAYERS app in the BGA Tour Tracker
# This file registers the PLAYER model so it can be managed via the Django Admin Panel
# - Allows me to view, add, or edit player info manually
# - Useful for debugging name typos or adding players who weren’t created through the form




#---------IMPORT DEPENDENCIES----------#
from django.contrib import admin
from .models import Player
#---------IMPORT DEPENDENCIES----------#




# ------------------------PlayerAdmin Class-----------------------------#
# Registers the PLAYER model with the admin panel
# This version uses the TRADITIONAL style instead of a PYTHON DECORATOR
# After presentation, I plan to swap this out for @admin.register(Player) for consistency across the admin page

# @admin.register(Player)                   TO BE IMPLEMENTED POST PRESENTATION
# class PlayerAdmin(admin.ModelAdmin):      TO BE IMPLEMENTED POST PRESENTATION


admin.site.register(Player)
# ------------------------PlayerAdmin Class-----------------------------#