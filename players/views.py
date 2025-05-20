# FILE Purpose: View logic for the PLAYERS section of the BGA Tour Tracker
# This file powers the Tour Players, Player Profiles, Career Stats, and handles edit/delete logic
# Templates include: 1. player_list.html, 2. player_detail.html, 3. player_form.html, 4. player_confirm_delete.html, 5. player_stats.html
# Uses DJANGOS class based views for consistency and modularity
# Imports forms, models, and Score data for cross-app logic (like events played and wins)
# This file handles both displaying players and processing form submissions (like editing or creating)




#----------------------------------IMPORT DEPENDENCIES----------------------------------#
from django.shortcuts import redirect                   # used to redirect after POST

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from django.urls import reverse_lazy                    # used for success_url to avoid circular imports
from django.db import models                            # needed for Q object (advanced filtering)
from .models import Player                              # local app model for BGA players
from .forms import PlayerForm                           # custom form class
from results.models import Score                        # imported to calculate wins using the Score model
#----------------------------------IMPORT DEPENDENCIES----------------------------------#




#----------------------------PLAYER LIST VIEW (ALL PLAYERS PAGE)----------------------------#
class PlayerListView(ListView):
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
            # Checks the form's built-in validation logic
            # Makes sure all required fields are filled, types are correct, no validation errors

            form.save()                     
            # If the form is valid, save the new PLAYER object to the database

        return redirect('player_list')      
        # After saving (or even if form is invalid), redirect user back to the player list page
        # Prevents duplicate form submissions on page refresh
        # 'player_list' is the NAME of the route (from players/urls.py)

#----------------------------PLAYER LIST VIEW (ALL PLAYERS PAGE)----------------------------#






#----------------------------PLAYER DETAIL VIEW (PROFILE PAGE)----------------------------#
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()  # Load the player from the URL’s primary key (pk)

        # BELOW = Get all event wins where this player was either player or teammate
        # models.Q() lets me OR conditions (player= or teammate=)
        # placement__in = handles both "1" and "1st" as valid first place strings
        context['event_wins'] = Score.objects.filter(
            models.Q(player=player) | models.Q(teammate=player),
            placement__in=["1", "1st"]
        ).select_related("event")  # Optimizes DB query by joining related event data

        return context
#----------------------------PLAYER DETAIL VIEW (PROFILE PAGE)----------------------------#






#----------------------------PLAYER UPDATE VIEW (EDIT PAGE)----------------------------#
class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'bgaapp/player_form.html'
    success_url = reverse_lazy('player_list')  # Redirect back to list after update
#----------------------------PLAYER UPDATE VIEW (EDIT PAGE)----------------------------#






#----------------------------PLAYER DELETE VIEW (CONFIRM DELETE PAGE)----------------------------#
class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'bgaapp/player_confirm_delete.html'
    success_url = reverse_lazy('player_list')  # Redirect to list after deletion
#----------------------------PLAYER DELETE VIEW (CONFIRM DELETE PAGE)----------------------------#






#----------------------------PLAYER STATS VIEW (CAREER STATS PAGE)----------------------------#
class PlayerStatsView(TemplateView):
    template_name = 'bgaapp/player_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # BELOW = sort all players in DESCENDING ORDER of career_wins
        # lambda p: p.career_wins → pulls wins from each player
        players = sorted(Player.objects.all(), key=lambda p: p.career_wins, reverse=True)

        context['players'] = players
        return context
#----------------------------PLAYER STATS VIEW (CAREER STATS PAGE)----------------------------#