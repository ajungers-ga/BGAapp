# File Purpose = This file defines the views (functions responding to user requests) \
# for the Tour Results section of BGAapp

# These views allow users to:
# - View all events
# - Create new events
# - Edit or delete existing events
# This connects to the Event model (models.py), the EventForm (forms.py), and template files inside templates/bgaapp/.

# ------IMPORTS BELOW -------#
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, Player, Score
from .forms import EventForm, ScoreForm
from django.views.decorators.http import require_http_methods
from players.models import Player
from django.db.models import Q
#-------IMPORTS ABOVE-----------#


# BELOW = Display only upcoming events sorted by date--------------------# 
def schedule_view(request):
    today = timezone.now().date()
    events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request, 'bgaapp/schedule.html', {'events': events})
#-----------------------------------------------------------------------#


# BELOW = List all events and show a form to add a new one-----------------------------------------------------------#
class EventListView(ListView):
    model = Event
    template_name = 'bgaapp/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, extra_context=None):
        context = super().get_context_data()
        context['form'] = EventForm()
        return context

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("event form errors:", form.errors)
        return redirect('event_list')
#-----------------------------------------------------------------------------------------------------------------------#


# Edit an existing event------------------------------------------------------------------------------------#
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'bgaapp/event_form.html'
    success_url = reverse_lazy('event_list')
#-----------------------------------------------------------------------------------------------------------#


# Delete an event-------------------------------------------------------------------------------------------#
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'bgaapp/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')
#-----------------------------------------------------------------------------------------------------------#    


# BELOW = Show leaderboard form + scores for an individual event --------------#
def leaderboard_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    scores = event.scores.order_by('score')

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_entry = form.save(commit=False)

            player_name = form.cleaned_data['player']
            teammate_name = form.cleaned_data['teammate']
            valid = True  # flag to track if both lookups succeed

            # Try to convert PLAYER field into a Player object
            try:
                first, last = player_name.strip().split(" ", 1)
                score_entry.player = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
            except (ValueError, Player.DoesNotExist):
                form.add_error('player', f"No player found for '{player_name}'. Make sure the name matches a known player.")
                valid = False

            # Try to convert TEAMMATE field into a Player object (if filled)
            if teammate_name:
                try:
                    first, last = teammate_name.strip().split(" ", 1)
                    score_entry.teammate = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                except (ValueError, Player.DoesNotExist):
                    form.add_error('teammate', f"No player found for '{teammate_name}'. Make sure the name matches a known player.")
                    valid = False
            else:
                score_entry.teammate = None

            if not valid:
                return render(request, 'bgaapp/leaderboard.html', {
                    'event': event,
                    'scores': scores,
                    'form': form,
                    'all_players': Player.objects.all()
                })

            # All good — save score and update leaderboard
            par = 72
            score_entry.event = event
            score_entry.to_par = score_entry.score - par
            score_entry.save()

            ordered_scores = event.scores.order_by('score')
            for i, s in enumerate(ordered_scores, start=1):
                s.placement = f"{i}"
                s.save()

            return redirect('leaderboard', pk=event.pk)
    else:
        form = ScoreForm()

    return render(request, 'bgaapp/leaderboard.html', {
        'event': event,
        'scores': scores,
        'form': form,
        'all_players': Player.objects.all()
    })
#-------------------------------------------------------------------------------------------#


# BELOW = Edit a submitted score for an event -------------------------------------#
@require_http_methods(["GET", "POST"])
def edit_score_view(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    event = score.event

    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            updated_score = form.save(commit=False)
            updated_score.to_par = updated_score.score - 72
            updated_score.save()

            ordered_scores = event.scores.order_by('score')
            for i, s in enumerate(ordered_scores, start=1):
                s.placement = f"{i}"
                s.save()

            return redirect('leaderboard', pk=event.pk)
    else:
        form = ScoreForm(instance=score)

    return render(request, 'bgaapp/edit_score.html', {
        'form': form,
        'score': score,
        'event': event
    })


# BELOW = function to delete a score, from the /results/score/#/edit page--------------------------------#
def delete_score(request, pk):
    score = get_object_or_404(Score, pk=pk)
    event_id = score.event.pk
    score.delete()
    return redirect('leaderboard', pk=event_id)
#---------------------------------------------------------------------------------------------------------#
