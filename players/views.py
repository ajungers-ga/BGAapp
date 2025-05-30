
from django.views.generic import ListView, DetailView
from django.db import models
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
        )

        # Calculate additional stats
        for player in players:
            events_played = player.career_events_played
            wins = player.career_wins
            if events_played > 0:
                player.win_percentage = round((wins / events_played) * 100, 1)
            else:
                player.win_percentage = 0.0

        # Sorting logic
        sort = self.request.GET.get('sort', 'events_played')
        order = self.request.GET.get('order', 'desc')

        if sort == 'career_wins':
            players = sorted(players, key=lambda p: p.career_wins, reverse=(order == 'desc'))
        elif sort == 'win_percentage':
            players = sorted(players, key=lambda p: p.win_percentage, reverse=(order == 'desc'))
        else:  # Default to events played
            players = sorted(players, key=lambda p: p.career_events_played, reverse=True)

        return players

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add rank to each player
        page_number = self.request.GET.get('page', 1)
        per_page = self.paginate_by
        start_rank = (int(page_number) - 1) * per_page + 1
        for idx, player in enumerate(context['object_list'], start=start_rank):
            player.rank = idx
        return context
#------------------------------------------------------------#
