from django.views.generic import ListView, DetailView
from django.db import models
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
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
            career_events_played=Count('scores', distinct=True) +
                                 Count('teammate_scores', distinct=True) +
                                 Count('third_player_scores', distinct=True) +
                                 Count('fourth_player_scores', distinct=True),
            career_wins=(
                Count('scores', filter=Q(scores__placement__in=["1", "1st"]), distinct=True) +
                Count('teammate_scores', filter=Q(teammate_scores__placement__in=["1", "1st"]), distinct=True) +
                Count('third_player_scores', filter=Q(third_player_scores__placement__in=["1", "1st"]), distinct=True) +
                Count('fourth_player_scores', filter=Q(fourth_player_scores__placement__in=["1", "1st"]), distinct=True)
            )
        ).annotate(
            win_percentage=ExpressionWrapper(
                F('career_wins') * 100.0 / F('career_events_played'),
                output_field=FloatField()
            )
        )

        # Sorting logic
        sort = self.request.GET.get('sort', 'career_events_played')
        order = self.request.GET.get('order', 'desc')

        if sort == 'career_wins':
            players = players.order_by(('-' if order == 'desc' else '') + 'career_wins')
        elif sort == 'win_percentage':
            # Filter players with at least 20 events played
            players = players.filter(career_events_played__gte=20).order_by(('-' if order == 'desc' else '') + 'win_percentage')
        else:  # Default to events played
            players = players.order_by('-career_events_played')

        return players

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        per_page = self.paginate_by
        start_rank = (int(page_number) - 1) * per_page + 1
        for idx, player in enumerate(context['object_list'], start=start_rank):
            player.rank = idx
        return context

#------------------------------------------------------------#
