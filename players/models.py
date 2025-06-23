#-------IMPORT DEPENDENCIES-------#
from django.db import models
from decimal import Decimal
from cloudinary_storage.storage import MediaCloudinaryStorage
#-------IMPORT DEPENDENCIES-------#


#----------------------DEFINE THE PLAYER SCHEMA (data fields)-------------------------#
class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, blank=True)
    hometown = models.CharField(max_length=50, blank=True)
    years_active = models.CharField(max_length=20, blank=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='player_images/',
        blank=True,
        null=True
    )

    hof_inducted = models.BooleanField(default=False)
    hof_year = models.PositiveIntegerField(blank=True, null=True)
    accolades = models.TextField(blank=True)

    wins = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))

    def __str__(self):
        return f"{self.first_name} '{self.nickname}' {self.last_name}" if self.nickname else f"{self.first_name} {self.last_name}"

#---------------------------------COMPUTED PROPERTIES-----------------------------------------#

    @property
    def career_events_played(self):
        from results.models import Score
        return Score.objects.filter(
            models.Q(player=self) |
            models.Q(teammate=self) |
            models.Q(third_player=self) |
            models.Q(fourth_player=self)
        ).count()

    @property
    def career_wins(self):
        from results.models import Score
        from collections import defaultdict

        all_scores = Score.objects.filter(event__finalized=True).only(
            'event_id', 'score', 'player_id', 'teammate_id', 'third_player_id', 'fourth_player_id'
        )

        wins = 0.0
        event_scores = defaultdict(list)

        for score in all_scores:
            event_scores[score.event_id].append(score)

        for event_id, scores in event_scores.items():
            if not scores:
                continue

            min_score = min(s.score for s in scores)
            winning_teams = [s for s in scores if s.score == min_score]
            win_fraction = 1.0 / len(winning_teams)

            for s in winning_teams:
                if self.id in [
                    s.player_id,
                    s.teammate_id,
                    s.third_player_id,
                    s.fourth_player_id
                ]:
                    wins += win_fraction
                    break

        return round(wins, 2)

    def get_winning_scores(self):
        from results.models import Score
        from collections import defaultdict

        all_scores = Score.objects.filter(event__finalized=True).select_related('event')
        event_scores = defaultdict(list)

        for score in all_scores:
            event_scores[score.event_id].append(score)

        winning_scores = []

        for event_id, scores in event_scores.items():
            if not scores:
                continue

            min_score = min(s.score for s in scores)
            winning_teams = [s for s in scores if s.score == min_score]

            for s in winning_teams:
                if self.id in [
                    s.player_id,
                    s.teammate_id,
                    s.third_player_id,
                    s.fourth_player_id
                ]:
                    winning_scores.append(s)
                    break

        return winning_scores
