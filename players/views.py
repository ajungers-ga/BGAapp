# FILE Purpose: View logic for the PLAYERS section of the BGA Tour Tracker
# This file powers the Tour Players, Player Profiles, Career Stats, and handles edit/delete logic
# Templates include: 1. player_list.html, 2. player_detail.html, 3. player_form.html, 4. player_confirm_delete.html, 5. player_stats.html
# Uses DJANGOS class based views for consistency and modularity
# Imports forms, models, and Score data for cross-app logic (like events played and wins)
# This file handles both displaying players and processing form submissions (like editing or creating)

# Why use reverse_lazy instead of reverse()?
# Because all of my reverse_lazy references exist INSIDE a class definition,
# which loads as soon as DJANGO starts, but the URL patterns may not be loaded,
# which would BREAK reverse(), BUT reverse_lazy() DELAYS that lookup until the view actually runs 
# (s/o my classmate -  Zack, for breaking that down for me in unit 4 group collab)

# views in order top down
# (line39)  1. PLAYER LIST VIEW #-----# (Tour Players Page)
# (line94)  2. PLAYER DETAIL VIEW #---# (Tour Player Detail card (profile page))
# (line132) 3. PLAYER UPDATE VIEW #---# (INACTIVE: update player (profile page))
# (line158) 4. PLAYER DELETE VIEW #---# (INACTIVE: delete players from the Tour Players Page)
# (line178) 5. PLAYER STATS VIEW #----# (Career Stats Page)




#----------------------------------IMPORT DEPENDENCIES----------------------------------#
from django.shortcuts import redirect                   # used to redirect after POST

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from django.urls import reverse_lazy                    # used for success_url to avoid circular imports
from django.db import models                            # needed for Q object (advanced filtering)
from .models import Player                              # local app model for BGA players
from .forms import PlayerForm                           # custom form class
from results.models import Score                        # imported to calculate wins using the Score model

# POST PRESENTATION, PRE LAUNCH (3.0)
from django.contrib.auth.mixins import UserPassesTestMixin

#----------------------------------IMPORT DEPENDENCIES----------------------------------#

# POST PRESENTATION, PRE LAUNCH (3.1)
class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser



#---------------------------- 1. PLAYER LIST VIEW (ALL PLAYERS PAGE)----------------------------#
# POST PRESENTATION, PRE LAUNCH (3.2)
class PlayerListView(AdminOnlyMixin, ListView):
    model = Player
    template_name = 'bgaapp/player_list.html'

    # Add a player form (NO LONGER ACTIVE on public site) to the context so the template could render one if needed
    def get_context_data(self, **kwargs):
    # What is self?        # PYTHONS reference to the CURRENT INSTANCE of the class (PlayerListView in this case)
    # What is **kwargs?    # Lets DJANGO pass any keyword arguments like view state or object metadata — helps extend the default behavior

        context = super().get_context_data(**kwargs)
        # ABOVE = super() = calling the built in DJANGO method(parentheses needed for all methods) 
        # to load the default context (this will already include object_list which is all players)

        context['form'] = PlayerForm()
        # This line manually adds a new, blank PlayerForm to the context dictionary
        # This makes {{ form }} available in the player_list.html template
        # Even though this is NO LONGER ACTIVE on the public site, I kept it in case I re-enable form input later

        return context
        # last, return the full context to the template so it can render everything



    # If a POST request is made (like from a form), try to create a new player
    def post(self, request, *args, **kwargs):
        # self = PYTHONS reference to the CURRENT INSTANCE of this class (PlayerListView)
        # request = the incoming HTTP POST request from the browser (contains form data)
        # *args, **kwargs = optional arguments passed by DJANGO (URL params, view state, etc.)

        form = PlayerForm(request.POST, request.FILES)
        # PlayerForm(...) = create a new form instance using the submitted form data
        # request.POST = holds the TEXT-based input fields (like name, hometown, etc.)
        # request.FILES = holds any FILE uploads (like player images)
        # Both are required to process a file-uploading form properly

        if form.is_valid():
            # Checks the forms built in validation logic
            # Makes sure all required fields are filled, types are correct, no validation errors

            form.save()                     
            # If the form is valid, save the new PLAYER object to the database

        return redirect('player_list')      
        # After saving (or even if form is invalid), redirect user back to the player list page
        # Prevents duplicate form submissions on page refresh
        # 'player_list' is the NAME of the route (from players/urls.py)

#----------------------------PLAYER LIST VIEW (ALL PLAYERS PAGE)----------------------------#






#---------------------------- 2. PLAYER DETAIL VIEW (PROFILE PAGE)----------------------------#
class PlayerDetailView(DetailView):
    model = Player
    # model = This view is tied to the Player model — it will display a single Player’s profile page

    template_name = 'bgaapp/player_detail.html'
    # template_name = This is the HTML file that shows player details (name, image, hometown, stats, etc.)

    # BELOW = Overriding DJANGO’S get_context_data method to add custom variables to the template
    def get_context_data(self, **kwargs):
        # self = PYTHON’S reference to the current class instance (PlayerDetailView)
        # **kwargs = lets Django pass in additional context arguments (like object metadata)

        context = super().get_context_data(**kwargs)
        # super() = gets the default context data (includes 'object', which is the Player)

        player = self.get_object()
        # self.get_object() = grabs the Player object based on the primary key in the URL (like /players/3/)

        # BELOW = Query the Score model to find wins for this player
        # Q(player=player) | Q(teammate=player) = include scores where player OR (|) teammate is this person
        # placement__in = make sure we match either "1" or "1st" in the placement field
        # .select_related("event") = preloads the linked Event data to avoid extra DB hits per loop
        context['event_wins'] = Score.objects.filter(
            models.Q(player=player) | models.Q(teammate=player),
            placement__in=["1", "1st"]
        ).select_related("event") # THIS IS THE MAGIC TO DYNAMIC LINK WINS TO PROFILE PAGE

        return context
        # Return the updated context dictionary — now includes both the Player AND their event wins
#----------------------------PLAYER DETAIL VIEW (PROFILE PAGE)----------------------------#







#---------------------------- 3. PLAYER UPDATE VIEW (EDIT PAGE)----------------------------#
# INACTIVE! This view is DISCONNECTED from the public site to protect player data
class PlayerUpdateView(UpdateView):
    model = Player
    # model = Tells Django which MODEL this view is updating (in this case, a Player object)

    form_class = PlayerForm
    # form_class = Connects the view to my custom PLAYER FORM (defined in forms.py)
    # This is the form users will fill out when editing an existing player

    template_name = 'bgaapp/player_form.html'
    # template_name = Tells Django which HTML template to render for the edit form
    # This file will contain {{ form }} and a submit button

    success_url = reverse_lazy('player_list')
    # success_url = Where to redirect after a successful form submission
    # reverse_lazy = used instead of reverse() to avoid issues at import time (recommended in class-based views)
    # 'player_list' = Name of the route in urls.py → sends user back to the full player list page
#----------------------------PLAYER UPDATE VIEW (EDIT PAGE)----------------------------#







#---------------------------- 4. PLAYER DELETE VIEW (CONFIRM DELETE PAGE)----------------------------#
# INACTIVE! This view is DISCONNECTED from the public site to protect player data
# It was originally used to delete players via the front-end, but I disabled this
# Deletion can now only happen internally via the Django Admin Panel

class PlayerDeleteView(DeleteView):
    model = Player
    # model = The model this view will delete (Player)

    template_name = 'bgaapp/player_confirm_delete.html'
    # template_name = HTML template that shows the deletion confirmation prompt

    success_url = reverse_lazy('player_list')
    # success_url = After deletion, redirect to the main player list page
    # reverse_lazy = resolves the 'player_list' route name safely at runtime

#----------------------------PLAYER DELETE VIEW (CONFIRM DELETE PAGE)----------------------------#



#---------------------------- 5. PLAYER STATS VIEW (CAREER STATS PAGE)----------------------------#
class PlayerStatsView(TemplateView):
    template_name = 'bgaapp/player_stats.html'
    # template_name = This is the HTML file that renders the career stats table
    # Uses {{ player.first_name }}, {{ player.career_wins }}, etc. inside a Bootstrap table

    # BELOW = Overriding DJANGO’S get_context_data method to pass in my own custom data
    def get_context_data(self, **kwargs):
        # self = PYTHONS reference to the CURRENT INSTANCE of the class (PlayerStatsView)
        # **kwargs = allows Django to pass in extra info (like object metadata or session state)

        context = super().get_context_data(**kwargs)
        # super() = calling Django’s built-in method to initialize the default context
        # This ensures any standard variables are still included (even though I’m not using any)

        # Custom logic: grab ALL players and sort by career_wins (highest first)
        players = sorted(
            Player.objects.all(),                # Pull all player objects from the database
            key=lambda p: p.career_wins,         # lambda function(anonymous function, defining function w/o using def) = get the career_wins for each player
            reverse=True                         # reverse=True = sort from most to least
        )
        # lambda is a built in PYTHON KEYWORD
        # lambda p: p.career_wins, is saying 'for each player(p), use their career_wins value as the SORTING KEY
        context['players'] = players
        # Add the sorted player list to the context dictionary so it can be used in the template
        # Template will loop through {{ players }} to render stats

        return context
        # Return the full context to be passed into player_stats.html
#----------------------------PLAYER STATS VIEW (CAREER STATS PAGE)----------------------------#
