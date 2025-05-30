from django.views.generic import ListView, DetailView
from django.db import models
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce, NullIf
from .models import Player
from results.models import Score

#-------------------------------------------#
class PlayerListView(ListView):
    model = Player
    template_name = 'bgaapp/player_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Player.objects.all().prefetch_related(
            'scores',
            'teammate_scores',
            'third_player_scores',
            'fourth_player_scores'
        )
#---------------------------------------------#

#-----------------------------------------------------#
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()
        context['event_wins'] = Score.objects.filter(
            (
                models.Q(player=player) |
                models.Q(teammate=player) |
                models.Q(third_player=player) |
                models.Q(fourth_player=player)
            ),
            placement__in=["1", "1st"]
        ).select_related("event")
        return context
#------------------------------------------------------------#

#------------------------------------------------------------#
class PlayerStatsView(ListView):
    model = Player
    template_name = 'bgaapp/player_stats.html'
    paginate_by = 25

    def get_queryset(self):
        players = Player.objects.all().prefetch_related(
            'scores',
            'teammate_scores',
            'third_player_scores',
            'fourth_player_scores'
        ).annotate(
            events_played=(
                Count('scores__event', distinct=True) +
                Count('teammate_scores__event', distinct=True) +
                Count('third_player_scores__event', distinct=True) +
                Count('fourth_player_scores__event', distinct=True)
            ),
            career_wins=(
                Coalesce(Count('scores', filter=Q(scores__placement__in=["1", "1st"]), distinct=True), 0) +
                Coalesce(Count('teammate_scores', filter=Q(teammate_scores__placement__in=["1", "1st"]), distinct=True), 0) +
                Coalesce(Count('third_player_scores', filter=Q(third_player_scores__placement__in=["1", "1st"]), distinct=True), 0) +
                Coalesce(Count('fourth_player_scores', filter=Q(fourth_player_scores__placement__in=["1", "1st"]), distinct=True), 0)
            )
        ).annotate(
            win_percentage=ExpressionWrapper(
                F('career_wins') * 100.0 / Coalesce(NullIf(F('events_played'), 0), 1),
                output_field=FloatField()
            )
        ).order_by('-events_played')
        return players
#------------------------------------------------------------#
