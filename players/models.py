# File Purpose = 
# Create your models here.
from django.db import models
from decimal import Decimal


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, blank=True)
    hometown = models.CharField(max_length=50, blank=True)
    years_active = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)

    # career_events_played = models.PositiveIntegerField(default=0)
    # career_wins = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    
    hof_inducted = models.BooleanField(default=False)
    hof_year = models.PositiveBigIntegerField(blank=True, null=True)
    accolades = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"

    @property
    def career_events_played(self):
        from results.models import Score
        # Get all scores where player was the main or teammate is listed
        return Score.objects.filter(models.Q(player=self) | models.Q(teammate=self)).count()

    @property
    def career_wins(self):
        from collections import defaultdict
        from decimal import Decimal
        from results.models import Score  

        win_total = Decimal("0.0")

        relevant_scores = Score.objects.filter(
            models.Q(player=self) | models.Q(teammate=self),
            placement__in=["1", "1st"]
        ).select_related("event")

        # Group all 1st place scores by event to calculate ties and team shares
        event_to_scores = defaultdict(list)
        for score in Score.objects.filter(placement__in=["1", "1st"]):
            event_to_scores[score.event_id].append(score)

        for score in relevant_scores:
            tied_scores = event_to_scores[score.event_id]
            tie_count = len(tied_scores)

            # Skip if something is off
            if tie_count == 0:
                continue

            # Divide win evenly among all 1st place scores (accounts for ties automatically)
            win_share = Decimal("1.0") / Decimal(tie_count)
            win_total += win_share

        return win_total.quantize(Decimal("0.01"))