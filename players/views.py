from django.views.generic import ListView, DetailView
from django.db import models
from django.db.models import Q, Min, F, Subquery, OuterRef
from .models import Player
from results.models import Score


# ------------------------------------------- #
class PlayerListView(ListView):
    model = Player
    template_name = 'bgaapp/player_list.html'
    paginate_by = 25

    def get_queryset(self):
        players = Player.objects.all().prefetch_related(
            'scores',
            'teammate_scores',
            'third_player_scores',
            'fourth_player_scores'
        )
        # Sort players by career_events_played in descending order
        players = sorted(players, key=lambda p: p.career_events_played, reverse=True)
        return players
# --------------------------------------------- #


# ----------------------------------------------------- #
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

        # All scores involving this player (any slot on a team)
        scores_for_player = (
            Score.objects
            .filter(
                Q(player=player) |
                Q(teammate=player) |
                Q(third_player=player) |
                Q(fourth_player=player)
            )
            .select_related("event")
        )

        # For each event, compute the minimum to_par (this mirrors leaderboard winners)
        event_min_subq = (
            Score.objects
            .filter(event=OuterRef('event'))
            .values('event')
            .annotate(min_to_par=Min('to_par'))
            .values('min_to_par')[:1]
        )

        winners_qs = (
            scores_for_player
            .annotate(event_min_to_par=Subquery(event_min_subq))
            .filter(to_par=F('event_min_to_par'))
        )

        # Group winners by event type (keeps your existing sections)
        context['major_wins'] = (
            winners_qs
            .filter(event__is_major=True)
            .order_by('-event__date')
        )

        context['two_man_wins'] = (
            winners_qs
            .filter(event__is_major=False, teammate__isnull=False, third_player__isnull=True)
            .order_by('-event__date')
        )

        context['four_man_wins'] = (
            winners_qs
            .filter(third_player__isnull=False)
            .order_by('-event__date')
        )

        return context
# ------------------------------------------------------------ #


# ------------------------------------------------------------ #
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
        filtered_players = []
        for player in players:
            events_played = player.career_events_played
            wins = player.career_wins
            if events_played > 0:
                player.win_percentage = round((wins / events_played) * 100, 2)
            else:
                player.win_percentage = 0.0
            filtered_players.append(player)

        # Sorting logic
        sort = self.request.GET.get('sort', 'events_played')
        order = self.request.GET.get('order', 'desc')

        if sort == 'career_wins':
            filtered_players.sort(key=lambda p: p.career_wins, reverse=(order == 'desc'))
        elif sort == 'win_percentage':
            filtered_players = [p for p in filtered_players if p.career_events_played >= 20]
            filtered_players.sort(key=lambda p: p.win_percentage, reverse=(order == 'desc'))
        else:
            filtered_players.sort(key=lambda p: p.career_events_played, reverse=True)

        return filtered_players

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        per_page = self.paginate_by
        start_rank = (int(page_number) - 1) * per_page + 1
        for idx, player in enumerate(context['object_list'], start=start_rank):
            player.rank = idx
        context['players'] = context['object_list']  # match template variable
        return context
# ------------------------------------------------------------ #
