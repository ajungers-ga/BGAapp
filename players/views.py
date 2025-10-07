from django.views.generic import ListView, DetailView
from django.db import models
import re

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


# --- Strict placement parser (no false positives like "10th") ---
# Matches: 1, 1.0, 1st, T1, T-1, "🥇 1", "1 (Playoff)", "1st place"
_PLACEMENT_RE = re.compile(
    r'^(?:t[-\s]*)?1(?:\.0)?(?:st)?(?:\s*(?:place)?)?(?:\s*\(.*\))?$',
    re.IGNORECASE,
)

def is_first_place(placement) -> bool:
    if placement is None:
        return False
    # Numeric storage (int/float)
    if isinstance(placement, (int, float)):
        try:
            return float(placement) == 1.0
        except Exception:
            return False
    s = str(placement).strip()
    # strip common first-place emojis/trophies that might be prepended
    for sym in ('🥇', '🏆'):
        s = s.replace(sym, '')
    s = s.strip()
    return bool(_PLACEMENT_RE.match(s))


# ----------------------------------------------------- #
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

        # All scores involving this player (any slot on a team)
        scores_for_player = (
            Score.objects.filter(
                models.Q(player=player) |
                models.Q(teammate=player) |
                models.Q(third_player=player) |
                models.Q(fourth_player=player)
            )
            .select_related("event")
        )

        # Winners = rows explicitly marked as first by placement (strict match, includes ties)
        winners = [s for s in scores_for_player if is_first_place(getattr(s, 'placement', None))]

        # Group winners and sort by event date (newest first)
        major_wins = [w for w in winners if getattr(w.event, 'is_major', False)]
        two_man_wins = [
            w for w in winners
            if not getattr(w.event, 'is_major', False)
            and getattr(w, 'teammate_id', None) is not None
            and getattr(w, 'third_player_id', None) is None
        ]
        four_man_wins = [w for w in winners if getattr(w, 'third_player_id', None) is not None]

        major_wins.sort(key=lambda w: w.event.date, reverse=True)
        two_man_wins.sort(key=lambda w: w.event.date, reverse=True)
        four_man_wins.sort(key=lambda w: w.event.date, reverse=True)

        context['major_wins'] = major_wins
        context['two_man_wins'] = two_man_wins
        context['four_man_wins'] = four_man_wins
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
        context['players'] = context['object_list']  # Added to match template variable
        return context
# ------------------------------------------------------------ #
