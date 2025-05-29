# File Purpose:
# This file defines the PLAYER model for BGA Tour Tracker.
# It stores player profile data and EXPOSES CUSTOM LOGIC for career stats
# such as events played and wins, based on results in the Score model.

# 1.  Defines the PLAYER SCHEMA (data Fields)
# 2.1 Controls how PLAYERS are displayed using __str__ - method determines what shows up when a player is referenced
# 2.2 in the admin panel, debug logs, template loops, drop downs
# 3.  Provides custom properties for dynamic stats (@property methods update the stats in the score model)
# 4. Links to other models (score.player, score.teammate, score.event)

# The players/models.py is the definintion of what a player is, how they appear on the page and how to calc their stats from the DB


#-------IMPORT DEPENDENCIES-------#
from django.db import models
from decimal import Decimal
from cloudinary_storage.storage import MediaCloudinaryStorage

#-------IMPORT DEPENDENCIES-------#


#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#
class Player(models.Model):
    first_name = models.CharField(max_length=20)                                 # String, REQUIRED
    last_name = models.CharField(max_length=20)                                  # String, REQUIRED
    nickname = models.CharField(max_length=50, blank=True)                       # String, optional *Keep this? Maybe add logic to show first name OR nickname?*
    hometown = models.CharField(max_length=50, blank=True)                       # String, optional
    years_active = models.CharField(max_length=20, blank=True)                   # String, optional *Keep this? Maybe rework this to show rookie season*
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='player_images/',
        blank=True,
        null=True
    )

    hof_inducted = models.BooleanField(default=False)                            # Boolean (true/false) - shows IF a player is in the hall of fame
    hof_year = models.PositiveIntegerField(blank=True, null=True)                # Integer, must be positive. Perfect for representing a Year. Had the BGA been running for 3000 years I would have used the generic IntegerField()
    accolades = models.TextField(blank=True)                                     # NEEDS WORK (1. Create Awards app. 2. Dynamically link Award (from year) to profile page?)

    wins = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))  # New field to store win total directly
#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#



    # String representation for Player objects (used in admin, dropdowns, and logs)
    # If the player has a nickname, format as: First 'Nickname' Last (this has become annoying when adding players to an event)
    # Otherwise, just return: First Last
    # Considering reworking this logic or even removing nicknames all together. 
    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"



#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
    @property # This is a PYTHON DECORATOR that lets me call a METHOD like an attribute. (read only) Using it to dynamically calulate fields w/o storing them in the DB
    def career_events_played(self):
        from results.models import Score
        # Count total number of events this player has participated in
        # A player can appear as the main player OR as the teammate
        return Score.objects.filter(models.Q(player=self) | models.Q(teammate=self)).count()

    @property
    def career_wins(self):
        # New logic: return the stored `wins` value, dynamically
        return self.wins
#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
