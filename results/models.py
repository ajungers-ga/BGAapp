# File Pupose: Defines the Event and Score models for BGA Tour Tracker.
# These models represent all tournament-level data, including team/solo format,
# majors, dates, scorecards, placements, and relationships to Players.

#-------IMPORT DEPENDENCIES-------#
from django.db import models
from players.models import Player # import the PLAYER model to link scores to users
#-------IMPORT DEPENDENCIES-------#


# -----Event Model - defines a tournament----------------------------------------------------------------------#
class Event(models.Model):
    EVENT_TYPES = [
    ('2-Man Scramble', '2-Man Scramble'),
    ('4-Man Scramble', '4-Man Scramble'),
    ('Major Tournament', 'Major Tournament'),
]
    # Specific LABELS for MAJOR TOURNAMENTS
    MAJOR_CHOICES = [
    ('BGA Masters', 'BGA Masters'),
    ('BGA Championship', 'BGA Championship'),
    ('BGA US Open', 'BGA US Open'),
    ('BGA British Open', 'BGA British Open'),
]

    # 1. What kind of event is this?
    name = models.CharField(max_length=50, choices=EVENT_TYPES, default='2-Man Scramble')
    # 2. When was it played?
    date = models.DateField()
    # 3. Where was it played?
    course_name = models.CharField(max_length=100)
    # 4. Is this a team event?
    is_team_event = models.BooleanField(default=True)
    # 5. Are there any OPTIONAL notes for the event?
    notes = models.TextField(blank=True)
    # 6. Which BGA Season/year does this event belong to?
    season = models.PositiveIntegerField(default=2024)
    # 7. Is this a MAJOR TOURNAMENT?
    is_major = models.BooleanField(default=False)
    # 8. If this is a MAJOR, which one?
    major_label = models.CharField(
    max_length=50,
    choices=MAJOR_CHOICES,
    blank=True,
    )
    # 9. Once all thescores are entered, finialize this event to lock in medals and stats
    finalized = models.BooleanField(default=False, help_text="Mark this event as finalized to lock stats and show medals.")
    # 10. Display this event in a readable format
    def __str__(self):
        return f"{self.name} at {self.course_name} on {self.date}"
#-----------------------------------------------EVENT MODEL-----------------------------------------------------#

# EVENT and SCORES are a 1 to many relationship. 
# The EVENT is the tournament and the SCORE is one row on that leaderboard event
# Since they are tied together, it makes sense to define them side by side in the same models.py folder

#----------Score Model (defines one player or teams score in a given event)-------------------------------------#
# ----------Score Model (defines one player or team's score in a given event)------------------------------- #
class Score(models.Model):
    # 1. The Event this score belongs to (foreign key relationship)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='scores')
    # 2. The primary PLAYER being scored (always required)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scores')
    # 3. The teammate, if this was a team event (optional)
    teammate = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,  # If teammate is deleted, don't delete the score — just set to null
        blank=True,
        null=True,
        related_name='teammate_scores'
    )
    # 4. The raw score for this player/team (like 69.00)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    # 5. The score in relation to par (like -3.00)
    to_par = models.DecimalField(max_digits=5, decimal_places=2)
    # 6. The final placement for this score (like "1", "2nd", "T-3")
    placement = models.CharField(max_length=20, blank=True)
    # 7. Show a readable label in admin/debug/console
    def __str__(self):
        label = self.event.major_label if self.event.is_major and self.event.major_label else self.event.name
        return f"{self.player} - {self.score} in {label} on {self.event.date}"
# ----------------------------------------------------SCORE MODEL------------------------------------------------ #

    
