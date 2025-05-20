# File Purpose: View logic for the RESULTS section of the BGA Tour Tracker
# This file powers the Tour Results, Schedule, Leaderboard, Score Entry/Edit, and Event Management
# Views connect to: Event, Score, and Player models
# Forms: EventForm and ScoreForm
# Templates: event_list.html, schedule.html, leaderboard.html, event_form.html, event_confirm_delete.html, edit_score.html
# Special logic: handles custom leaderboard sorting, placement logic, and to_par calculations

# Why use reverse_lazy?
# Same as players/views — since class based views are loaded at import time, 
# reverse_lazy delays the URL resolution until the view is used

# /block begins / View Order from top down    / What it shows

# /(line34)     / 1. schedule_view            / (Upcoming Events Page)
# /(line60)     / 2. EventListView            / (List + Create Events)
# /(line132)    / 3. EventUpdateView          / (Edit Event)
# /(line154)    / 4. EventDeleteView          / (Delete Event)
# /(line178)    / 5. leaderboard_view         / (Leaderboard + Add Score)
# /(line369)    / 6. edit_score_view          / (Edit Score)
# /(line445)    / 7. delete_score             / (Delete Score from Event)

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
    # model = Tells DJANGO this view is tied to the EVENT model — we’ll be deleting one Event at a time

    template_name = 'bgaapp/event_confirm_delete.html'
    # template_name = This is the HTML file that shows the confirmation message:
    # “Are you sure you want to delete this event?”
    # Template uses {{ object.name }} and a <form method="post"> to confirm deletion

    success_url = reverse_lazy('event_list')
    # success_url = After deletion, redirect back to the main list of events
    # reverse_lazy = delays the URL resolution until the view runs — safer to use in class based views
    # 'event_list' = refers to the named route from results/urls.py

#---------------------------- 4. EVENT DELETE VIEW (Confirm & Delete Event) ----------------------------#







#---------------------------- 5. LEADERBOARD VIEW (View + Add Scores) ----------------------------#
def leaderboard_view(request, pk):
    # leaderboard_view = A FUNCTION based view that handles BOTH:
    # 1. Showing the current leaderboard (GET request)
    # 2. Adding a new score to that leaderboard (POST request)
    # pk = The primary key of the Event being viewed (passed from the URL)    
    event = get_object_or_404(Event, pk=pk)
        # Look up the Event using its primary key
        # If no Event exists with that pk, show a 404 error page
    scores = event.scores.order_by('score')
        # Get all SCORE objects linked to this EVENT
        # .scores = reverse relationship (Score model has a FK to Event)
        # .order_by('score') = sort scores from lowest to highest (golf style leaderboard)
    

    if request.method == 'POST':
        # If user submitted the form, process the POST request below
        form = ScoreForm(request.POST)
            # Create a ScoreForm instance using the data from the form
            # request.POST = all text input from the submitted form
        if form.is_valid():
            # Check if the form passed DJANGOS built in validation
            score_entry = form.save(commit=False)
                # Create a new Score object from the form, but DON’T save to DB yet
                # I will manually attach the event + match the player names first

            player_name = form.cleaned_data['player']
            teammate_name = form.cleaned_data['teammate']
                # Pull the cleaned text inputs from the form (both required for my logic)
            valid = True
                # Flag that tracks whether both names were matched to real Player objects
                
            # BELOW  = Try to match typed name to Player model 
            # .strip is PYTHON string METHOD (remove whitespace around text like space)
            # .split= turns string into multiple pieces with "space" and how many times to split
            try:
                first, last = player_name.strip().split(" ", 1) 
                score_entry.player = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                # player.objects.get = DJANGO ORM to query player model, goal is first and last name match exact
                # __iexact is LOOKUP MODIFER in DJANGO that is case-INSENSITIVE (alex === Alex, ALEX, alEx)
                    
            # BELOW = Try/except block handles errors from query like if .split fals or player does not exist
            # if either of those happen, add an error message to the form. 
            # valid = False UNTIL the USER fixes the error (never the systems fault ;) )
            except (ValueError, Player.DoesNotExist):
                form.add_error('player', f"No player found for '{player_name}'.")
                valid = False

            if teammate_name:
                # check if a teammate name was submitted on the form 
                # (teammate is optional, bc 1. not all players are in system 2. Some events are solo play/no teams)
                try:
                    first, last = teammate_name.strip().split(" ", 1)
                    # clean up and split the teammate name
                    # .strip() = removes whitespace like spacces
                    # .split (" ", 1) = splits teammate name string into 2 pieces (first & last)
                    score_entry.teammate = Player.objects.get(first_name__iexact=first, last_name__iexact=last)
                    # DJANGO ORM to look up teammate in the PLAYER MODEL
                    # .get(...) = find one UNIQUE MATCH
                    # __iexact = LOOKUP MODIFER in DJANGO that is case-INSENSITIVE (alex === Alex, ALEX, alEx)
                    
                    
            # BELOW = Try/except block handles errors from query like if .split fals or player does not exist
            # if either of those happen, add an error message to the form. 
            # valid = False UNTIL the USER fixes the error (never the systems fault ;) )
                except (ValueError, Player.DoesNotExist):
                    form.add_error('teammate', f"No player found for '{teammate_name}'.")
                    valid = False
                    
                    
            else:
                score_entry.teammate = None
                # if the teammate field was left blank, no problem. 
                # Set to the database so it knows score is solo (slight issue with this below)
                # i dont have EVERY SINGLE PLAYER in the data base from the inceptioon of BGA...
                # ... only players who have 5+ events OR a tour win were added to the original player list
                # so in the circumstance that I seed all the old EVENTS - there will be leaderboards w/ mostly...
                # teams of 2 but also will APPEAR like some players posted SOLO scores in these 2man scrambles
                # solution is prob to bite the bullet and ADD EVERY SINGLE PLAYER to the database thru admin/portal
                

            if not valid:
                # if anything went wrong with the LOOKUP (set valid to False), do not save the score, reload the page with error messages
                return render(request, 'bgaapp/leaderboard.html', {
                    'event': event,
                    'scores': scores,
                    'form': form,
                    'all_players': Player.objects.all() # .all is DJANGO METHOD, () must be included. Thats how PYTHOIN knows to execute METHOD
                })
                # return render(...) = DJANGO response FUNCTION to re render the leaderboard template
                # 'event': event = passing the SPECIFIC EVENT to the template, used to show EVENT name @top
                # 'scores': scores = passing the current leaderbaord data(scores already submitted)
                # 'form': form = passing the SCOREFORM that was submitted
                # 'all_players': Player.objects.all() = passed so the template can build the data list of name suggstions
                

            score_entry.event = event
            # this line connects the SCORE to the current EVENT (score_entry is new score object)
            # manually assigning the score_entry to its related EVENT field
            # This is CRUCIAL bc the form doesent know which event its apart of w/o assigning the SPECIFIC EVENT
           
            score_entry.to_par = score_entry.score - 72
            # This line calculates score entered against par. ISSUE = NOT ALL COURSES ARE PAR 72 (NEEDS WORK)
            # score_entry.score = is the raw score submitted by the user
            # 72 = DEFAULT PAR VALUE (considering creating more in depth COURSE SPECIFIC LOGIC...
            # ... and creating variable of par at that corse, again NEEDS WORK)
            # if a score comes in at 68 the return will show a score of -4 (score minus par) 68 - 72 = -4
            # if a score comes in at 76 the return will show a score of +4 (score minus par) 76 - 72 = +4
            
            score_entry.save() # save is DJANGO METHOD, () must be included. Thats how PYTHOIN knows to execute METHOD
            # This is where the score finally gets saved to the DB
            # before this line, it was just a form object living in memory (commit=False)
            # This writes the FULL SCORE ENTRY to the SCORES TABLE with: the linked event, player &teammate,
            # raw score(like 76) and the SCORE converted RELATIVE to par (like +4)

            # Recalculate placements after score added
            ordered_scores = event.scores.order_by('score')
            # Pull all SCORES linked to this specific EVENT
            # .scores = reverse relatiuon from EVENT to SCORE via the foreign key (like results/7/)
            # .order_by('score') = sort all SCORES F/ lowest to highest (lowest score wins)
            placement = 1
            # placement = 1 is the VARAIABLE that tracks the CURRENT PLACEMENT value
            # placement starts at 1(firstplace)
            # gets reused in the loop and assigned to each score
            last_score = None
            # THIS LINE IS KEY in tracking tie logic. 
            # helps check - 'Is this score the same as the last one?'
            # if YES - its a tie, give the players/ teams the SAME PLACEMENT
            # if NO - ok, move to the next placement
            actual_placement = 1
            # Tracks how many scores in the loop so far
            # it always goes UP BY 1, (unless in the event of a tie, they share that placement like 2nd and next score placement = 4th)
            # Used to assign the correct NEXT PLACEMENT only where there is NOT A TIE

            for s in ordered_scores:
            # start looping through the sorted list of scores (ordered_scores)
            # s = each INDIVIDUAL SCORE OBJECT on the list
            # ordered top to bottom (lowest score to highest score)
                if last_score is not None and s.score == last_score:
            # Check if the CURRENT SCORE is a TIE w/ previous one
            # last_score is not None = skip this check for the FIRST SCORE in the list
            # s.score == last_score = detection for a TIE (give the same placement)
                    s.placement = f"{placement}"  
            # If its a TIE, assign the SAME PLACEMENT as the last one
            # using f-string to turn the integer into a string (1 = 1st = first) (2 = 2nd = second) etc
            # multiple SCORE OBJECTS have the low score of 71? BOTH get PLACEMENT of 1/1st/first
                else:
                    placement = actual_placement
                    s.placement = f"{placement}"
            # ABOVE block runs if the SCORE IS NOT A TIE
            # assign the next avaialble placement using actual_placement
            # placement = actual_placement UPDATES THE PLACEMENT tracker for future comparisons
            # then that number(placement) is assigned to the current score
                s.save() # save is DJANGO METHOD, () must be included. Thats how PYTHOIN knows to execute METHOD
                # saving the UPDATED SCORE back to the DB
                # Now it has a NEW PLACEMENT value displayed in the leaderboard and medal logic) 
                last_score = s.score
                # UPDATE the last_score tracker to this SCORES value
                # used for comparison on the next loop to check for ties
                actual_placement += 1
                # += 1 is to make sure this value is always bumped by 1. 
                # example 1. Alex 68(placement=1), Jon 68(placement=1) Steve 70 (placement=2),BUT actual_placement = 3

            return redirect('leaderboard', pk=event.pk)
            # if the form was submitted correctly, redirect the user to the leaderboard from that event
            # pk=event.pk = pass the same EVENTS primary key so the user lands back on the SAME leaderboard

    else:
        form = ScoreForm()
        # This else runs IF the request was NOT a form submission
        # meaning if the user is visiting the page with a GET request (clicking into a leaderboard)..
        # a new blank SCOREFORM for them to fill out
        # This is what powers the "ADD NEW SCORE" form at bottom of leadeerboard page

    return render(request, 'bgaapp/leaderboard.html', {
        'event': event,
        'scores': scores,
        'form': form,
        'all_players': Player.objects.all()
    })
    # This block is the final response - the HTML page that gets returned for both:
    # 1. Visiting the leaderboard (GET)
    # 2. Submitting a broken or invalid (POST) with errors
    # 'event' = displays EVENT name, Course, Date
    # 'scores' = Table of all submitted scores (used for rendering)
    # 'form' = SCORE ENTRY FORM
    # 'all_players' = populates the <datalist> for the autocomplete suggestions 
    
#--------------------------------------------------------------------------------------------------#


#---------------------------- 6. EDIT SCORE VIEW (Edit Submitted Score) ----------------------------#
@require_http_methods(["GET", "POST"])
# @ is the PTHON DECORATOR SYMBOL (shorthand for "wrap this FUNCTION W/ another FUNCTION")
# Stops users from accessing it via weird methods like DELETE or PUT
# GET = show the form with the current score info pre filled
# POST = process the form submission and update the Score in the DB
def edit_score_view(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    # STEP 1 = Find the specific SCORE we want to edit, using its unique ID (score_id)...
    # get_object_or_404 = builtin DJANGO FUNCTION — returns the object or shows 404 page if not found

    event = score.event
    # STEP 2 = Load the EVENT this SCORE is tied to (used later for placement)

    if request.method == "POST":
    # Step 3 = If the user submitted the form via (POST), its processed below
    
        form = ScoreForm(request.POST, instance=score)
        # STEP 4 = Create a new ScoreForm using the submitted form data AND tie it to the existing SCORE instance
        # instance=score is KEY — tells DJANGO im EDITING this EXACT SCORE object (not creating a new one)
        # W/o instance=score, DJANGO would try to make a whole NEW SCORE object
    
        if form.is_valid():
        # STEP 5 = If the form passes validation, update the Score fields and save to DB
            updated_score = form.save(commit=False)
            # save(commit=False) = holds off on saving the changes so the extra fields can be modified first 
            updated_score.to_par = updated_score.score - 72
            # Manually recalculate the to_par field (just like in leaderboard_view) (NEEDS WORK -PAR72 is not global)
            updated_score.save()
            # This line saves the updated Score object to the DB
           
            # STEP 6 = Recalculate leaderboard placements for the full event
            ordered_scores = event.scores.order_by('score')
            # Grab ALL scores for this event, ordered lowest to highest (classic leaderboard logic)
            
            placement = 1
            last_score = None
            actual_placement = 1
            # placement = display placement for ties (can stay the same across multiple scores)
            # actual_placement = always increases by 1 and controls next available place number
            # last_score = tracks what the previous score value was so we can detect TIES 


            for s in ordered_scores:
                if last_score is not None and s.score == last_score:
                    #Tie Check = If this score is the same as the one before it, assign the same PLACEMENT
                    s.placement = f"{placement}"
                else:
                    placement = actual_placement
                    s.placement = f"{placement}"
                s.save()
                last_score = s.score
                actual_placement += 1
                # Placement logic loops through the scores and handles ties so same scores = same place

            return redirect('leaderboard', pk=event.pk)
            # After everything is updated, redirect user back to the same leaderboard page
            # pk=event.pk = keeps the user inside the correct event context
    else:
        form = ScoreForm(instance=score)
        # If user is just visiting the edit page (GET request), show them a pre filled ScoreForm
        # instance=score = pre-loads the form fields with current data for this score

    return render(request, 'bgaapp/edit_score.html', {
        'form': form,
        'score': score,
        'event': event
    })
    # STEP 7 = render the edit_score.html template
    # Passes 3 objects:
    # 'form' = the form itself (for display)
    # 'score' = the actual score object (can show values in the template)
    # 'event' = used for the header/title or back button link
#--------------------------------------------------------------------------------------------------#


#---------------------------- 7. DELETE SCORE VIEW (Remove a Score + Recalculate) ----------------------------#
def delete_score(request, pk):
    score = get_object_or_404(Score, pk=pk)
    # STEP 1 = Get the specific SCORE to delete using its primary key (pk)
    # get_object_or_404 = DJANGO FUNCTION that either returns the Score or shows a 404 page if it doesn’t exist

    event = score.event
    # STEP 2 = Grab the EVENT this score belongs to (used later to recalculate placements and redirect properly)

    score.delete()
    # STEP 3 = Delete the selected SCORE from the database
    # DJANGO handles this with a single .delete() call on the object
    # This is a PERMANENT delete — the record is removed from the scores table

    # STEP 4 = Recalculate leaderboard placements after the deletion
    ordered_scores = event.scores.order_by('score')
    # After deleting, re-pull all remaining scores for this event, sorted lowest to highest

    placement = 1
    last_score = None
    actual_placement = 1
    # placement = tracks visible placement (so tied scores share the same number)
    # last_score = helps us detect if the current score matches the previous one (TIE CHECK)
    # actual_placement = always increases by 1 — even if placement doesn't (used to assign the next available slot)

    for s in ordered_scores:
        if last_score is not None and s.score == last_score:
            # If this score is a TIE with the last one, give it the SAME placement
            s.placement = f"{placement}"
        else:
            # If NOT a tie, assign the next available placement number
            placement = actual_placement
            s.placement = f"{placement}"
        s.save() # save is DJANGO METHOD, () must be included. Thats how PYTHOIN knows to execute METHOD
        # Save the updated placement to the DB

        last_score = s.score
        # Update last_score tracker for the next loop
        actual_placement += 1
        # Always increment actual_placement no matter what
        # Even if there’s a tie and placement stays the same, this tracks how many scores we’ve looped through

    return redirect('leaderboard', pk=event.pk)
    # STEP 5 = After recalculating, send user back to the leaderboard for the same event
    # pk=event.pk = keeps the user within the correct event context

#--------------------------------------------------------------------------------------------------#

