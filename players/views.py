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
        return Player.objects.all().prefetch_related(
            'scores',
            'teammate_scores',
            'third_player_scores',
            'fourth_player_scores'
        ).order_by('-id')
#------------------------------------------------------------#
