from django.shortcuts import render
from results.models import Event

# Create your views here.
# Tour Legacy page (shows list of seasons)
def tour_legacy(request):
    seasons = [2019, 2020, 2021, 2022, 2023, 2024]
    return render(request, 'legacy/tour_legacy.html', {'seasons': seasons})

def season_detail (request, season):
    events = Event.objects.filter(season=season).order_by('date')
    return render(request, 'legacy/season_detail.html', {
        'season': season,
        'events': events
    })