# File Purpose:
# This file defines the PLAYER model for BGA Tour Tracker.
# It stores player profile data and EXPOSES CUSTOM LOGIC for career stats
# such as events played and wins, based on results in the Score model.

# 1.  Defines the PLAYER SCHEMA (data Fields)
# 2.1 Controls how PLAYERS are displayed using __str__ - method determines what shows up when a player is referenced
# 2.2 in the admin panel, debug logs, template loops, drop downs
# 3.  Provides custom properties for dynamic stats (@property methods update the stats in the score model)
# 4. Links to other models (score.player, score.teammate, score.event)

# The players/models.py is the definition of what a player is, how they appear on the page and how to calc their stats from the DB

#-------IMPORT DEPENDENCIES-------#
from django.db import models
from decimal import Decimal
from cloudinary_storage.storage import MediaCloudinaryStorage
#-------IMPORT DEPENDENCIES-------#

#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#
class Player(models.Model):
    first_name = models.CharField(max_length=20)                                 # String, REQUIRED
    last_name = models.CharField(max_length=20)                                  # String, REQUIRED
    nickname = models.CharField(max_length=50, blank=True)                       # String, optional
    hometown = models.CharField(max_length=50, blank=True)                       # String, optional
    years_active = models.CharField(max_length=20, blank=True)                   # String, optional
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='player_images/',
        blank=True,
        null=True
    )

    hof_inducted = models.BooleanField(default=False)                            # Boolean (true/false)
    hof_year = models.PositiveIntegerField(blank=True, null=True)                # Integer (positive, for year)
    accolades = models.TextField(blank=True)                                     # Long-form text for awards or shoutouts
#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#


    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"



#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
    @property
    def career_events_played(self):
        from results.models import Score
        return Score.objects.filter(models.Q(player=self) | models.Q(teammate=self)).count()

    @property
    def career_wins(self):
        from results.models import Score
        # Return number of wins this player was part of (solo or team)
        return Score.objects.filter(
            models.Q(player=self) | models.Q(teammate=self),
            placement__in=["1", "1st"]
        ).count()
#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
