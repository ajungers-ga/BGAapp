# File Purpose:
# This file defines the PLAYER model for BGA Tour Tracker.
# It stores player profile data and EXPOSES CUSTOM LOGIC for career stats
# such as events played and wins, based on results in the Score model.

# 1.  Defines the PLAYER SCHEMA (data Fields)
# 2.1 Controls how PLAYERS are displayed using __str__ - method determines what shows up when a player is referenced
# 2.2 in the admin panel, debug logs, template loops, drop downs
# 3.  Provides custom properties for dynamic stats (@property methods update the stats in the score model)
# 4. Links to other models (score.player, score.teammate, score.third_player, score.fourth_player)

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


    # 2.1 / 2.2 How the player appears in dropdowns, logs, etc
    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"


#---------------------------------COMPUTED PROPERTIES-----------------------------------------#

    # 3. Events Played (if player appears in any slot)
    @property
    def career_events_played(self):
        from results.models import Score
        return Score.objects.filter(
            models.Q(player=self) |
            models.Q(teammate=self) |
            models.Q(third_player=self) |
            models.Q(fourth_player=self)
        ).count()

    # 4. Wins (accurately detects team participation + avoids inflated counts)
    @property
    def career_wins(self):
        from results.models import Score
        from collections import defaultdict

        # Pull all finalized scores (do NOT prefilter to this player)
        all_scores = Score.objects.filter(event__finalized=True)

        wins = 0.0
        event_scores = defaultdict(list)

        # Group all scores by event
        for score in all_scores:
            event_scores[score.event_id].append(score)

        # Process win credit for each event
        for event_id, scores in event_scores.items():
            if not scores:
                continue

            # Find the best (lowest) score
            min_score = min(s.score for s in scores)
            winning_teams = [s for s in scores if s.score == min_score]
            win_fraction = 1.0 / len(winning_teams)

            for s in winning_teams:
                if self in [s.player, s.teammate, s.third_player, s.fourth_player]:
                    wins += win_fraction
                    break  # avoid double credit

        return round(wins, 2)

#---------------------------------COMPUTED PROPERTIES-----------------------------------------#
