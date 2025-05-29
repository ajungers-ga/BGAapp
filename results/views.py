# File Purpose: View logic for the RESULTS section of the BGA Tour Tracker
# This file powers the Tour Results, Schedule, Leaderboard, Score Entry/Edit, and Event Management
# Views connect to: Event, Score, and Player models
# Forms: EventForm and ScoreForm
# Templates: event_list.html, schedule.html, leaderboard.html, event_form.html, event_confirm_delete.html, edit_score.html
# Special logic: handles custom leaderboard sorting, placement logic, and to_par calculations

#-----------------IMPORT DEPENDENCIES-------------------------------------#
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, Score
from .forms import EventForm, ScoreForm
from players.models import Player
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
#-------------------------------------------------------------------------#
# POST PRESENTATION, PRE LAUNCH (1.1)
class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# POST PRESENTATION, PRE LAUNCH (2.1)
def superuser_only(user):
    return user.is_superuser

# 1. SCHEDULE VIEW (Public)
def schedule_view(request):
    today = timezone.now().date()
    events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request, 'bgaapp/schedule.html', {'events': events})

# 2. EVENT LIST VIEW (Superuser Only)
class EventListView(ListView):
    model = Event
    template_name = 'bgaapp/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        # Sort events by descending date (newest to oldest)
        return Event.objects.order_by('-date')

    def get_context_data(self, extra_context=None):
        context = super().get_context_data()
        context['form'] = EventForm()
        return context

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('event_list')

# 3. EVENT UPDATE VIEW (Superuser Only)
class EventUpdateView(AdminOnlyMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'bgaapp/event_form.html'
    success_url = reverse_lazy('event_list')

# 4. EVENT DELETE VIEW (Superuser Only)
class EventDeleteView(AdminOnlyMixin, DeleteView):
    model = Event
    template_name = 'bgaapp/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

# 5. LEADERBOARD VIEW (Public Read, Superuser Create)
def leaderboard_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    scores = event.scores.order_by('score')

    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden("Access denied.")

        form = ScoreForm(request.POST)
        if form.is_valid():
            score_entry = form.save(commit=False)
            player_name = form.cleaned_data['player']
            teammate_name = form.cleaned_data.get('teammate')
            third_name = form.cleaned_data.get('third_player')
            fourth_name = form.cleaned_data.get('fourth_player')
            valid = True

            try:
                first, last = player_name.strip().split(" ", 1)
                score_entry.player = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
            except (ValueError, Player.DoesNotExist):
                form.add_error('player', f"No player found for '{player_name}'.")
                valid = False

            if teammate_name:
                try:
                    first, last = teammate_name.strip().split(" ", 1)
                    score_entry.teammate = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                except (ValueError, Player.DoesNotExist):
                    form.add_error('teammate', f"No player found for '{teammate_name}'.")
                    valid = False
            else:
                score_entry.teammate = None

            if third_name:
                try:
                    first, last = third_name.strip().split(" ", 1)
                    score_entry.third_player = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                except (ValueError, Player.DoesNotExist):
                    form.add_error('third_player', f"No player found for '{third_name}'.")
                    valid = False
            else:
                score_entry.third_player = None

            if fourth_name:
                try:
                    first, last = fourth_name.strip().split(" ", 1)
                    score_entry.fourth_player = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                except (ValueError, Player.DoesNotExist):
                    form.add_error('fourth_player', f"No player found for '{fourth_name}'.")
                    valid = False
            else:
                score_entry.fourth_player = None

            if not valid:
                return render(request, 'bgaapp/leaderboard.html', {
                    'event': event,
                    'scores': scores,
                    'form': form,
                    'all_players': Player.objects.all()
                })

            score_entry.event = event
            score_entry.to_par = score_entry.score - 72
            score_entry.save()

            # Update placement logic after score is saved
            ordered_scores = event.scores.order_by('score')
            placement = 1
            last_score = None
            actual_placement = 1

            for s in ordered_scores:
                if last_score is not None and s.score == last_score:
                    s.placement = f"{placement}"
                else:
                    placement = actual_placement
                    s.placement = f"{placement}"
                s.save()
                last_score = s.score
                actual_placement += 1

            return redirect('leaderboard', pk=event.pk)
    else:
        form = ScoreForm()

    # FINALIZED EVENT LOGIC - CALCULATE WINS
    if event.finalized:
        tied_winners = scores.filter(placement='1')
        if tied_winners.exists():
            num_tied_teams = tied_winners.count()
            win_share = round(1.0 / num_tied_teams, 2)

            for score in tied_winners:
                for player in [score.player, score.teammate, score.third_player, score.fourth_player]:
                    if player:
                        player.career_wins += win_share
                        player.save()

        # Mark event played for all players
        for score in scores:
            for player in [score.player, score.teammate, score.third_player, score.fourth_player]:
                if player:
                    player.career_events_played += 1
                    player.save()

    return render(request, 'bgaapp/leaderboard.html', {
        'event': event,
        'scores': scores,
        'form': form,
        'all_players': Player.objects.all()
    })

# 6. EDIT SCORE VIEW (Superuser Only)
@user_passes_test(superuser_only)
@require_http_methods(["GET", "POST"])
def edit_score_view(request, score_id):
    # (unchanged from your version)
    ...
    
# 7. DELETE SCORE VIEW (Superuser Only)
@user_passes_test(superuser_only)
def delete_score(request, pk):
    # (unchanged from your version)
    ...
