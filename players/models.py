# File Purpose:
# This file defines the PLAYER model for BGA Tour Tracker.
# It stores player profile data and EXPOSES CUSTOM LOGIC for career stats
# such as events played and wins, based on results in the Score model.



#-------IMPORT DEPENDENCIES-------#
from django.db import models
from decimal import Decimal
#-------IMPORT DEPENDENCIES-------#


#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#
class Player(models.Model):
    first_name = models.CharField(max_length=20)                                 # String, REQUIRED
    last_name = models.CharField(max_length=20)                                  # String, REQUIRED
    nickname = models.CharField(max_length=50, blank=True)                       # String, optional *Keep this? Maybe add logic to show first name OR nickname?*
    hometown = models.CharField(max_length=50, blank=True)                       # String, optional
    years_active = models.CharField(max_length=20, blank=True)                   # String, optional *Keep this? Maybe rework this to show rookie season*
    image = models.ImageField(upload_to='player_images/', blank=True, null=True) # String, optional NEEDS WORK - Why dont images display properly? tbd
    hof_inducted = models.BooleanField(default=False)                            # Boolean (true/false) - shows IF a player is in the hall of fame
    hof_year = models.PositiveIntegerField(blank=True, null=True)                # Integer, must be positive. Perfect for representing a Year. Had the BGA been running for 3000 years I would have used the generic IntegerField()
    accolades = models.TextField(blank=True)                                     # NEEDS WORK (1. Create Awards app. 2. Dynamically link Award (from year) to profile page?)
#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#

  
  
  
    # String representation for Player objects (used in admin, dropdowns, and logs)
    # If the player has a nickname, format as: First 'Nickname' Last (this has become annoying when adding players to an event)
    # Otherwise, just return: First Last
    # Considering reworking this logic or even removing nicknames all together. 
    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"



#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
    @property # This is a PYTHON DECORATIOR that lets me call a METHOD like an attribute. (read only) Using it to dynamically calulate fields w/o storing them in the DB
    def career_events_played(self):
        from results.models import Score
        # Count total number of events this player has participated in
        # A player can appear as the main player OR as the teammate
        return Score.objects.filter(models.Q(player=self) | models.Q(teammate=self)).count()

    @property
    def career_wins(self):
        from collections import defaultdict
        from decimal import Decimal
        from results.models import Score  

        # Start from 0.0 total wins
        win_total = Decimal("0.0")

        # Step 1: Get all 1st place finishes for this player (solo or team event)
        relevant_scores = Score.objects.filter(
            models.Q(player=self) | models.Q(teammate=self), # Q() is DJANGO query obj ussed for OR logic. (GET ALL SCORES WHERE THE PLAYER IS EITHER THE PLAYER OR TEAMMATE)
            placement__in=["1", "1st"]                       # seperating arguments passed into the filter function
        ).select_related("event")

        # Step 2: Build a DICTIONARY to group ALL 1st place scores by EVENT ID
        event_to_scores = defaultdict(list)
        for score in Score.objects.filter(placement__in=["1", "1st"]):
            event_to_scores[score.event_id].append(score)

        # Step 3: Loop through relevent 1st place finishes for this player (self)
        for score in relevant_scores:
            tied_scores = event_to_scores[score.event_id]     # get all 1st-place scores for this event
            tie_count = len(tied_scores)

            # Skip if something is off (shouldnt happen)
            if tie_count == 0:
                continue

            # Step 4: Divide win evenly among all 1st place scores (accounts for ties automatically)
            win_share = Decimal("1.0") / Decimal(tie_count)
            win_total += win_share

        # Return the final win total, rounded to 2 decimal places. (1 decimal place would have worked, too)
        return win_total.quantize(Decimal("0.01"))
    #---------------------------------COMPUTED PROPERTIES-----------------------------------------#