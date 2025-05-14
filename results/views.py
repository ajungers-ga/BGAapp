# File Purpose = This file defines the views (functions responding to user requests) \
# for the Tour Results section of BGAapp

# These views allow users to:
# - View all events
# - Create new events
# - Edit or delete existing events
# This connects to the Event model (models.py), the EventForm (forms.py), and template files inside templates/bgaapp/.


# ------IMPORTS BELOW -------#
from django.shortcuts import render, redirect, get_object_or_404
# ABOVE = manUally redirect users after a form is submitted so theyre not stuck at deadlink

from django.views.generic import ListView, UpdateView, DeleteView, DetailView
# ABOVE = Built in class views that make it easier to: List items, Edit Items & Delete items

from django.urls import reverse_lazy # refer to a URL by name insead of hardcoding - redirect after edit/delete
from django.utils import timezone # using timezone for getting todays date and specific local time (scheduled_view)
from .models import Event # importing the EVENT model, so it can be used in views
from .forms import EventForm, ScoreForm # importing the form connected to the event model, used for create & edit

from .models import Score  
from django.views.decorators.http import require_http_methods
#-------IMPORTS ABOVE-----------#





# BELOW = Display only upcoming events sorted by date--------------------# 

def schedule_view(request):
    today = timezone.now().date()  # Get today's date
    events = Event.objects.filter(date__gte=today).order_by('date')  # only future events, sorted soonest to latest
    return render(request, 'bgaapp/schedule.html', {'events': events})
#-----------------------------------------------------------------------#






# BELOW = List all events and show a form to add a new one-----------------------------------------------------------#
class EventListView(ListView):
    model = Event # telling Django which model
    template_name = 'bgaapp/event_list.html'
    context_object_name = 'events' # the name used in the template to access all events

    # When the page loads (user GET request)
    def get_context_data(self, extra_context=None):
        context = super().get_context_data() # super refers to parent class(listview) now I can reuse default logic
        context['form'] = EventForm() # form to be filled and returned by user
        return context

    # when the user submits form (user POST request)
    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save() # if form filled out properly, save the event to the DB
        else:
            print("event form errors:", form.errors)    
        return redirect('event_list') # sending the user back to the Event List page
#-----------------------------------------------------------------------------------------------------------------------#





# Edit an existing event------------------------------------------------------------------------------------#
class EventUpdateView(UpdateView):
    model = Event  # telling Django which model
    form_class = EventForm  # use the same form as the create view
    template_name = 'bgaapp/event_form.html'  # page where the edit form will be displayed
    success_url = reverse_lazy('event_list')  # after saving, redirect user back to the Event List page
#-----------------------------------------------------------------------------------------------------------#



# Delete an event-------------------------------------------------------------------------------------------#
class EventDeleteView(DeleteView):
    model = Event  # tell Django which model to delete from
    template_name = 'bgaapp/event_confirm_delete.html'  # confirmation page
    success_url = reverse_lazy('event_list')  # after deletion, send user back to the Event List page
#-----------------------------------------------------------------------------------------------------------#    









#---- Why I decided to use get_object_or_404 BELOW ------ #
# - I want to avoid DJANGO raising a DOES NOT EXIST error if the event does not exist.
# - By using it in LEADERBOARD_VIEW - it tries to get the event from the database using its primary key...
# ... the database only holds the primary keys of EVENTS ALREADY CREATED...
# - This way, the user has to CREATE the event using the CRUD or API call BEFORE accessing the LEADERBOARD_VIEW
# - Instead of crashing the app, we just display the 404 page not found
#--------------------------------------------------------------------------------#

# BELOW = Show leaderboard form + scores for an individual event --------------#
def leaderboard_view(request, pk):
    event = get_object_or_404(Event, pk=pk)  # load the event using primary key
    scores = event.scores.order_by('score')  # order by lowest score first

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_entry = form.save(commit=False)
            score_entry.event = event

            # relative to par 72
            par = 72
            score_entry.to_par = score_entry.score - par
            score_entry.save()





#------------BELOW update placement across leaderboard after new entry is added--------------#           
#------------------------------ Notes for ORDERED_SCORES BELOW ------------------------------#
            # i = current position in list, starting from one--> start=1
            # s represents SCORE OBJECT
            # enumerate is a PYTHON FUNCTION that allows the...
            # looping over a LIST & get the INDEX (position) of all items @sametime
            
            # so im taking the all of the scores and ordering from lowest score to higheest score
            # S.PLACEMENT = then im setting the placement field on the SCORE OBJECT using...
            # f"{i}" ... and FSTRING to embed that OBJECT, 
            # so i = 1 (which stores "1" in the placement field and so on through the leaderboard 2,3,4,5 etc)
            
            # Then im saving the SCORE OBJECT
            
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
        'form': form
    })
#-------------------------------------------------------------------------------------------#
# BELOW = Edit a submitted score for an event -------------------------------------#
# Purpose:
# - Allows editing an individual Score using its ID
# - Automatically recalculates to_par and reorders leaderboard placements
# - Reuses the same ScoreForm used on the leaderboard page
# - After saving, redirects back to the same leaderboard page

# BELOW = Edit a submitted score for an event
@require_http_methods(["GET", "POST"])
def edit_score_view(request, score_id):
    score = get_object_or_404(Score, id=score_id)  # get the score object using primary key
    event = score.event  # link back to the event it belongs to

    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)  # pass in instance to prefill existing score
        if form.is_valid():
            updated_score = form.save(commit=False)
            updated_score.to_par = updated_score.score - 72  # recalculate to_par
            updated_score.save()

            # update placement based on new scores
            ordered_scores = event.scores.order_by('score')
            for i, s in enumerate(ordered_scores, start=1):
                s.placement = f"{i}"
                s.save()

            return redirect('leaderboard', pk=event.pk)  # go back to leaderboard
    else:
        form = ScoreForm(instance=score)  # load form with current data for editing

    return render(request, 'bgaapp/edit_score.html', {
        'form': form,
        'score': score,
        'event': event
    })
#-------------------------------------------------------------------------------------------#




# BELOW = function to delete a score, from the /results/score/#/edit page--------------------------------#
def delete_score(request, pk):          # get the SCORE OBJECT from the DB using primarykey f/ url
    score = get_object_or_404(Score, pk=pk)   # if the SCORE OBJECT does not existm throw 404 error
    event_id = score.event.pk  # saving the EVENT ID linked to this OBJECT SCORE,  before deleting, (link back to that objscore in return)
    score.delete() # now that the event_id has been found, saved, its safe to delete (CONSIDER A CONFIRM MESSAGE???)
    return redirect('leaderboard', pk=event_id) # returning to the leaderboard, linked from earlier, user wont stay on brkn page
#---------------------------------------------------------------------------------------------------------#