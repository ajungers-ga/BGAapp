from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Player
from .forms import PlayerForm
from results.models import Score






class PlayerListView(ListView):
    model = Player
    template_name = 'bgaapp/player_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlayerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('player_list')









class PlayerDetailView(DetailView):
    model = Player
    template_name = 'bgaapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

        # Get all scores where the player finished 1st
        wins = Score.objects.filter(player=player, placement="1st").select_related('event')
        context['event_wins'] = wins
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
