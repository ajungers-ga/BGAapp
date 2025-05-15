from django.db import models
from players.models import Player

class Event(models.Model):
    EVENT_TYPES = [
    ('2-Man Scramble', '2-Man Scramble'),
    ('4-Man Scramble', '4-Man Scramble'),
    ('Major Tournament', 'Major Tournament'),
]
    name = models.CharField(max_length=50, choices=EVENT_TYPES, default='2-Man Scramble')
    date = models.DateField()
    course_name = models.CharField(max_length=100)
    is_team_event = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    season = models.PositiveIntegerField(default=2024)
    is_major = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} at {self.course_name} on {self.date}"

class Score(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='scores')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scores')
    teammate = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='teammate_scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    to_par = models.DecimalField(max_digits=5, decimal_places=2)
    placement = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.player} - {self.score} in {self.event.name}"
