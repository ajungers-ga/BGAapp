# File Purpose: View logic for the RESULTS section of the BGA Tour Tracker
# This file powers the Tour Results, Schedule, Leaderboard, Score Entry/Edit, and Event Management
# Views connect to: Event, Score, and Player models
# Forms: EventForm and ScoreForm
# Templates: event_list.html, schedule.html, leaderboard.html, event_form.html, event_confirm_delete.html, edit_score.html
# Special logic: handles custom leaderboard sorting, placement logic, and to_par calculations

# Why use reverse_lazy?
# Same as players/views — since class based views are loaded at import time, 
# reverse_lazy delays the URL resolution until the view is used

# View Order from top down:
# (line34) 1. schedule_view         (Upcoming Events Page)
# (line60) 2. EventListView         (List + Create Events)
# 3. EventUpdateView       (Edit Event)
# 4. EventDeleteView       (Delete Event)
# 5. leaderboard_view      (Leaderboard + Add Score)
# 6. edit_score_view       (Edit Score)
# 7. delete_score          (Delete Score from Event)

#-------------------------------IMPORT DEPENDENCIES--------------------------------#
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, Score
from .forms import EventForm, ScoreForm
from django.views.decorators.http import require_http_methods
from players.models import Player
from django.db.models import Q
#-------------------------------IMPORT DEPENDENCIES--------------------------------#


#---------------------------- 1. SCHEDULE VIEW (Upcoming Events Page) ----------------------------#
def schedule_view(request):
    # schedule_view is a FUNCTION 
    # request = the incoming HTTP GET request from the browser

    today = timezone.now().date()
    # timezone.now() = DJANGOS timezone aware FUNCTION for getting the current date and time
    # .date() = a METHOD to extract just the DATE portion (ignores time) — used for comparing to Event dates

    events = Event.objects.filter(date__gte=today).order_by('date')
    # Event.objects = access all records in the Event model using DJANGO ORM (to interact with DB using PYTHING instead of SQL)
    # .filter - narrows down the query set from all events 
    # date__gte? -underscores are DJANGO way of CHAINING look up - (lookup MODIFIER meaning greater than or equal to)
    # .order_by('date') = sorts those future events in ascending order (soonest first)
    # why the . before order_by? - This is standard PYTHON syntax for calling a METHOD ON AN OBJECT

    return render(request, 'bgaapp/schedule.html', {'events': events})
    # Renders the HTML template at templates/bgaapp/schedule.html
    # Context = passing a dictionary with one key: 'events' — which will be looped through in the template
    
# "hey DJANGO,can you take schedule.html template and give it the EVENTSdata so it can be displayed? thanks, alex"
#--------------------------------------------------------------------------------------------------#




#---------------------------- 2. EVENT LIST VIEW (All Events + Create Form) ----------------------------#
class EventListView(ListView):
    model = Event
    # model = This view is tied to the EVENT model — it will load ALL EVENT objects from the DB

    template_name = 'bgaapp/event_list.html'
    # template_name = This is the HTML file used to show the full event list + form

    context_object_name = 'events'
    # context_object_name = Tells DJANGO to send the EVENT list to the template using the variable name 'events'
    # Without this line, the variable would default to 'object_list' in the template


    # BELOW = Customizing the context so the page ALSO includes the EVENT CREATION FORM at the top
    def get_context_data(self, extra_context=None):
        # self = PYTHONS reference to the current instance of this class (EventListView)
        # extra_context = Optional — used by DJANGO if additional template variables are passed in

        context = super().get_context_data()
        # super() = built in PYTHON FUNCTION, calls the parents class METHOD
        # in this case, EventListView INHERITS from ListView and want to run its built in .get_context_data() before adding our new content
        # .get_context_data() = DJANGO METHOD that builds the CONTEXT DICTIONARY for templates
        # Now I can add my EVENTFORM() after DJANGO runs the default logic for this view first
        
        context['form'] = EventForm()
        # This manually adds a NEW blank instance of EventForm to the context DICTIONARY    
        # Key name = form - so in the template I can just write {{ form }} and DJANGO will render the whole form
        # This is what powers the “Create New Event” form at the top of the Tour Results page

        return context
        # Return the final context DICTIONARY to the template
        # This now includes both:
        # - EVENTS = the list of all Event objects (from the model)
        # - form = a blank EventForm instance used to create new events
        # This makes both available to the event_list.html page via {{ events }} and {{ form }}



    # BELOW = Handle POST requests when someone submits the "Create Event" form
    # When I say someone, i mean me, and it will be done through the admin portal post presentation 
    def post(self, request):
        # def = defines a METHOD (post)
        # inside this class (this will run when a POST request is made)
        # self = PYTHONS reference to the current instance of this class (EventListView)
        # request = the incoming POST request triggered by the HTML form submission

        form = EventForm(request.POST)
        # Create a new instance of the EventForm using the submitted form data
        # request.POST = contains all the text based input fields from the form

        if form.is_valid():
            form.save()  
            # If the form passes DJANGOS built in validation, save it to the database
            # This creates a brand new Event object from the user input

        else:
            print("event form errors:", form.errors)
            # If the form doesn’t pass validation, print out the specific errors in the terminal
            # (Note: these errors are not shown in the template — just for debugging right now)

        return redirect('event_list')
        # After form is processed (whether valid or not), redirect back to the main Event list page
        # Prevents duplicate submissions if the user refreshes
        # 'event_list' refers to the named URL route from results/urls.py
        
#---------------------------- 2. EVENT LIST VIEW (All Events + Create Form) ----------------------------#  






#---------------------------- 3. EVENT UPDATE VIEW (Edit Existing Event) ----------------------------#
class EventUpdateView(UpdateView):
    model = Event
    # model = This view is tied to the EVENT model — it knows we’re editing an existing Event instance

    form_class = EventForm
    # form_class = Tells DJANGO to use my custom EventForm (from forms.py)
    # This is the same form class I used when creating a new event — now reused for editing

    template_name = 'bgaapp/event_form.html'
    # template_name = The HTML file that displays the edit form (same template used for create/edit)
    # Template will automatically populate with the selected Event’s current data

    success_url = reverse_lazy('event_list')
    # success_url = After saving the edited Event, redirect to the Event List page
    # reverse_lazy = delays URL resolution until the view is used at runtime
    # This avoids circular import issues (why it's better than reverse() inside class-based views)

#---------------------------- 3. EVENT UPDATE VIEW (Edit Existing Event) ----------------------------#



#---------------------------- 4. EVENT DELETE VIEW (Confirm & Delete Event) ----------------------------#
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'bgaapp/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')  # go back to list after deletion
#--------------------------------------------------------------------------------------------------#


#---------------------------- 5. LEADERBOARD VIEW (View + Add Scores) ----------------------------#
def leaderboard_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    scores = event.scores.order_by('score')

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_entry = form.save(commit=False)

            player_name = form.cleaned_data['player']
            teammate_name = form.cleaned_data['teammate']
            valid = True

            # Try to match typed name to Player model
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

            # Recalculate placements after score added
            ordered_scores = event.scores.order_by('score')
            placement = 1
            last_score = None
            actual_placement = 1

            for s in ordered_scores:
                if last_score is not None and s.score == last_score:
                    s.placement = f"{placement}"  # same as previous
                else:
                    placement = actual_placement
                    s.placement = f"{placement}"
                s.save()
                last_score = s.score
                actual_placement += 1

            return redirect('leaderboard', pk=event.pk)

    else:
        form = ScoreForm()

    return render(request, 'bgaapp/leaderboard.html', {
        'event': event,
        'scores': scores,
        'form': form,
        'all_players': Player.objects.all()
    })
#--------------------------------------------------------------------------------------------------#


#---------------------------- 6. EDIT SCORE VIEW (Edit Submitted Score) ----------------------------#
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

            # Recalculate placements
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
        form = ScoreForm(instance=score)

    return render(request, 'bgaapp/edit_score.html', {
        'form': form,
        'score': score,
        'event': event
    })
#--------------------------------------------------------------------------------------------------#


#---------------------------- 7. DELETE SCORE VIEW (Remove a Score + Recalculate) ----------------------------#
def delete_score(request, pk):
    score = get_object_or_404(Score, pk=pk)
    event = score.event
    score.delete()

    # Recalculate placements after deletion
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
#--------------------------------------------------------------------------------------------------#
