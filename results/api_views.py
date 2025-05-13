# File Purpose: API endpoint to serve future BGA events in JSON format

from django.http import JsonResponse
from django.utils import timezone
from .models import Event

def schedule_api(request):
    today = timezone.now().date()
    future_events = Event.objects.filter(date__gte=today).order_by('date')

    data = [
        {
            'date': event.date,
            'course_name': event.course_name,
            'event_type': event.name,
            'season': event.season,
            'notes': event.notes,
        }
        for event in future_events
    ]

    return JsonResponse(data, safe=False)
