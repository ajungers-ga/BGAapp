from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import models

from .models import Player
from .forms import PlayerForm
from results.models import Score






class PlayerListView(ListView):
    model = Player
    template_name = 'bgaapp/player_list.html'


# What is self?------ A. PYTHONS reference to the CURRENT CLASS INSTANCE
# What is **kwargs?-- A. allows the passing of any number or KEYWORD aruments, DJANGO uses it to send object, view etc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlayerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('player_list')



# What is self?------ A. PYTHONS reference to the CURRENT CLASS INSTANCE
# What is **kwargs?-- A. allows the passing of any number or KEYWORD aruments, DJANGO uses it to send object, view etc

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

       # give me all SCORE OBJECTS WHERE (player is this player OR teammate is this player AND placement is 1 or 1st)
        context['event_wins'] = Score.objects.filter(            # without Q, django filters default to AND ONLY
            models.Q(player=player) | models.Q(teammate=player), # models.Q = DJANGO uses query logic, LIKE OR CONDITIONALS 
            placement__in=["1", "1st"]                           # so im doing a sweet COMBO of OR operator ( | ) and...
        ).select_related("event")  # using & operator (under the hood - DJANGO treats multiple arguments in .filter as being AND togther)  

        return context




    
    
    

class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'bgaapp/player_form.html'
    success_url = reverse_lazy('player_list')
    
    
    
    
    
    
    
    
    

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'bgaapp/player_confirm_delete.html'
    success_url = reverse_lazy('player_list')
