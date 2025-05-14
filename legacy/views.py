from django.shortcuts import render
from results.models import Event

# Create your views here.
# Tour Legacy page (shows list of seasons)

# telling DJANGO to give me a FLAT list of all unique seasons from the event table from top down
def tour_legacy(request):
    seasons = Event.objects.values_list('season', flat=True).distinct().order_by('-season')
    return render(request, 'legacy/tour_legacy.html', {'seasons': seasons})

def season_detail (request, season):
    events = Event.objects.filter(season=season).order_by('date')
    return render(request, 'legacy/season_detail.html', {
        'season': season,
        'events': events
    })