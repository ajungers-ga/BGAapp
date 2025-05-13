from django.shortcuts import render
from django.utils import timezone
from results.models import Event  # importing Event model from results app

# Home page
def home(request):
    today = timezone.now().date()

    # Get the next upcoming event
    next_event = Event.objects.filter(date__gte=today).order_by('date').first()

    # Get the last completed event
    last_event = Event.objects.filter(date__lt=today).order_by('-date').first()

    return render(request, 'core/home.html', {
        'next_event': next_event,
        'last_event': last_event
    })
