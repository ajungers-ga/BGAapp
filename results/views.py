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
from decimal import Decimal

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

            for field_name, player_field in {
                'teammate': teammate_name,
                'third_player': third_name,
                'fourth_player': fourth_name
            }.items():
                if player_field:
                    try:
                        first, last = player_field.strip().split(" ", 1)
                        setattr(score_entry, field_name, Player.objects.get(first_name__iexact=first, last_name__iexact=last))
                    except (ValueError, Player.DoesNotExist):
                        form.add_error(field_name, f"No player found for '{player_field}'.")
                        valid = False
                else:
                    setattr(score_entry, field_name, None)

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

            # Recalculate placements with tie logic
            ordered_scores = list(event.scores.order_by('score'))
            placement = 1
            current_score = None
            actual_place = 1

            for i, s in enumerate(ordered_scores):
                if i == 0:
                    s.placement = str(actual_place)
                elif s.score == current_score:
                    s.placement = str(actual_place)
                else:
                    actual_place = i + 1
                    s.placement = str(actual_place)
                current_score = s.score
                s.save()

            return redirect('leaderboard', pk=event.pk)

    else:
        form = ScoreForm()

    # FINALIZED EVENT LOGIC - apply placements
    if event.finalized:
        all_scores = list(scores)
        if all_scores:
            score_to_place = {}
            current_place = 1
            current_score = None

            for i, s in enumerate(all_scores):
                if i == 0:
                    score_to_place[s.score] = current_place
                elif s.score != current_score:
                    current_place = i + 1
                    score_to_place[s.score] = current_place
                current_score = s.score

            for s in all_scores:
                s.placement = str(score_to_place[s.score])
                s.save()

            # 🟢 No need to manually modify career_wins or events played — they're properties now
            pass

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
    score = get_object_or_404(Score, id=score_id)

    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            updated_score = form.save(commit=False)

            # Re-parse names into Player instances
            def parse_player_name(name_str):
                try:
                    first, last = name_str.strip().split(" ", 1)
                    return Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                except Exception:
                    return None

            updated_score.player = parse_player_name(form.cleaned_data['player'])
            updated_score.teammate = parse_player_name(form.cleaned_data.get('teammate', ''))
            updated_score.third_player = parse_player_name(form.cleaned_data.get('third_player', ''))
            updated_score.fourth_player = parse_player_name(form.cleaned_data.get('fourth_player', ''))

            updated_score.save()
            return redirect('leaderboard', pk=score.event.pk)
    else:
        # Pre-fill the form using instance
        initial_data = {
            'player': f"{score.player.first_name} {score.player.last_name}" if score.player else '',
            'teammate': f"{score.teammate.first_name} {score.teammate.last_name}" if score.teammate else '',
            'third_player': f"{score.third_player.first_name} {score.third_player.last_name}" if score.third_player else '',
            'fourth_player': f"{score.fourth_player.first_name} {score.fourth_player.last_name}" if score.fourth_player else '',
            'score': score.score
        }
        form = ScoreForm(initial=initial_data)

    return render(request, 'bgaapp/edit_score.html', {
        'form': form,
        'score': score
    })




# 7. DELETE SCORE VIEW (Superuser Only)
@user_passes_test(superuser_only)
def delete_score(request, pk):
    score = get_object_or_404(Score, pk=pk)
    event_pk = score.event.pk  # Save event id before deleting
    score.delete()
    return redirect('leaderboard', pk=event_pk)